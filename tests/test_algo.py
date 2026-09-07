import json

coords = [
    [40.08903, 32.993209],
    [40.08958, 32.993349],
    [40.090023, 32.993488],
    [40.089859, 32.99616],
    [40.088677, 32.996085],
    [40.087963, 32.995816],
    [40.088661, 32.994325],
    [40.08903, 32.993209]
]

step_meters = 25
lat_step = step_meters / 111111.0

min_lat = min(p[0] for p in coords)
max_lat = max(p[0] for p in coords)

print(f"min_lat: {min_lat}, max_lat: {max_lat}, lat_step: {lat_step}")

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

print(f"Generated {len(new_waypoints)} waypoints")
print(new_waypoints[:5])
