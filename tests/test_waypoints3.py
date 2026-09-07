import json
import math
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

for i in range(0, 10, 2):
    wp1 = reader.waypoints[i]
    wp2 = reader.waypoints[i+1]
    length_deg = abs(wp1[0] - wp2[0])
    length_m = length_deg * 111111.0
    print(f"Line {i//2}: lon={wp1[1]:.6f}, length={length_m:.1f} meters")
