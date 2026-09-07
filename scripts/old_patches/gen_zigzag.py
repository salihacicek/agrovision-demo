import math

# The 6-point polygon
pts = [
    (39.7608, 32.4248),
    (39.7612, 32.4272),
    (39.7602, 32.4270),
    (39.7597, 32.4260),
    (39.7598, 32.4250),
    (39.7603, 32.4246)
]

# Find bounding box
max_lat = max(p[0] for p in pts) - 0.00005 # start slightly inside
min_lat = min(p[0] for p in pts) + 0.00005

def get_intersections(lat):
    intersections = []
    for i in range(len(pts)):
        p1 = pts[i]
        p2 = pts[(i+1) % len(pts)]
        # Check if lat is between p1[0] and p2[0]
        if (p1[0] <= lat and p2[0] > lat) or (p2[0] <= lat and p1[0] > lat):
            # linear interpolation to find lon
            t = (lat - p1[0]) / (p2[0] - p1[0])
            lon = p1[1] + t * (p2[1] - p1[1])
            intersections.append(lon)
    return sorted(intersections)

row_step = 0.00006 # roughly 6.6 meters
lat = max_lat
waypoints = []
direction = 'east'

while lat > min_lat:
    xs = get_intersections(lat)
    if len(xs) >= 2:
        left_lon = xs[0] + 0.00002 # slightly inside
        right_lon = xs[-1] - 0.00002
        
        if direction == 'east':
            waypoints.append((lat, left_lon))
            waypoints.append((lat, right_lon))
            direction = 'west'
        else:
            waypoints.append((lat, right_lon))
            waypoints.append((lat, left_lon))
            direction = 'east'
            
    lat -= row_step

print("WAYPOINTS = [")
for wp in waypoints:
    print(f"    ({wp[0]:.6f}, {wp[1]:.6f}),")
print("]")
