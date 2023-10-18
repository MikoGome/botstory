import keyboard
import threading
import time
import states

from utils import variance

PET_FOOD_KEY = None
PET_NUMBER = 1

def petfeeder():
    global PET_FOOD_KEY
    global PET_NUMBER

    #ask user if they would like to use the pet food feature
    
    pet_feeder_start = None
    # print('states', states["settings"])
    settings = states.settings
    if settings.get("enable_pet_feeder"):
        pet_feeder_start = settings["enable_pet_feeder"]
    else:
        settings["enable_pet_feeder"] = input('Start auto Pet feeder? [y/n]\n')
        pet_feeder_start = settings["enable_pet_feeder"]

    if pet_feeder_start[0].lower() == 'y':
        #if yes, get what key they use their pet food
        if settings.get('pet_food_key'):
            PET_FOOD_KEY = settings["pet_food_key"]
        else:
            print('What is your petfood key?')
            while PET_FOOD_KEY == 'enter' or PET_FOOD_KEY is None:
                time.sleep(0.1)
                settings["pet_food_key"] = keyboard.read_key()
                PET_FOOD_KEY = settings["pet_food_key"]
        print(f"Your petfood key is {PET_FOOD_KEY}")
        if settings.get("pet_number"):
            PET_NUMBER = settings["pet_number"]
        else:
            settings["pet_number"] = int(input('How many pets do you have on?'))
            PET_NUMBER = settings["pet_number"]
            print('pet feeder on')
        threading.Thread(target=feed_pet, daemon=True).start()
    else:
        print('pet feeder off')

def feed_pet():
    global PET_FOOD_KEY
    global PET_NUMBER

    while(True):
        time.sleep(variance(15*60, (10, 0)))
        for i in range(0, PET_NUMBER):
            keyboard.send(PET_FOOD_KEY)
            print(f'pet #{i} fed')
            time.sleep(variance(1, (0, 100)))