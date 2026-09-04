import argparse
import sys
import os
import cv2
import threading
import time
from ultralytics import YOLO

# Proje kök dizinini Python path'e ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.database import DatabaseManager
from src.data.session_manager import SessionManager
from src.data.gps_reader import GPSReader
from src.pipeline.camera_stream import CameraStream, CameraConfig
from src.pipeline.frame_pipeline import FramePipeline, PipelineConfig
from src.pipeline.result_aggregator import ResultAggregator
from src.reporting.pdf_report import PDFReportGenerator

def main():
    parser = argparse.ArgumentParser(description="Agrovision AI - Gerçek Zamanlı Tarla Analizi")
    parser.add_argument("--source", type=str, default="0", help="Kamera kaynağı (0, 1 veya video/rtsp yolu)")
    parser.add_argument("--model", type=str, default="yolov8n.pt", help="YOLO model yolu")
    parser.add_argument("--session", action="store_true", help="Oturum kaydını başlat")
    parser.add_argument("--heatmap", action="store_true", help="Sağlık ısı haritasını göster")
    parser.add_argument("--no-display", action="store_true", help="Görüntü penceresini gösterme (headless mod)")
    parser.add_argument("--dashboard", action="store_true", help="Web dashboard'u başlat")
    parser.add_argument("--port", type=int, default=8000, help="Dashboard portu")
    parser.add_argument("--sim-gps", action="store_true", help="GPS verisini simüle et")
    args = parser.parse_args()

    print("="*50)
    print(" AGROVISION AI - BAŞLATILIYOR")
    print("="*50)

    # 1. Veritabanı ve Oturum Yönetimi
    db = DatabaseManager()
    session_manager = SessionManager(db)
    
    # 2. Donanım Arayüzleri
    gps_reader = GPSReader(simulated=True) # Always simulate for demo
    gps_reader.start()

    # Kamera kaynağını parse et (integer ise int'e çevir)
    cam_source = int(args.source) if args.source.isdigit() else args.source
    camera = CameraStream(CameraConfig(source=cam_source))
    camera.start()

    # 3. Model Yükleme
    print(f"[{args.model}] modeli yükleniyor...")
    try:
        model = YOLO(args.model)
    except Exception as e:
        print(f"Model yüklenemedi: {e}")
        return

    # 4. Pipeline Kurulumu
    pipeline_config = PipelineConfig()
    pipeline = FramePipeline(camera, model, session_manager, gps_reader, pipeline_config)
    
    aggregator = ResultAggregator()

    # Callback tanımlamaları
    def on_detection(frame, crop_type, conf):
        aggregator.add_result(crop_type, conf*100, conf*100)
    
    pipeline.on_detection = on_detection

    # 5. Oturum Başlatma (opsiyonel)
    if args.session:
        session_id = session_manager.start_session(location="Test Tarlası", operator="Sistem")
        print(f"Yeni oturum başlatıldı. ID: {session_id}")

    # Dashboard entegrasyonu
    dashboard_update_func = None
    if args.dashboard:
        try:
            from src.dashboard.app import update_dashboard, state
            dashboard_update_func = update_dashboard
            
            def change_source_callback(video_path):
                print(f"Yeni video kaynağına geçiliyor: {video_path}")
                
                # Önceki görüntünün kalmaması için kareyi anında temizle
                with state.lock:
                    state.frame = None
                pipeline.latest_annotated_frame = None
                
                camera.change_source(video_path)
                if video_path == "none":
                    gps_reader.is_paused = True
                else:
                    aggregator.reset()
                    gps_reader.reset_distance()
                    gps_reader.is_paused = False
                
            def toggle_play_callback():
                if camera.is_paused:
                    camera.resume()
                    gps_reader.is_paused = False
                    return True
                else:
                    camera.pause()
                    gps_reader.is_paused = True
                    return False
                
            def client_frame_callback(frame):
                camera.receive_client_frame(frame)
                
            state.on_video_upload = change_source_callback
            state.on_toggle_play = toggle_play_callback
            state.on_client_frame = client_frame_callback
            state.on_target_parcel_change = gps_reader.set_waypoints_from_polygon
            
            def reset_simulation_callback():
                with gps_reader._lock:
                    if hasattr(gps_reader, 'sim_state') and len(gps_reader.waypoints) > 0:
                        gps_reader.sim_state['target_idx'] = 1
                        gps_reader.sim_state['lat'] = gps_reader.waypoints[0][0]
                        gps_reader.sim_state['lon'] = gps_reader.waypoints[0][1]
                        gps_reader.last_lat = gps_reader.waypoints[0][0]
                        gps_reader.last_lon = gps_reader.waypoints[0][1]
                        gps_reader.current_data.lat = gps_reader.waypoints[0][0]
                        gps_reader.current_data.lon = gps_reader.waypoints[0][1]
                        gps_reader.is_paused = False
                return True
                
            state.on_reset_simulation = reset_simulation_callback
            
            print("✅ Dashboard entegrasyonu aktif. Metrikler web'e gönderilecek.")
        except ImportError as e:
            print(f"⚠️ Dashboard modülü yüklenemedi: {e}")

    # Arka planda pipeline'ı çalıştır
    pipeline_thread = threading.Thread(target=pipeline.run, daemon=True)
    pipeline_thread.start()

    # Eğer dashboard istenmişse, Uvicorn'u ana thread'de çalıştır (FastAPI gereksinimi)
    if args.dashboard:
        import uvicorn
        print(f"🌐 Dashboard Sunucusu Başlatılıyor: http://localhost:{args.port}")
        # Not: Uvicorn ana thread'i bloklar. Pipeline zaten daemon thread'de çalışıyor.
        
        # Pipeline'dan verileri alıp dashboard'a gönderecek bir arka plan görevi
        def dashboard_feeder():
            last_stats_time = 0
            data = {}
            while True:
                # Dashboard artık yapay zekanın işaretlediği kareyi gösterecek
                # ve böylece kamera buffer'ını boş yere tüketmeyecek.
                frame = getattr(pipeline, 'latest_annotated_frame', None)
                
                current_time = time.time()
                if current_time - last_stats_time >= 0.1:
                    stats = aggregator.get_aggregated()
                    gps_data = gps_reader.get_data()
                    
                    # ÇKS Denetim Mantığı
                    cks_status = "Bekleniyor"
                    declared_crop = getattr(state, 'declaration', 'bilinmiyor')
                    
                    if declared_crop != 'bilinmiyor' and stats.dominant_crop != 'bilinmiyor':
                        if declared_crop == stats.dominant_crop:
                            cks_status = "Uygun"
                        else:
                            cks_status = "Uyumsuz (Kaçak Ekim)"
                            
                    data = {
                        "wheat_coverage": stats.avg_coverage if stats.dominant_crop == "bugday" else 0,
                        "corn_coverage": stats.avg_coverage if stats.dominant_crop == "misir" else 0,
                        "sunflower_coverage": stats.avg_coverage if stats.dominant_crop == "ayc" else 0,
                        "barley_coverage": stats.avg_coverage if stats.dominant_crop == "arpa" else 0,
                        "cks_status": cks_status,
                        "harvested_area_m2": getattr(gps_data, 'total_distance_m', 0.0) * 6.0, # 6 metre tabla genişliği
                        "fps": camera.status.fps,
                        "status": "Duraklatıldı" if camera.is_paused else "Sistem Aktif",
                        "is_paused": camera.is_paused,
                        "source": str(camera.config.source),
                        "lat": gps_data.lat if gps_data and hasattr(gps_data, 'lat') and gps_data.lat else 39.7612,
                        "lon": gps_data.lon if gps_data and hasattr(gps_data, 'lon') and gps_data.lon else 32.4250,
                        "speed": (gps_data.speed_knots * 1.852) if gps_data and getattr(gps_data, 'speed_knots', None) else 0.0
                    }
                    last_stats_time = current_time
                    
                if dashboard_update_func:
                    dashboard_update_func(frame, data)
                    
                if frame is None:
                    with open("dashboard_feeder_error.log", "a") as f:
                        f.write(f"{time.time()}: Frame is None! pipeline.latest_annotated_frame is None\n")
                        
                time.sleep(0.04) # 25 FPS video akışı
                
        feeder_thread = threading.Thread(target=dashboard_feeder, daemon=True)
        feeder_thread.start()
        
        uvicorn.run("src.dashboard.app:app", host="0.0.0.0", port=args.port, log_level="error")
        return # Uvicorn kapanınca program biter


    print("Sistem çalışıyor. Çıkmak için 'q' tuşuna basın.")
    
    # Ana döngü (UI ve Kontrol)
    try:
        while True:
            # Güncel kareyi ve sonucu UI için al
            # Not: pipeline._process_frame zaten kareleri işliyor, 
            # ancak ekranda göstermek istiyorsak modeli tekrar çalıştırmamalıyız 
            # veya pipeline içindeki son işlenmiş kareyi almalıyız.
            # Basitlik için burada kamera sınıfından direkt okuyoruz (hızlı gösterim)
            
            if not args.no_display:
                # Gerçek uygulamada işlenmiş kareyi (bounding box'larla) göstermek için
                # pipeline içine bir "last_processed_frame" eklenebilir.
                # Şimdilik sadece sistemi bloklamadan bekliyoruz.
                time.sleep(0.1)
                
                # İstatistikleri ekrana yazdır (konsola)
                stats = aggregator.get_aggregated()
                sys.stdout.write(f"\rÜrün: {stats.dominant_crop} | Sağlık: {stats.avg_health:.1f} | Kapsama: {stats.avg_coverage:.1f} | FPS: {camera.status.fps:.1f}")
                sys.stdout.flush()

            else:
                time.sleep(1)

    except KeyboardInterrupt:
        print("\nSistem kapatılıyor...")
    finally:
        pipeline.stop()
        camera.stop()
        gps_reader.stop()
        if args.session:
            session_manager.end_session()
            print("Oturum kaydedildi.")
            # Rapor oluştur
            report_gen = PDFReportGenerator()
            report_gen.generate_report(session_manager.current_session.to_dict())
            print("Rapor oluşturuldu.")

if __name__ == "__main__":
    main()
