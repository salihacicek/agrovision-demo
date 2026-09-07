import re

with open('src/data/gps_reader.py', 'r') as f:
    content = f.read()

old_init = """        self.last_lat = None
        self.last_lon = None
        default_coords = [[40.088029, 32.992823], [40.086806, 32.995559], [40.086264, 32.995076], [40.086953, 32.993553], [40.087241, 32.992898], [40.087405, 32.992415], [40.088029, 32.992823]]
        self.waypoints = [default_coords[0]]
        self.is_paused = False
        self.set_waypoints_from_polygon(default_coords)"""

new_init = """        self.last_lat = None
        self.last_lon = None
        self.waypoints = []
        self.is_paused = True
        self.sim_state = {
            'lat': 40.0880,
            'lon': 32.9950,
            'target_idx': 0,
            'speed_timer': 0,
            'current_speed': 0.0
        }"""

content = content.replace(old_init, new_init)

with open('src/data/gps_reader.py', 'w') as f:
    f.write(content)
