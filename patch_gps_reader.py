import re

with open('/Users/salihacicek/Desktop/bugdaymisir/src/data/gps_reader.py', 'r') as f:
    content = f.read()

# Add set_waypoints_from_polygon method
new_method = """
    def set_waypoints_from_polygon(self, coords):
        \"\"\"Dinamik olarak parsel poligonundan çapraz waypointler hesaplar.\"\"\"
        if not coords or len(coords) != 4:
            return False
            
        tl, tr, br, bl = coords
        
        height = tl[0] - bl[0]
        # Eğer çok küçükse en az 4 tur at, büyükse daha fazla
        num_passes = max(4, int(height / 0.0001))
        
        new_waypoints = []
        for i in range(num_passes):
            f = i / max(1, (num_passes - 1))
            
            # Sol kenar (TL'den BL'ye)
            left_lat = tl[0] + f * (bl[0] - tl[0])
            left_lon = tl[1] + f * (bl[1] - tl[1])
            
            # Sağ kenar (TR'den BR'ye)
            right_lat = tr[0] + f * (br[0] - tr[0])
            right_lon = tr[1] + f * (br[1] - tr[1])
            
            # Kenarlara tam değmemesi için hafif içe çekelim
            lon_margin = abs(right_lon - left_lon) * 0.05
            if left_lon < right_lon:
                left_lon += lon_margin
                right_lon -= lon_margin
            else:
                left_lon -= lon_margin
                right_lon += lon_margin
                
            if i % 2 == 0:
                new_waypoints.append((right_lat, right_lon))
                new_waypoints.append((left_lat, left_lon))
            else:
                new_waypoints.append((left_lat, left_lon))
                new_waypoints.append((right_lat, right_lon))
                
        with self._lock:
            self.waypoints = new_waypoints
            self.sim_state = {
                'lat': self.waypoints[0][0],
                'lon': self.waypoints[0][1],
                'target_idx': 1,
                'speed_timer': 0,
                'current_speed': 6.0
            }
            self.is_paused = False
        return True

    def _generate_fake_data(self):"""

content = content.replace("    def _generate_fake_data(self):", new_method)

# Remove the hardcoded WAYPOINTS local variable from _generate_fake_data
pattern = r"WAYPOINTS\s*=\s*\[(.*?)\]\s*with self\._lock:"
# Wait, this is multi-line. Let's use regex
content = re.sub(r'WAYPOINTS = \[\s*.*?\s*\]\s*with self\._lock:', 'with self._lock:', content, flags=re.DOTALL)

# Replace WAYPOINTS with self.waypoints
content = content.replace("WAYPOINTS[0][0]", "self.waypoints[0][0]")
content = content.replace("WAYPOINTS[0][1]", "self.waypoints[0][1]")
content = content.replace("len(WAYPOINTS)", "len(self.waypoints)")
content = content.replace("WAYPOINTS[target]", "self.waypoints[target]")

# Add self.waypoints to __init__
init_code = """
        self.last_lon = None
        self.is_paused = False
        
        # Varsayılan (P157)
        self.waypoints = [
            (40.210050, 33.010100), (40.209850, 33.007750),
            (40.209775, 33.007825), (40.209975, 33.010100),
            (40.209900, 33.010100), (40.209700, 33.007900),
            (40.209625, 33.007975), (40.209825, 33.010100),
            (40.209750, 33.010100), (40.209550, 33.008050),
            (40.209475, 33.008125), (40.209675, 33.010100),
        ]
"""
content = content.replace("        self.is_paused = False", init_code)

with open('/Users/salihacicek/Desktop/bugdaymisir/src/data/gps_reader.py', 'w') as f:
    f.write(content)
print("gps_reader.py updated.")
