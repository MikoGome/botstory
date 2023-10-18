import keyboard
import mouse
import random
import threading
import time
import json
import states
import os
import minimap
from utils import variance

#states
initial_time = None

#HOTKEYS
RECORD_KEY = 'f11'
PLAY_KEY = 'f10'
SAVE_KEY = 'f9'
LOAD_KEY = 'f8'
EMERGENCY_STOP = 'f1'
JUMP_KEY = None
HOT_KEYS = [PLAY_KEY, RECORD_KEY, SAVE_KEY, LOAD_KEY, EMERGENCY_STOP]

def record_toggle():
    print('recording')
    # global is_recording
    # global is_playing
    # global input_branches
    # global inputs
    global initial_time

    #check if program is playing
    if states.is_playing:
        print('stop playing before recording')
        return
    
    print('hit f11')
    
    #toggling
    states.is_recording = not states.is_recording

    #let user know the recording state
    if states.is_recording:
        print('program is now recording')
        initial_time = time.time()
    elif len(states.inputs) == 0:
        print('current recording has no inputs')
    else:
        print('program has stopped recording')
        #add inputs to input_branches
        states.input_branches.append(states.inputs)
        print(f'recording #{len(states.input_branches)} saved')
        #now that recording is done erase the inputs
        states.inputs = []


def playback_toggle():
    # global is_recording
    # global is_playing

    #check if program is recording
    if states.is_recording:
        print('stop recording before playing')
        return
    
    print('hit f10')
    #toggling
    states.is_playing = not states.is_playing

    #check if there are recordings available to be played
    if states.is_playing and len(states.input_branches) == 0:
        print('no recordings available')
    #start playback
    elif states.is_playing and len(states.input_branches) != 0:
        print('start')
        threading.Thread(target=playback, daemon=True).start()\

active_keys_playing = []

def playback():
    # global input_branches
    # global is_playing
    global active_keys_playing
    global WAVE_CLEAR_KEY
    skip_delay_time = False

    #loop as long as is_playing is True
    while(states.is_playing):
    #get a random recording
        index = random.randrange(0, len(states.input_branches))
        chosen_inputs = states.input_branches[index]
        #play the recording
        print(f'playing recording #{index + 1}')
        for input in chosen_inputs:
            if keyboard.is_pressed('f1'):
                states.is_playing = False
                print('emergency stop')
            
            if not states.is_playing:
                for active_key in active_keys_playing:
                    keyboard.release(active_key)
                active_keys_playing = []
                print('program has stopped playing')
                return
            
            #edge_prune, if character is going left even though he is at the left most. Skip all futher left commands (Vice versa with right)
            if states.should_edge_prune_left and input.get('name') is not None:
                #stop holding left
                if 'left' in active_keys_playing:
                    keyboard.release('left')
                    active_keys_playing.remove('left')
                    print('pruned left')
                    continue
                #stop any further left actions
                if input['name'] == 'left' or input['name'] == WAVE_CLEAR_KEY:
                    continue
            elif states.should_edge_prune_right and input.get('name') is not None :
                #stop holding right
                if 'right' in active_keys_playing:
                    keyboard.release('right')
                    active_keys_playing.remove('right')
                    print('pruned right')
                    continue
                #stop any further right actions
                if input['name'] == 'right' or input['name'] == WAVE_CLEAR_KEY:
                    continue

            #new logic
            #make sure to get to the correct position
            if input.get('pos'):
                target_pos = input['pos']
                get_to_position(target_pos, input['type'])
                skip_delay_time = True
                continue

            #preserve the time between actions
            if not skip_delay_time:
                time.sleep(variance(input['time_delay'], 30))
            else:
                time.sleep(variance(0.05, 20))
                skip_delay_time = False

            #do action
            if input.get('x'):
                mouse.move(input['x'] + random.randrange(-5,5), input['y']+random.randrange(-5,5))
                mouse.click()
            elif input['type'] == 'down':
                keyboard.press(input['name'])
                if input['name'] not in active_keys_playing:
                    active_keys_playing.append(input['name'])
            elif input['type'] == 'up':
                keyboard.release(input['name'])
                if input['name'] in active_keys_playing:
                    active_keys_playing.remove(input['name'])
            else:
                print('playback error')

def wave_clear(key, rep):
    i = 0
    print('wave clearing')
    while i < rep: 
        print(i)
        time.sleep(variance(0.5, 30))
        keyboard.press(key)
        time.sleep(variance(0.5, 30))
        keyboard.release(key)
        i += 1

