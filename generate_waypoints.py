waypoints = []
lats = [40.21000, 40.20995, 40.20990, 40.20985, 40.20980, 40.20975, 40.20970, 40.20965]
right_lon = 33.0101
left_lons = [33.0079, 33.0080, 33.0080, 33.0081, 33.0081, 33.0082, 33.0082, 33.0083]

for i in range(len(lats)):
    lat = lats[i]
    left_lon = left_lons[i]
    if i % 2 == 0:
        # Move left
        waypoints.append((lat, right_lon))
        waypoints.append((lat, left_lon))
    else:
        # Move right
        waypoints.append((lat, left_lon))
        waypoints.append((lat, right_lon))

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
print("Waypoints fully replaced.")
