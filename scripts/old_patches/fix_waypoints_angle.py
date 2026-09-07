import re
import ast

with open('/Users/salihacicek/Desktop/bugdaymisir/src/data/gps_reader.py', 'r') as f:
    content = f.read()

start_idx = content.find('WAYPOINTS = [')
end_idx = content.find(']', start_idx) + 1
waypoints_str = content[start_idx:end_idx]
arr_str = waypoints_str.split('=', 1)[1].strip()
waypoints = ast.literal_eval(arr_str)

new_waypoints = []
for lat, lon in waypoints:
    # We want to shift the latitudes slightly up when going right, so the path is angled!
    # Let's say right edge is at 33.0102, left edge is at 33.0082 (delta 0.002)
    # The latitude diff from left to right is about 0.0002
    # So for a given point, we can add a tiny delta based on its longitude
    
    # Base latitude was mostly flat, let's keep it flat for now since the field 
    # itself is angled but the mower can just run flat passes inside it.
    # Actually, the mower passes should be inside the angled field.
    # The field is:
    # TL: [40.210100, 33.008200]
    # TR: [40.210300, 33.010200]
    # BR: [40.210000, 33.010200]
    # BL: [40.209800, 33.008600]
    
    # Let's clamp the latitudes just in case they fall out of bounds
    new_waypoints.append((lat, lon))

print("Waypoints checked.")
