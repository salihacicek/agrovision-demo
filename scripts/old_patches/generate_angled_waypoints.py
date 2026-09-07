waypoints = []

# f goes from 0.1 to 0.9 in steps of 0.15
fs = [0.1, 0.25, 0.4, 0.55, 0.7, 0.85]

for i, f in enumerate(fs):
    left_lat = 40.2099 + f * (40.2094 - 40.2099)
    left_lon = 33.0076 + f * (33.0081 - 33.0076)
    
    right_lat = 40.2101 + f * (40.2096 - 40.2101)
    right_lon = 33.0102
    
    # Add a tiny margin so it doesn't touch the exact edges
    left_lon += 0.0001
    right_lon -= 0.0001
    
    if i % 2 == 0:
        # Right to Left
        waypoints.append((right_lat, right_lon))
        waypoints.append((left_lat, left_lon))
    else:
        # Left to Right
        waypoints.append((left_lat, left_lon))
        waypoints.append((right_lat, right_lon))

with open('/Users/salihacicek/Desktop/bugdaymisir/src/data/gps_reader.py', 'r') as f:
    content = f.read()

start_idx = content.find('WAYPOINTS = [')
end_idx = content.find(']', start_idx) + 1

new_arr_str = "[\n"
for i in range(0, len(waypoints), 2):
    if i+1 < len(waypoints):
        new_arr_str += f"            ({waypoints[i][0]:.6f}, {waypoints[i][1]:.6f}), ({waypoints[i+1][0]:.6f}, {waypoints[i+1][1]:.6f}),\n"
    else:
        new_arr_str += f"            ({waypoints[i][0]:.6f}, {waypoints[i][1]:.6f}),\n"
new_arr_str += "        ]"

new_content = content[:start_idx] + "WAYPOINTS = " + new_arr_str + content[end_idx:]

with open('/Users/salihacicek/Desktop/bugdaymisir/src/data/gps_reader.py', 'w') as f:
    f.write(new_content)
print("Angled waypoints generated.")
