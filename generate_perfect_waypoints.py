waypoints = []
# P157 is from lat 40.2100 down to 40.2095
lats = [40.2100, 40.2099, 40.2098, 40.2097, 40.2096, 40.2095]
right_lon = 33.0101 # Right edge is straight

# Left edge is slanted: at 40.2099 it's 33.0077, at 40.2094 it's 33.0081
def get_left_lon(lat):
    # Linear interpolation
    # lat 40.2099 -> lon 33.0077
    # lat 40.2094 -> lon 33.0081
    # slope = (33.0081 - 33.0077) / (40.2094 - 40.2099) = 0.0004 / -0.0005 = -0.8
    return 33.0077 + (40.2099 - lat) * 0.8

for i in range(len(lats)):
    lat = lats[i]
    left_lon = get_left_lon(lat)
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
print("Perfect waypoints generated.")
