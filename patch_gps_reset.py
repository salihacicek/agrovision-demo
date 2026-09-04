import re

with open('src/data/gps_reader.py', 'r') as f:
    content = f.read()

old_block = """                self.last_lat = self.sim_state['lat']
                self.last_lon = self.sim_state['lon']
                self.current_data.lat = self.sim_state['lat']"""

new_block = """                self.last_lat = self.sim_state['lat']
                self.last_lon = self.sim_state['lon']
                self.current_data.lat = self.sim_state['lat']
                self.total_distance_m = 0.0
                self.visited_polygons = []"""

content = content.replace(old_block, new_block)

with open('src/data/gps_reader.py', 'w') as f:
    f.write(content)
