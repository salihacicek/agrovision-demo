import argparse
import sys
import os
import threading
import time

# Proje kök dizinini Python path'e ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.gps_reader import GPSReader

def main():
    parser = argparse.ArgumentParser(description="Agrovision AI - Lite Mod (Sadece Harita ve Dashboard)")
    parser.add_argument("--port", type=int, default=8000, help="Dashboard portu")
    args = parser.parse_args()

    print("="*50)
    print(" AGROVISION AI - LITE MOD (GÖRÜNTÜ İŞLEME KAPALI)")
    print("="*50)

    # 1. Sadece GPS okuyucu başlat
    gps_reader = GPSReader(simulated=True)
    gps_reader.start()

    # Dashboard entegrasyonu
    try:
        from src.dashboard.app import update_dashboard, state, app
        
        def toggle_play_callback():
            if gps_reader.is_paused:
                gps_reader.is_paused = False
                return True
            else:
                gps_reader.is_paused = True
                return False
                
        state.on_toggle_play = toggle_play_callback
        
        def target_parcel_callback(coords):
            return gps_reader.set_waypoints_from_polygon(coords)
            
        state.on_target_parcel_change = target_parcel_callback

        print("✅ Dashboard entegrasyonu aktif. Metrikler web'e gönderilecek.")
    except ImportError as e:
        print(f"⚠️ Dashboard modülü yüklenemedi: {e}")
        return

    import uvicorn
    print(f"🌐 Dashboard Sunucusu Başlatılıyor: http://localhost:{args.port}")
    
    # Arka plan verici döngüsü
    def dashboard_feeder():
        last_stats_time = 0
        while True:
            current_time = time.time()
            if current_time - last_stats_time >= 0.1:
                gps_data = gps_reader.get_data()
                
                # Sahte veri beslemesi (Kamera yok, sadece map var)
                data = {
                    "wheat_coverage": 85.5,
                    "cks_status": "Uygun",
                    "harvested_area_m2": getattr(gps_data, 'total_distance_m', 0.0) * 6.0,
                    "fps": 0.0,
                    "status": "Duraklatıldı" if gps_reader.is_paused else "Sistem Aktif",
                    "is_paused": gps_reader.is_paused,
                    "source": "lite_mode",
                    "lat": gps_data.lat if gps_data and hasattr(gps_data, 'lat') and gps_data.lat else 40.209500,
                    "lon": gps_data.lon if gps_data and hasattr(gps_data, 'lon') and gps_data.lon else 33.007700,
                    "speed": 0.0 if gps_reader.is_paused else ((gps_data.speed_knots * 1.852) if gps_data and getattr(gps_data, 'speed_knots', None) else 0.0),
                    "temperature": gps_data.temperature if gps_data and hasattr(gps_data, 'temperature') else 32.0,
                    "humidity": gps_data.humidity if gps_data and hasattr(gps_data, 'humidity') else 45.0,
                    "crop_moisture": gps_data.crop_moisture if gps_data and hasattr(gps_data, 'crop_moisture') else 12.5,
                    "crop_temperature": gps_data.crop_temperature if gps_data and hasattr(gps_data, 'crop_temperature') else 28.0
                }
                last_stats_time = current_time
                
                # Kare (frame) yok
                update_dashboard(None, data)
                    
            time.sleep(0.04)
            
    feeder_thread = threading.Thread(target=dashboard_feeder, daemon=True)
    feeder_thread.start()
    
    port = int(os.environ.get("PORT", args.port))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="error")
if __name__ == "__main__":
    main()
