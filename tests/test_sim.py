import sys
import unittest.mock as mock
sys.modules['serial'] = mock.Mock()
sys.modules['pynmea2'] = mock.Mock()

sys.path.append('.')
from src.data.gps_reader import GPSReader
import time

reader = GPSReader(simulated=True)
coords = [[40.08903, 32.993209], [40.08958, 32.993349], [40.090023, 32.993488], [40.089859, 32.99616], [40.088677, 32.996085], [40.087963, 32.995816], [40.088661, 32.994325], [40.08903, 32.993209]]

#reader.set_waypoints_from_polygon(coords)
print(f"Waypoints: {len(reader.waypoints)}")
print(f"Start: {reader.waypoints[0]}")

for i in range(20):
    reader._generate_fake_data()
    data = reader.current_data
    print(f"Tick {i}: lat={data['lat'] if isinstance(data, dict) else data.lat}, lon={data['lon'] if isinstance(data, dict) else data.lon}, idx={reader.sim_state['target_idx']}")
