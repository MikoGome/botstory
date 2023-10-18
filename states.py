#STATES
input_branches = []
inputs = []
is_recording = False
is_playing = False
is_paused = False

#VISION
vision_on = False
portals = []
yellow_dot = ()
red_dots = []
mini_map = None
warning_mode_on = False
portal_guard_on = False

#VISION_COORDS
mini_map_coords = ()
window = ()

#autopot
auto_hp_on = False
auto_mp_on = False

#HP_COORDS (x, y, w, h)
HP_COORD = (223, 782, 223 + 105, 782 + 0)

#MP_COORDS (x, y, w, h)
MP_COORD = (331, 782, 331 + 105, 782 + 0)

#EDGE_PRUNE
should_edge_prune_left = False
should_edge_prune_right = False

#settings
settings = {}