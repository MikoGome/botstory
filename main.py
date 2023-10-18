import time
import keyboard

import macro
from petfeeder import petfeeder
import vision
import autopot
import minimap
import edge_prune
import settings
import teleportcheck

EXIT_KEY = 'f12'

#MACRO HOTKEYS
RECORD_KEY = macro.RECORD_KEY
PLAY_KEY = macro.PLAY_KEY
SAVE_KEY = macro.SAVE_KEY
LOAD_KEY = macro.LOAD_KEY
EMERGENCY_STOP = macro.EMERGENCY_STOP
JUMP_KEY = macro.JUMP_KEY
HOT_KEYS = macro.HOT_KEYS

def main():
  #initalize settings
  settings.initialize()

  #pet feeder
  petfeeder()

  #vision
  if vision.initialize():
     autopot.initialize()
     minimap.initialize()
     edge_prune.initialize()
     teleportcheck.initialize()
  #macro
  macro.macro()
  
  settings.save()

  #exit function
  while not keyboard.is_pressed(EXIT_KEY):
     time.sleep(0.025)
     if keyboard.is_pressed(macro.RECORD_KEY):
        macro.record_toggle()
        time.sleep(0.1)
     elif keyboard.is_pressed(macro.PLAY_KEY):
        macro.playback_toggle()
        time.sleep(0.1)
     elif keyboard.is_pressed(macro.SAVE_KEY):
        macro.save()
        time.sleep(0.1)
     elif keyboard.is_pressed(macro.LOAD_KEY):
        macro.load()
        time.sleep(0.1)

if __name__ == '__main__':
    main()