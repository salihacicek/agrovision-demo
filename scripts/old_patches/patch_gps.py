import re

with open("src/data/gps_reader.py", "r") as f:
    content = f.read()

new_func = '''    def set_waypoints_from_polygon(self, coords):
        """Dinamik olarak parsel poligonunun içini zikzak (lawnmower) şeklinde tarar."""
        if not coords or len(coords) < 3:
            return False
            
        step_meters = 15  # 15 metre aralıklarla tarama (traktör genişliği)
        lat_step = step_meters / 111111.0
        
        min_lat = min(p[0] for p in coords)
        max_lat = max(p[0] for p in coords)
        
        new_waypoints = []
        current_lat = min_lat + lat_step/2
        direction = 1
        
        while current_lat < max_lat:
            intersections = []
            for i in range(len(coords)):
                p1 = coords[i]
                p2 = coords[(i+1)%len(coords)]
                if min(p1[0], p2[0]) < current_lat <= max(p1[0], p2[0]):
                    if p2[0] != p1[0]:
                        lon = p1[1] + (current_lat - p1[0]) * (p2[1] - p1[1]) / (p2[0] - p1[0])
                        intersections.append(lon)
            
            intersections.sort()
            for i in range(0, len(intersections)-1, 2):
                lon1 = intersections[i]
                lon2 = intersections[i+1]
                if direction == 1:
                    new_waypoints.append([current_lat, lon1])
                    new_waypoints.append([current_lat, lon2])
                else:
                    new_waypoints.append([current_lat, lon2])
                    new_waypoints.append([current_lat, lon1])
                    
            direction *= -1
            current_lat += lat_step
            
        if not new_waypoints:
            new_waypoints = coords
                
        with self._lock:'''

old_func_pattern = r'    def set_waypoints_from_polygon\(self, coords\):.*?        with self\._lock:'

new_content = re.sub(old_func_pattern, new_func, content, flags=re.DOTALL)

with open("src/data/gps_reader.py", "w") as f:
    f.write(new_content)
