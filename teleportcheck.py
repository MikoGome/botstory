from PIL import ImageGrab
import threading
import states
import time
from playsound import playsound 
import os
import keyboard
import random

def initialize():
    settings = states.settings

    if settings.get("enable_teleport_check"):
        enable_teleport_check = settings["enable_teleport_check"]
    else:
        settings["enable_teleport_check"] = input("Would you like to enable teleport check? [y/n]\n")
        enable_teleport_check = settings["enable_teleport_check"]

    if enable_teleport_check[0].lower() == 'y':
        threading.Thread(target=check, daemon=True).start()
        print('teleport check on')

def check():
    x = states.window[0]
    y = states.window[1]
    while True:
        time.sleep(1)
        if not states.is_playing:
            continue
        hp_mark = ImageGrab.grab(bbox=(x + 950, y + 27, x + 1026, y + 133))
        color_1 = hp_mark.getpixel(xy=(5, 9))
        color_2 = hp_mark.getpixel(xy=(5, 26))
        #check if teleported
        (r1, g1, b1) = color_1
        (r2, g2, b2) = color_2
        if (r1 != 238 or r2 != 238):
               states.is_playing = False
               print("DANGER! STOP PLAYBACK AND PLAYING SOUND")
               speech = 'what\'s going on?'
               threading.Thread(target=talk, args=(speech,), daemon=True).start()
               playdangersound()
               time.sleep(10)

def playdangersound():
    playsound(os.path.abspath(os.path.join('sounds', 'danger.mp3')))

def talk(speech):
    time.sleep(5)
    keyboard.press_and_release('enter')
    for letter in speech:
        time.sleep(random.randrange(10, 25)/100)
        if letter == '?':
            keyboard.press('shift')
        keyboard.press_and_release(letter)
        if letter == '?':
            keyboard.release('shift')
    keyboard.press_and_release('enter')


if __name__ == "__main__":
    initialize()