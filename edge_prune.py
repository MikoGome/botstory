import states
import minimap
from PIL import ImageGrab
import time
import threading

def initialize():
    threading.Thread(target=scan_edges, daemon=True).start()

def scan_edges():
    while True:
        time.sleep(0.1)
        monitor_edges()

def monitor_edges():
    if grab_left_mini_map_edge():
        states.should_edge_prune_left = True
    elif grab_right_mini_map_edge():
        states.should_edge_prune_right = True
    else:
        states.should_edge_prune_left = False
        states.should_edge_prune_right = False
    

def grab_left_mini_map_edge():
    edge_cut = 1
    left_x = states.mini_map_coords[0]
    initial_y = states.mini_map_coords[1]
    final_y = states.mini_map_coords[3]
    yellow_dot_width = 5
    left_edge_image = ImageGrab.grab(bbox=(left_x + edge_cut, initial_y, left_x + yellow_dot_width + edge_cut + 1, final_y))

    for x in range(0, left_edge_image.width):
        for y in range(left_edge_image.height, 0, -1):
            if minimap.get_yellow_dot(x, y, left_edge_image):
                return True
    return False

def grab_right_mini_map_edge():
    edge_cut = 1
    right_x = states.mini_map_coords[2]
    initial_y = states.mini_map_coords[1]
    final_y = states.mini_map_coords[3]
    yellow_dot_width = 5
    right_edge_image = ImageGrab.grab(bbox=(right_x - yellow_dot_width - edge_cut - 2, initial_y, right_x - edge_cut - 1, final_y))

    for x in range(0, right_edge_image.width):
        for y in range(right_edge_image.height, 0, -1):
            if minimap.get_yellow_dot(x, y, right_edge_image):
                return True
    return False