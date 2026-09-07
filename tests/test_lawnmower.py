def generate_lawnmower_path(coords, step_meters=10):
    # coords = [[lat, lon], [lat, lon], ...]
    if not coords or len(coords) < 3:
        return coords
        
    lat_step = step_meters / 111111.0
    
    min_lat = min(p[0] for p in coords)
    max_lat = max(p[0] for p in coords)
    
    waypoints = []
    
    current_lat = min_lat + lat_step/2
    direction = 1 # 1 for right, -1 for left
    
    while current_lat < max_lat:
        intersections = []
        for i in range(len(coords)):
            p1 = coords[i]
            p2 = coords[(i+1)%len(coords)]
            
            # Check if line segment intersects the current latitude line
            if min(p1[0], p2[0]) < current_lat <= max(p1[0], p2[0]):
                if p2[0] != p1[0]:
                    lon = p1[1] + (current_lat - p1[0]) * (p2[1] - p1[1]) / (p2[0] - p1[0])
                    intersections.append(lon)
        
        intersections.sort()
        # Pair up intersections
        for i in range(0, len(intersections)-1, 2):
            lon1 = intersections[i]
            lon2 = intersections[i+1]
            
            if direction == 1:
                waypoints.append([current_lat, lon1])
                waypoints.append([current_lat, lon2])
            else:
                waypoints.append([current_lat, lon2])
                waypoints.append([current_lat, lon1])
                
        direction *= -1
        current_lat += lat_step
        
    return waypoints if waypoints else coords

# Test with a simple square
coords = [[0, 0], [0, 0.001], [0.001, 0.001], [0.001, 0]]
path = generate_lawnmower_path(coords, step_meters=20)
print(len(path), "waypoints generated")
print(path[:4])
