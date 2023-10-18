import states
import time
from PIL import ImageGrab
from utils import lerp
import keyboard
import threading

HP_POT_KEY = None
MP_POT_KEY = None

def initialize():
    global HP_POT_KEY
    global MP_POT_KEY

    enable_hp = None
    enable_mp = None
    
    settings = states.settings

    if settings.get("enable_hp"):
        enable_hp = settings["enable_hp"]
    else:
        settings["enable_hp"] = input("Would you like to enable auto hp pot? [y/n]\n")
        enable_hp = settings["enable_hp"]

    if enable_hp[0].lower() == 'y':
        states.auto_hp_on = True
        print("What is your HP pot key?")
        if settings.get("hp_pot_key"):
            HP_POT_KEY = settings["hp_pot_key"]
        else:
            while HP_POT_KEY == 'enter' or HP_POT_KEY is None:
                settings["hp_pot_key"] = keyboard.read_key()
                HP_POT_KEY = settings["hp_pot_key"]
                time.sleep(0.1)
        print(f"Your hp pot key is {HP_POT_KEY}")
        print("auto hp pot on")

    if settings.get("enable_mp"):
        enable_mp = settings["enable_mp"]
    else:
        settings["enable_mp"] = input("Would you like to enable auto mp pot? [y/n]\n")
        enable_mp = settings["enable_mp"]

    if enable_mp[0].lower() == 'y':
        states.auto_mp_on = True
        print("What is your MP pot key")
        if settings.get("mp_pot_key"):
            MP_POT_KEY = settings["mp_pot_key"]
        else:
            while MP_POT_KEY == 'enter' or MP_POT_KEY is None:
                settings["mp_pot_key"] = keyboard.read_key()
                MP_POT_KEY = settings["mp_pot_key"]
                time.sleep(0.1)
        print(f"Your mp pot key is {MP_POT_KEY}")
        print("auto mp pot on")
    if states.auto_hp_on or states.auto_mp_on:
        threading.Thread(target=get_bars, daemon=True).start()

def get_bars():
    x = states.window[0]
    y = states.window[1]
    states.HP_COORD = (223 + x, 782 + y, 223 + 105 + x, 782 + 1 + y)
    states.MP_COORD = (331 + x, 782 + y, 331 + 105 + x, 782 + 1 + y)
    while True:
        if states.auto_hp_on:
            check_hp()
        if states.auto_mp_on:
            check_mp()
        time.sleep(0.3)

#handle hp bar
def check_hp():
    global HP_POT_KEY
    if should_pot(states.HP_COORD, 0.5):
        drink_pot(HP_POT_KEY)
#handle mp bar
def check_mp():
    global MP_POT_KEY
    if should_pot(states.MP_COORD, 0.5):
        drink_pot(MP_POT_KEY)


#return true or false depending on how low your bar is
def should_pot(COORD, t):
    bar = ImageGrab.grab(bbox=(COORD))
    target_x = lerp(0, bar.width - 1, t)
    (r,g,b) = bar.getpixel(xy=(target_x, 0))
    if r == g and r == b and g == b and 255 > r > 0:
        return True
    else:
        return False

def drink_pot(POT_KEY):
    keyboard.send(POT_KEY)