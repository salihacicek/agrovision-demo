import re

with open('/Users/salihacicek/Desktop/bugdaymisir/src/data/gps_reader.py', 'r') as f:
    content = f.read()

# Fix WAYPOINTS to self.waypoints
content = content.replace("WAYPOINTS[", "self.waypoints[")

# The bad injection is in set_waypoints_from_polygon:
bad_code = """
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
# We just replace the bad code with "        self.is_paused = False"
content = content.replace(bad_code, "\n        self.is_paused = False\n")

# Now check if __init__ has self.waypoints. If not, add it.
if "self.waypoints =" not in content[:content.find('def set_waypoints')]:
    init_end = content.find("self.is_paused = False") + len("self.is_paused = False")
    content = content[:init_end] + "\n        self.waypoints = [\n            (40.210050, 33.010100), (40.209850, 33.007750),\n            (40.209775, 33.007825), (40.209975, 33.010100),\n            (40.209900, 33.010100), (40.209700, 33.007900),\n            (40.209625, 33.007975), (40.209825, 33.010100),\n            (40.209750, 33.010100), (40.209550, 33.008050),\n            (40.209475, 33.008125), (40.209675, 33.010100),\n        ]\n" + content[init_end:]

with open('/Users/salihacicek/Desktop/bugdaymisir/src/data/gps_reader.py', 'w') as f:
    f.write(content)
print("Fixed.")
