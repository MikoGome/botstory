import states
from PIL import Image
import threading
import time
import random
from playsound import playsound
import os
import keyboard
import mss

def initialize():
    settings = states.settings
    warning_mode = None
    if states.settings.get("enable_warning_mode"):
        warning_mode = settings["enable_warning_mode"]
    else:
        settings["enable_warning_mode"] = input("Would you like to enable warning mode? [y/n]\n")
        warning_mode = settings["enable_warning_mode"]
    if warning_mode[0].lower() == 'y':
        states.warning_mode_on = True
    # portal_guard = input("Would you like to enable portal guard? [y/n]\n")
    # if portal_guard[0].lower() == 'y':
    #     get_portals()
    #     states.portal_guard_on = True
    if states.warning_mode_on:
        threading.Thread(target=scan_map, daemon=True).start()
    keyboard.add_hotkey('f6', scan_portals)

def scan_portals():
    get_mini_map()
    get_portals()

def scan_map():
    #will do portal guard later
    red_cache = []
    while(True):
        time.sleep(3)
        if not states.is_playing:
            continue
        get_mini_map()
        get_dots()
        if states.warning_mode_on:
            if states.red_dots != red_cache and len(states.red_dots) >= len(red_cache):
                print('Player detected... playing sound')
                # states.is_playing = False
                playsound(os.path.abspath(os.path.join('sounds', 'warning.mp3')))
                print('back to scanning')
            red_cache = states.red_dots[:]


#get just the coordinates of minimap
def get_mini_map_coords(screenshot):
    initial_x = 9
    initial_y = 55
    final_x = None
    final_y = None
    in_mini_map_x = False
    in_mini_map_y = False
            
    for x in range(initial_x, states.window[2]//3):
        #check for any whites, if there are then we hit the end of the minimap horizontally
        (r,g,b) = screenshot.getpixel(xy=(x, initial_y))
        if (r == 255 and b == 255 and g == 255) or (r == 210 and g == 219 and b == 237):
            if final_x is None:
                final_x = x - 1
            break
        #get only the relevant parts of minimap
        if r <= 100 and g <= 100 and b <= 100:
            if not in_mini_map_x:
               initial_x = x
               in_mini_map_x = True
            else:
                final_x = x

    for y in range(initial_y, states.window[3]//3):
        #check for any whites, if there are then we hit the end of the minimap vertically
        (r,g,b) = screenshot.getpixel(xy=(initial_x, y))
        if (r == 255 and b == 255 and g == 255) or (r == 210 and g == 219 and b == 237):
            if final_y is None:
                final_y = y - 1
            break

        # get only the relevant parts of minimap
        if r <= 100 and g <= 100 and b <= 100:
            if not in_mini_map_y:
               initial_y = y
               in_mini_map_y = True
            else:
                final_y = y

    coords = (
        states.window[0] + initial_x, 
        states.window[1] + initial_y, 
        states.window[0] + final_x + 1, 
        states.window[1] + final_y + 1
    )
    states.mini_map_coords = coords
    return coords

#get the minimap with the coordinates
def get_mini_map():
    with mss.mss() as sct:
    #mini_map = ImageGrab.grab(bbox=states.mini_map_coords)
        img = sct.grab(states.mini_map_coords)
        mini_map = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
        states.mini_map = mini_map
        return mini_map


#PORTALS
def get_portals():
    states.portals = []
    for x in range(0, states.mini_map.width):
        for y in range(states.mini_map.height, 0, -1):
            temp_portal = get_portal(x, y, states.mini_map)
            if temp_portal:
                states.portals.append(temp_portal)
    print('portals', states.portals)




def get_portal(x, y, map):
    try:
        if (
            map.getpixel(xy=(x + 3, y)) == (51, 204, 255) and 
            map.getpixel(xy=(x + 4, y)) == (17, 170, 238) and 
            map.getpixel(xy=(x, y + 3)) == (102, 221, 255) and 
            map.getpixel(xy=(x + 2, y + 3)) == (51, 204, 255) and 
            map.getpixel(xy=(x + 5, y + 3)) == (17, 170, 238) and 
            map.getpixel(xy=(x + 7, y + 3)) == (51, 204, 255) 
        ):
            return (x, y, 8, 8)
        else:
            return False
    except: 
        return False

#DOTS
def get_dots():
    states.yellow_dot = ()
    states.red_dots = []
    # found_red = False
    # found_yellow = False
    for x in range(0, states.mini_map.width):
        for y in range(states.mini_map.height, 0, -1):
            # if found_red and found_yellow:
            #     return
            # get player
            # if not found_yellow:
            #     temp_yellow_dot = get_yellow_dot(x, y, states.mini_map)
            #     if temp_yellow_dot:
            #         states.yellow_dot = temp_yellow_dot
            #         found_yellow = True
            # if not found_red:
            temp_red_dot = get_red_dot(x, y, states.mini_map)
            if temp_red_dot:
                states.red_dots.append(temp_red_dot)
                    # found_red = True


def get_yellow_dot(x, y, map):
    try:
        if (map.getpixel(xy=(x + 1, y)) == (255, 255, 0) and
            map.getpixel(xy=(x, y + 1)) == (255, 255, 0) and
            map.getpixel(xy=(x + 1, y + 1)) == (255, 255, 0) and
            map.getpixel(xy=(x - 1, y + 2)) == (255, 255, 0) and
            map.getpixel(xy=(x, y + 2)) == (255, 255, 136) and
            map.getpixel(xy=(x + 1, y + 2)) == (255, 255, 136) and
            map.getpixel(xy=(x + 2, y + 2)) == (255, 255, 0)
        ):
            return (x-2, y, 5, 5)
        else:
            return False
    except:
        return False

def get_red_dot(x, y, map):
    try:
        if (
            map.getpixel(xy=(x + 2, y)) == (255, 0, 0) and 
            map.getpixel(xy=(x + 1, y + 1)) == (255, 0, 0) and 
            map.getpixel(xy=(x + 2, y + 1)) == (238, 0, 0) and 
            map.getpixel(xy=(x + 3, y + 1)) == (255, 0, 0) and 
            map.getpixel(xy=(x, y + 2)) == (255, 0, 0) and 
            map.getpixel(xy=(x + 1, y + 2)) == (238, 0, 0) and 
            map.getpixel(xy=(x + 2, y + 2)) == (221, 0, 0) and 
            map.getpixel(xy=(x + 3, y + 2)) == (238, 0, 0) and 
            map.getpixel(xy=(x + 4, y + 2)) == (255, 0, 0)
        ):
            return (x, y, 6, 6)
        else:
            return False
    except: 
        return False
        
