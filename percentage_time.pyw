# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 01:48:51 2019


from PIL import Image, ImageDraw

red = (254, 147, 140)
active_color = red
percent = 
progress = 270 - ((1 - percent) * 360)

img = Image.new('RGBA', (100, 100), color = (0,0,0,0))
d = ImageDraw.Draw(img)
d.pieslice([0,0,100,100], -90, progress, fill=active_color, outline=active_color, width=2)
img.save('test.png')


@author: fabia
"""

wake_up_time= 8*60 #expressed in minutes
total_wake_time = 16*60 #expressed in minutes

fontsize= 85
FILTERED_CHARACTERS = ['!','(',')',',','.','?','!',' ',';',':','"',"'"]


import time
import sys
from infi.systray import SysTrayIcon
from PIL import Image, ImageDraw, ImageFont
import pyperclip
import ctypes  # An included library with Python install.   
from nltk.corpus import wordnet
from AccelBrainBeat.brainbeat.binaural_beat import BinauralBeat
from winsound import PlaySound, SND_FILENAME, SND_LOOP, SND_ASYNC
from pynput.keyboard import Key, Controller
import pyautogui as pya
import pyperclip  # handy cross-platform clipboard text handler
import time
import os
import csv


personal_dictionary_object = open("personal_dictionary.csv","w+")
personal_dictionary_writer = csv.writer(personal_dictionary_object)

try:
	os.remove("pil_text_font.ico") #test for it to remove the file before starting to avoid certain conflicts
except OSError:
    pass

def tick ():
    minutes = 60* int(time.strftime('%H')) + int(time.strftime('%M')) ##gets time from system and converts it to minutes
    if minutes < wake_up_time: ###when passing bedtime the percentage will go above 1 and tell you how much you are cutting in to your sleeping time
        time_string = str(100*round((minutes)/480, 5))  ###480 comes to 8hours sleeping time
        color = '#DC143C'
        return time_string, color
    else:
        time_string = str(round(100*(minutes - wake_up_time)/960, 5))  ###960 refers to 16 hours waking time
        color = '#ffffff'
        return time_string, color 

def og_time_tick():
    og_time = str(time.strftime('%H:%M:%S'))
    return og_time

def drawnew ():
    img = Image.new('RGBA', (100, 100), color = (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.line((0,95,100,95), fill='#808080', width= 6)
    d.line((0,95, int(second[:2]) ,95), fill='#ffffff', width= 10)
    d.text((-1,-1), first, font = ImageFont.truetype("arial.ttf", fontsize), fill= color)
    img.save('pil_text_font.ico')

def copy_clipboard():
    #pya.doubleClick(pya.position())
    #pya.hotkey('ctrl', 'c')
    #time.sleep(.01)  # ctrl-c is usually very fast but your program may execute faster
    return pyperclip.paste()

### double clicks on a position of the cursor
##    ab = copy_clipboard()
##    return ab

##list = []
##var = 
##list.append(var) 
##print(list)
def getword(systray):
    word = copy_clipboard()
    for i in FILTERED_CHARACTERS: #filters out unwanted characters
        word = word.replace(i, '')
    syns = wordnet.synsets(word)
    definition_list = []
    synonyms = []
    antonyms =[]
    for i in syns:
            definition_list.append(i.definition())
    for syn in syns:
            for l in syn.lemmas():
                    synonyms.append(l.name())
                    if l.antonyms():
                             antonyms.append(l.antonyms()[0].name())

    definition = 'o) ' + '\no) '.join(definition_list)
    syn_string = ', '.join(synonyms)
    ant_string = ', '.join(antonyms)
    to_display = 'Definition:\n' + str(definition) + '\n\n' + 'Synonyms: \n' + syn_string + '\nAntonyms:\n' + ant_string
    ctypes.windll.user32.MessageBoxW(0, to_display, word, 0)
    
    
    temp_list = [word, definition, syn_string, ant_string]
    personal_dictionary_writer.writerow(temp_list)
switcher = True # having to use this is shitty but i need it as a sort of global on off switch

def play_beats(placeholder):
    binaural_beats()
    global switcher#use the global variable in this function rather than looking for a local one
    if switcher == False:
        PlaySound(None, SND_FILENAME) #the None here just stops whatever sound had been playing before
        switcher = True #return the new state of the variable
        return switcher
    if switcher == True:
        PlaySound('save_binaural_beat.wav', SND_FILENAME | SND_LOOP | SND_ASYNC)
        switcher = False
        return switcher

def binaural_beats():
    '''creates the wav for the beat if necessary'''
    brain_beat = BinauralBeat()
    brain_beat.save_beat(
        output_file_name="save_binaural_beat.wav",
        frequencys=(400, 430),
        play_time=2,
        volume=0.01
        )

def block_on():
    web_block ('on')
def block_off():
    web_block ('off')
    
def web_block (state):
    hostsPath=r"C:\Windows\System32\drivers\etc\hosts"
    redirect="127.0.0.1"
    websites=["www.facebook.com","facebook.com"]
    if state == 'on':
        with open(hostsPath,'r+') as file:
            content=file.read()
            for site in websites:
                if site in content:
                    pass
                else:
                    file.write(redirect+" "+site+"\n")
    if state == 'off':
        with open(hostsPath,'r+') as file:
                content=file.readlines()
                file.seek(0)
                for line in content:
                    if not any(site in line for site in websites):
                        file.write(line)
                file.truncate()




menu_options = (('Define', None, getword),
                ('Binaural Beats', None, play_beats),
                ('Internet', None, (('Block', None, block_on),
                                    ('Unblock', None, block_off),
                                     ))
                )

def callback(systray):
    personal_dictionary_object.close()
    # sys.exit() # I don't know this shit doesnt really work

systray = SysTrayIcon("pil_text_font.ico", "Percentage time", menu_options, on_quit=callback)
systray.start()





while True:
    time_string, color = tick()[0], tick()[1]
    first, second= time_string.split(sep='.')[0],time_string.split(sep='.')[1]
    drawnew()
    systray.update(icon='pil_text_font.ico', hover_text = og_time_tick())
    time.sleep (1)


