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
            (40.210050, 33.010100), (40.209850, 33.007750),
            (40.209775, 33.007825), (40.209975, 33.010100),
            (40.209900, 33.010100), (40.209700, 33.007900),
            (40.209625, 33.007975), (40.209825, 33.010100),
            (40.209750, 33.010100), (40.209550, 33.008050),
            (40.209475, 33.008125), (40.209675, 33.010100),
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
        """Dinamik olarak parsel poligonundan çapraz waypointler hesaplar."""
        if not coords or len(coords) != 4:
            return False
            
        tl, tr, br, bl = coords
        
        height = tl[0] - bl[0]
        # Eğer çok küçükse en az 4 tur at, büyükse daha fazla
        num_passes = max(4, int(height / 0.0001))
        
        new_waypoints = []
        for i in range(num_passes):
            f = i / max(1, (num_passes - 1))
            
            # Sol kenar (TL'den BL'ye)
            left_lat = tl[0] + f * (bl[0] - tl[0])
            left_lon = tl[1] + f * (bl[1] - tl[1])
            
            # Sağ kenar (TR'den BR'ye)
            right_lat = tr[0] + f * (br[0] - tr[0])
            right_lon = tr[1] + f * (br[1] - tr[1])
            
            # Kenarlara tam değmemesi için hafif içe çekelim
            lon_margin = abs(right_lon - left_lon) * 0.05
            if left_lon < right_lon:
                left_lon += lon_margin
                right_lon -= lon_margin
            else:
                left_lon -= lon_margin
                right_lon += lon_margin
                
            if i % 2 == 0:
                new_waypoints.append((right_lat, right_lon))
                new_waypoints.append((left_lat, left_lon))
            else:
                new_waypoints.append((left_lat, left_lon))
                new_waypoints.append((right_lat, right_lon))
                
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
                
            # Adım büyüklüğü
            step_size = 0.000003 * (speed_kmh / 5.0)
            
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
