import win32gui
from PIL import ImageGrab
import states
from minimap import *
from autopot import *

VISION_HOTKEY = "f7"

# get coordinates of minimap, hp, mp
def initialize():
    #feature to make it not work when the main maplestory window isn't focused
    print(f"Focus on a maplestory window and then press {VISION_HOTKEY} to initialize\n")
    keyboard.wait("f7")
    hwnd = win32gui.GetForegroundWindow()
    if not win32gui.GetWindowText(hwnd).startswith('Maple'):
        print('MapleStory is not focused\n')
        return
    screenshot = get_full_screenshot(hwnd)
    get_mini_map_coords(screenshot)
    return True
    # get_mini_map()
    # get_portals()
    # get_dots()

#get a fullscreenshot of the game
def get_full_screenshot(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    states.window = (x, y, w, h)
    print(states.window)
    screenshot = ImageGrab.grab(bbox=(x, y, x + w, y + h))
    return screenshot

if __name__ == "__main__":
    initialize()