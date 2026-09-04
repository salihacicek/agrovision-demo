import serial
import pynmea2
import threading
import time
import random
import math
from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class GPSData:
    """GPS verisini tutan sınıf."""
    lat: Optional[float] = None
    lon: Optional[float] = None
    altitude: Optional[float] = None
    speed_knots: Optional[float] = None
    heading_true: Optional[float] = None
    satellites: int = 0
    quality: int = 0
    timestamp: Optional[Any] = None
    total_distance_m: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "lat": self.lat,
            "lon": self.lon,
            "altitude": self.altitude,
            "speed_knots": self.speed_knots,
            "heading_true": self.heading_true,
            "satellites": self.satellites,
            "quality": self.quality,
            "timestamp": str(self.timestamp) if self.timestamp else None,
            "total_distance_m": self.total_distance_m
        }

def calculate_haversine(lat1, lon1, lat2, lon2):
    """İki koordinat arasındaki mesafeyi metre cinsinden hesaplar."""
    if None in (lat1, lon1, lat2, lon2):
        return 0.0
    R = 6371000  # Dünya yarıçapı (metre)
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi/2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2.0)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

class GPSReader:
    """NMEA cümlelerini parse eden geliştirilmiş GPS okuyucu."""
    
    def __init__(self, port: str = "/dev/ttyUSB0", baudrate: int = 9600, simulated: bool = False):
        self.port = port
        self.baudrate = baudrate
        self.simulated = simulated
        self.current_data = GPSData()
        self._lock = threading.Lock()
        self.running = False
        self._thread = None
        self.serial_conn = None
        self.last_lat = None
        self.last_lon = None

        self.is_paused = False
        self.waypoints = [
            (40.0880, 32.9950)
        ]



    def reset_distance(self):
        """Toplanan mesafeyi sıfırlar."""
        with self._lock:
            self.current_data.total_distance_m = 0.0
            self.last_lat = None
            self.last_lon = None

    def start(self):
        """GPS okuma döngüsünü başlatır."""
        if self.running:
            return
        
        self.running = True
        if not self.simulated:
            try:
                self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=1)
            except serial.SerialException as e:
                print(f"GPS bağlantı hatası: {e}. Simülasyon moduna geçiliyor.")
                self.simulated = True

        self._thread = threading.Thread(target=self._read_loop, daemon=True)
        self._thread.start()

    def stop(self):
        """GPS okumayı durdurur."""
        self.running = False
        if self._thread:
            self._thread.join()
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()

    def _read_loop(self):
        """Arka planda çalışan okuma döngüsü."""
        while self.running:
            if self.is_paused:
                time.sleep(1)
                continue

            if self.simulated:
                self._generate_fake_data()
                time.sleep(0.1) # 10 FPS
                continue

            try:
                if self.serial_conn.in_waiting > 0:
                    line = self.serial_conn.readline().decode('ascii', errors='replace').strip()
                    self._parse_nmea(line)
            except Exception as e:
                print(f"GPS okuma hatası: {e}")
                time.sleep(1)

    def _parse_nmea(self, line: str):
        """NMEA GGA, RMC, VTG formatlarını işler."""
        try:
            if line.startswith('$GPGGA') or line.startswith('$GNGGA'):
                msg = pynmea2.parse(line)
                with self._lock:
                    if self.last_lat is not None and self.last_lon is not None:
                        dist = calculate_haversine(self.last_lat, self.last_lon, msg.latitude, msg.longitude)
                        if dist > 0.5: # Sadece 0.5 metreden büyük değişimleri say (titremeyi önle)
                            self.current_data.total_distance_m += dist
                    self.last_lat = msg.latitude
                    self.last_lon = msg.longitude
                    
                    self.current_data.lat = msg.latitude
                    self.current_data.lon = msg.longitude
                    self.current_data.altitude = getattr(msg, 'altitude', None)
                    self.current_data.satellites = getattr(msg, 'num_sats', 0)
                    self.current_data.quality = getattr(msg, 'gps_qual', 0)
                    self.current_data.timestamp = getattr(msg, 'timestamp', None)
            
            elif line.startswith('$GPRMC') or line.startswith('$GNRMC'):
                msg = pynmea2.parse(line)
                with self._lock:
                    self.current_data.lat = msg.latitude
                    self.current_data.lon = msg.longitude
                    self.current_data.speed_knots = getattr(msg, 'spd_over_grnd', None)
                    self.current_data.heading_true = getattr(msg, 'true_course', None)
                    
        except pynmea2.ParseError:
            pass


    def set_waypoints_from_polygon(self, coords):
        """Dinamik olarak parsel poligonunun içini zikzak (lawnmower) şeklinde tarar."""
        if not coords or len(coords) < 3:
            return False
            
        step_meters = 25  # 25 metre aralıklarla tarama (traktör genişliği)
        lat_step = step_meters / 111111.0
        
        min_lat = min(p[0] for p in coords)
        max_lat = max(p[0] for p in coords)
        
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
            
        if not new_waypoints:
            new_waypoints = coords
                
        with self._lock:
            self.waypoints = new_waypoints
            self.sim_state = {
                'lat': self.waypoints[0][0],
                'lon': self.waypoints[0][1],
                'target_idx': 1,
                'speed_timer': 0,
                'current_speed': 6.0
            }
            self.last_lat = self.sim_state['lat']
            self.last_lon = self.sim_state['lon']
            self.current_data.lat = self.sim_state['lat']
            self.current_data.lon = self.sim_state['lon']
    
        self.is_paused = False

        return True

    def _generate_fake_data(self):
        """Simülasyon için sahte veriler üretir."""
        # Parsel 157'nin tam içinde kalan, sağ üst köşeden başlayan zigzag waypointler
        # (Poligon ray-casting ile hesaplandı, kenarlardan taşmaz)
        with self._lock:
            if not hasattr(self, 'sim_state'):
                self.sim_state = {
                    'lat': self.waypoints[0][0],
                    'lon': self.waypoints[0][1],
                    'target_idx': 1,
                    'speed_timer': 0,
                    'current_speed': random.uniform(5.0, 7.5)
                }
                self.current_data.lat = self.sim_state['lat']
                self.current_data.lon = self.sim_state['lon']
                self.last_lat = self.sim_state['lat']
                self.last_lon = self.sim_state['lon']

            # Hızın saniyeler boyunca sabit kalması (Barkod görünümünü engellemek için)
            self.sim_state['speed_timer'] -= 1
            if self.sim_state['speed_timer'] <= 0:
                if random.random() < 0.3: 
                    # Kırmızı (Hızlı) bölge — tane kaybı tehlikesi!
                    self.sim_state['current_speed'] = random.uniform(8.5, 12.5)
                    self.sim_state['speed_timer'] = random.randint(8, 25)
                elif random.random() < 0.15:
                    # Yavaşlama / dönüş
                    self.sim_state['current_speed'] = random.uniform(2.0, 4.0)
                    self.sim_state['speed_timer'] = random.randint(5, 12)
                else:
                    # Mavi (Normal) bölge
                    self.sim_state['current_speed'] = random.uniform(4.5, 7.5)
                    self.sim_state['speed_timer'] = random.randint(15, 40)
            
            # Her tick'te ufak salınım ekle (hep aynı sayıda donmuş gibi görünmesin)
            speed_kmh = self.sim_state['current_speed'] + random.uniform(-0.5, 0.5)
                
            step_size = 0.000040 * (speed_kmh / 5.0)
            
            target = self.waypoints[self.sim_state['target_idx']]
            d_lat = target[0] - self.sim_state['lat']
            d_lon = target[1] - self.sim_state['lon']
            distance = math.sqrt(d_lat**2 + d_lon**2)

            if distance < step_size:
                # Hedefe ulaştık, sıradakine geç
                if self.sim_state['target_idx'] < len(self.waypoints) - 1:
                    self.sim_state['target_idx'] += 1
                else:
                    # Parsel bitti, durdur
                    self.is_paused = True
                    # Bulunduğu yerde kalmasını sağla
            else:
                # Hedefe doğru ilerle
                self.sim_state['lat'] += (d_lat / distance) * step_size
                self.sim_state['lon'] += (d_lon / distance) * step_size

            new_lat = self.sim_state['lat']
            new_lon = self.sim_state['lon']
            
            dist = calculate_haversine(self.last_lat, self.last_lon, new_lat, new_lon)
            self.current_data.total_distance_m += dist
            
            self.last_lat = new_lat
            self.last_lon = new_lon
            self.current_data.lat = new_lat
            self.current_data.lon = new_lon
            # Knots'a çevir (dashboard geri km/h'ye çevirecek: * 1.852)
            self.current_data.speed_knots = speed_kmh / 1.852
            self.current_data.quality = 1
            self.current_data.satellites = random.randint(8, 12)

    def get_data(self) -> GPSData:
        """Güncel GPS verisini kopyalayarak döndürür (thread-safe)."""
        with self._lock:
            return GPSData(**self.current_data.to_dict())
