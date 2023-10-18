import json
import states
import os

def initialize():
    try:
        with open(os.path.abspath(os.path.join("settings.json"))) as f:
            states.settings = json.load(f)
    except:
        print('Please initialize your settings')

def save():
    with open(os.path.abspath(os.path.join("settings.json")), 'w') as f:
        json.dump(states.settings, f, indent=4)

if __name__ == '__main__':
    initialize()