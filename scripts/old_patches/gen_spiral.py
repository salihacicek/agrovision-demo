import math

pts = [
    (39.7608, 32.4248),
    (39.7612, 32.4272),
    (39.7602, 32.4270),
    (39.7597, 32.4260),
    (39.7598, 32.4250),
    (39.7603, 32.4246)
]

c_lat = sum(p[0] for p in pts) / len(pts)
c_lon = sum(p[1] for p in pts) / len(pts)

waypoints = []
scales = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
for s in scales:
    ring = []
    for p in pts:
        lat = c_lat + s * (p[0] - c_lat)
        lon = c_lon + s * (p[1] - c_lon)
        ring.append((lat, lon))
    waypoints.extend(ring)

print("WAYPOINTS = [")
for wp in waypoints:
    print(f"    ({wp[0]:.6f}, {wp[1]:.6f}),")
print("]")
