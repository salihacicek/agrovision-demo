import json
import sys
import unittest.mock as mock
sys.modules['serial'] = mock.Mock()
sys.modules['pynmea2'] = mock.Mock()
sys.path.append('.')
from src.data.gps_reader import GPSReader

data = json.load(open('src/dashboard/static/assets/data/parseller.json'))
p1789 = next(f for f in data['features'] if f['properties']['parsel_id'] == 'P1789')
coords = [[c[1], c[0]] for c in p1789['geometry']['coordinates'][0]]

reader = GPSReader(simulated=True)
reader.set_waypoints_from_polygon(coords)
wp0 = reader.waypoints[0]
print(f"Waypoint 0: {wp0}")
min_lon = min(p[1] for p in coords)
max_lon = max(p[1] for p in coords)
print(f"min_lon: {min_lon}, max_lon: {max_lon}")
print(f"wp0_lon: {wp0[1]}")
print(f"Distance from min_lon: {wp0[1] - min_lon}")
print(f"Distance from max_lon: {max_lon - wp0[1]}")