def get_to_position(target_pos, type):
    global active_keys_playing
    global WAVE_CLEAR_KEY
    global REP_NUM

    i = 0
    tolerance = 0
    if type == 'general':
        tolerance = 5

    print('traveling')

    while True:
        try:
            if keyboard.is_pressed('f1'):
                states.is_playing = False
                
            if not states.is_playing:
                return
            
            i+=1
            if i == 20:
                if 'left' in active_keys_playing:
                    active_keys_playing.remove('left')
                if 'right' in active_keys_playing:
                    active_keys_playing.remove('right')
                keyboard.release('left')
                keyboard.release('right')
                wave_clear(WAVE_CLEAR_KEY, REP_NUM)
                i = 0

            get_yellow_pos()
            if len(states.yellow_dot) == 0:
                time.sleep(0.1)
                print('cannot find yellow dot')
                continue
            if abs(states.yellow_dot[0] - target_pos[0]) <= tolerance:
                    if 'left' in active_keys_playing:
                        keyboard.release('left')
                        active_keys_playing.remove('left')
                    if 'right' in active_keys_playing:
                        keyboard.release('right')
                        active_keys_playing.remove('right')
                    time.sleep(0.1)
                    #wait a bit to confirm
                    get_yellow_pos()
                    if abs(states.yellow_dot[0] - target_pos[0]) <= tolerance:
                        print('locked on')
                        return
            elif states.yellow_dot[0] < target_pos[0]:
                if 'left' in active_keys_playing:
                    keyboard.release('left')
                    active_keys_playing.remove('left')
                    time.sleep(0.1)
                
                #rope logic
                if type == 'rope':
                    print('rope')
                    keyboard.press('right')
                    time.sleep(0.1 * abs(target_pos[0] - states.yellow_dot[0]))
                    keyboard.press('up')
                    while abs(states.yellow_dot[0] - target_pos[0]) > 5:
                        time.sleep(0.1)
                        get_yellow_pos()
                    keyboard.press(JUMP_KEY)
                    time.sleep(variance(0.1, 30))
                    keyboard.press('up')
                    time.sleep(variance(0.5, (0, 30)))
                    keyboard.release(JUMP_KEY)
                    time.sleep(variance(0.5, 30))
                    keyboard.release('up')
                    time.sleep(variance(1, 30))
                    keyboard.release('right')
                    time.sleep(variance(0.5, 30))
                else:
                    #go right
                    keyboard.press('right')
                    time.sleep(variance(0.02, (0, 15)) * abs(target_pos[0] - states.yellow_dot[0]))
                    keyboard.release('right')
            elif states.yellow_dot[0] > target_pos[0]:
                if 'right' in active_keys_playing:
                    keyboard.release('right')
                    active_keys_playing.remove('right')
                    time.sleep(0.1)

                #rope logic
                if type == 'rope':
                    print('rope')
                    keyboard.press('left')
                    time.sleep(0.1 * abs(target_pos[0] - states.yellow_dot[0]))
                    keyboard.press('up')
                    while abs(states.yellow_dot[0] - target_pos[0]) > 5:
                        time.sleep(0.1)
                        get_yellow_pos()
                    keyboard.press(JUMP_KEY)
                    time.sleep(variance(0.1, 30))
                    keyboard.press('up')
                    time.sleep(variance(0.5, (0, 30)))
                    keyboard.release('up')
                    time.sleep(variance(1, 30))
                    keyboard.release('left')
                    time.sleep(variance(0.5, 30))
                else:
                    #go left
                    keyboard.press('left')
                    time.sleep(variance(0.02, (0, 15)) * abs(states.yellow_dot[0] - target_pos[0]))
                    keyboard.release('left')
        except:
            time.sleep(0.1)
            print('get to error')
            continue

def record_keyboard_input(key):
    global HOT_KEYS
    # global active_keys
    global initial_time


    #do not record the toggle keys
    if key.name in HOT_KEYS:
        return
    
    #recording the key downs
    if not states.is_playing and states.is_recording:
        final_time = time.time()
        elapsed_time = final_time - initial_time
        initial_time = final_time

        #new logic for alt and up
        if states.is_paused and key.name != 'f5':
            print('currently paused, input not recorded')
            pass
        elif key.name == 'f2':
            if key.event_type == 'down':
                get_yellow_pos()
                states.inputs.append({
                    'pos': states.yellow_dot,
                    'type': 'precise'
                })
        elif key.name == 'f3':
            if key.event_type == 'down':
                get_yellow_pos()
                states.inputs.append({
                    'pos': states.yellow_dot,
                    'type': 'general'
                })
        elif key.name == 'f4':
            if key.event_type == 'down':
                get_yellow_pos()
                states.inputs.append({
                    'pos': states.yellow_dot,
                    'type': 'rope'
                })
        elif key.name == 'f5':
            if key.event_type == 'down':
                states.is_paused = not states.is_paused
                if states.is_paused:
                    print('recording is currently paused')
                else:
                    print('recording resumed')
        else:
            states.inputs.append({
                'name': key.name,
                'type': key.event_type,
                'time_delay': elapsed_time
            })

