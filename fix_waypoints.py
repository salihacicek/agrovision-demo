import re

with open('/Users/salihacicek/Desktop/bugdaymisir/src/data/gps_reader.py', 'r') as f:
    content = f.read()

# Find the WAYPOINTS array
import ast

# Extract the waypoints string
start_idx = content.find('WAYPOINTS = [')
end_idx = content.find(']', start_idx) + 1
waypoints_str = content[start_idx:end_idx]

# Safely evaluate it (ignoring the WAYPOINTS = part)
arr_str = waypoints_str.split('=', 1)[1].strip()
waypoints = ast.literal_eval(arr_str)

# Modify waypoints
new_waypoints = []
for lat, lon in waypoints:
    if lon < 33.0080:
        lon = 33.0080
    new_waypoints.append((lat, lon))

# Format back to string
new_arr_str = "[\n"
for i in range(0, len(new_waypoints), 2):
    if i+1 < len(new_waypoints):
        new_arr_str += f"            ({new_waypoints[i][0]:.6f}, {new_waypoints[i][1]:.6f}), ({new_waypoints[i+1][0]:.6f}, {new_waypoints[i+1][1]:.6f}),\n"
    else:
        new_arr_str += f"            ({new_waypoints[i][0]:.6f}, {new_waypoints[i][1]:.6f}),\n"
new_arr_str += "        ]"

new_content = content[:start_idx] + "WAYPOINTS = " + new_arr_str + content[end_idx:]

with open('/Users/salihacicek/Desktop/bugdaymisir/src/data/gps_reader.py', 'w') as f:
    f.write(new_content)
print("Waypoints updated.")
