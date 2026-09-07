def generate_waypoints_for_polygon(coords):
    # coords is a list of [lat, lon] in order: TL, TR, BR, BL
    # Wait, in main.js, the order is:
    # TL, TR, BR, BL
    tl, tr, br, bl = coords
    
    # We want horizontal passes from top to bottom
    # Number of passes = approx 1 pass per 0.0001 lat
    height = tl[0] - bl[0]
    num_passes = max(4, int(height / 0.00008))
    
    waypoints = []
    
    for i in range(num_passes):
        f = i / max(1, (num_passes - 1))
        
        # Left edge is line from TL to BL
        left_lat = tl[0] + f * (bl[0] - tl[0])
        left_lon = tl[1] + f * (bl[1] - tl[1])
        
        # Right edge is line from TR to BR
        right_lat = tr[0] + f * (br[0] - tr[0])
        right_lon = tr[1] + f * (br[1] - tr[1])
        
        # Inset slightly
        lon_margin = abs(right_lon - left_lon) * 0.05 # 5% margin
        
        if left_lon < right_lon:
            left_lon += lon_margin
            right_lon -= lon_margin
        else:
            left_lon -= lon_margin
            right_lon += lon_margin
            
        if i % 2 == 0:
            # Right to Left (Wait, let's just alternate)
            waypoints.append((right_lat, right_lon))
            waypoints.append((left_lat, left_lon))
        else:
            waypoints.append((left_lat, left_lon))
            waypoints.append((right_lat, right_lon))
            
    return waypoints

coords = [
    [40.210100, 33.007800], # TL
    [40.210300, 33.010200], // TR
    [40.210000, 33.010200], // BR
    [40.209800, 33.008600]  // BL
]

for w in generate_waypoints_for_polygon(coords):
    print(w)