def record_mouse_input():
    global initial_time
    mouse_pos = mouse.get_position()
    if not states.is_playing and states.is_recording:
        final_time = time.time()
        elapsed_time = final_time - initial_time
        initial_time = final_time
        states.inputs.append({
            'x': mouse_pos[0],
            'y': mouse_pos[1],
            'time_delay': elapsed_time
        })
    

def save():
    # global input_branches

    if len(states.input_branches) == 0:
        print('There are no recordings to save right now')
    elif states.is_recording:
        print('Stop recording to save')
    else:
        with open(os.path.abspath(os.path.join('recordings', 'active.json')), 'w') as f:
            json.dump(states.input_branches, f, indent=4)
        print('Recorded to active.json file')

load_index = 0

def load():
    # global input_branches
    # global is_playing
    # global is_recording
    global load_index
    active_recordings = []

    if states.is_playing or states.is_recording:
        print('stop playing and recording to load')
        return
    
    try:
        recordings = os.listdir('recordings')
        file = None
        for recording in recordings:
            if recording.startswith('active'):
                active_recordings.append(recording)

        file = active_recordings[load_index]
        with open(os.path.abspath(os.path.join('recordings', file)), 'r') as f:
            states.input_branches = json.load(f)
            print(file + ' loaded')
        load_index = (load_index + 1) % len(active_recordings)
    except Exception as e:
        print(e)


WAVE_CLEAR_KEY = None
REP_NUM = 0

def macro():
    global WAVE_CLEAR_KEY
    global REP_NUM
    global JUMP_KEY

    settings = states.settings
    if settings.get('wave_clear_key'):
        WAVE_CLEAR_KEY = settings["wave_clear_key"]
    else:
        print('What is your wave clear key?')
        while WAVE_CLEAR_KEY == 'enter' or WAVE_CLEAR_KEY is None:
            time.sleep(0.1)
            settings["wave_clear_key"] = keyboard.read_key()
            WAVE_CLEAR_KEY = settings["wave_clear_key"]
    print(f'Your wave clear key is {WAVE_CLEAR_KEY}')
    
    if settings.get('rep_num'):
        REP_NUM = settings['rep_num']
    else:
        settings['rep_num'] = int(input('How many times would you like to repeat this wave clear?\n'))
        REP_NUM = settings['rep_num']

    print('What is your jump key?')
    if settings.get('jump_key'):
        JUMP_KEY = settings["jump_key"]
    else:
        while JUMP_KEY == 'enter' or JUMP_KEY is None:
            time.sleep(0.1)
            settings["jump_key"] = keyboard.read_key()
            JUMP_KEY = settings["jump_key"]
    print(f'Your jump key is {JUMP_KEY}')
    
    #greeting
    print('Welcome to BotStory')
    print('F12 to exit program')
    print('F11 to start/end recording')
    print('F10 to play recording')
    print('F9 to save recording')
    print('F8 to load recording')
    print('F1 emergency stop')

    # #record
    # keyboard.add_hotkey(RECORD_KEY, record_toggle)
    # #playback
    # keyboard.add_hotkey(PLAY_KEY, playback_toggle)
    # #save
    # keyboard.add_hotkey(SAVE_KEY, save)
    # #load
    # keyboard.add_hotkey(LOAD_KEY, load)
    #detect keyboard inputs
    keyboard.hook(record_keyboard_input)
    #detect mouse Inputs
    mouse.on_click(record_mouse_input)

    #detect yellow dot
    keyboard.add_hotkey('f5', get_yellow_pos)

def get_yellow_pos():
    found_yellow = False
    minimap.get_mini_map()

    for x in range(0, states.mini_map.width):
        if found_yellow:
            break
        for y in range(states.mini_map.height, 0, -1):
            if found_yellow:
                break
            temp_yellow_dot = minimap.get_yellow_dot(x, y, states.mini_map)
            if temp_yellow_dot:
                states.yellow_dot = temp_yellow_dot
                found_yellow = True