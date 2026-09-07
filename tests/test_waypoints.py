import sys
import unittest.mock as mock
sys.modules['serial'] = mock.Mock()
sys.modules['pynmea2'] = mock.Mock()

sys.path.append('.')
from src.data.gps_reader import GPSReader

reader = GPSReader(simulated=True)
print("Waypoints:")
for i, wp in enumerate(reader.waypoints[:5]):
    print(f"{i}: {wp}")
