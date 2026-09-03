from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect, UploadFile, File
from fastapi.responses import StreamingResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import asyncio
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
import threading
import os
import shutil
from pydantic import BaseModel

app = FastAPI(title="Agrovision AI Dashboard")

# Dosya yolları
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

class DashboardState:
    """Dashboard için thread-safe state yönetimi."""
    def __init__(self):
        self.frame = None
        self.declaration = "bilinmiyor"
        self.data = {
            "wheat_coverage": 0.0,
            "corn_coverage": 0.0,
            "sunflower_coverage": 0.0,
            "barley_coverage": 0.0,
            "cks_status": "Bekleniyor",
            "harvested_area_m2": 0.0,
            "fps": 0.0,
            "status": "Sistem Başlatılıyor...",
            "lat": 40.2100,
            "lon": 33.0100,
            "speed": 0.0,
            "temperature": 28.5,
            "humidity": 45.0,
            "crop_moisture": 13.5,
            "crop_temperature": 27.0
        }
        self.lock = threading.Lock()
        self.clients = set()
        self.on_video_upload = None
        self.on_toggle_play = None
        self.on_client_frame = None
        self.on_target_parcel_change = None
        
    def update(self, frame, data):
        """Ana OpenCV döngüsünden verileri günceller."""
        with self.lock:
            if frame is not None:
                self.frame = frame.copy()
            elif data.get("source") == "none":
                self.frame = None
            self.data.update(data)
            
    async def broadcast(self):
        """Tüm bağlı WebSocket istemcilerine güncel metrikleri gönderir."""
        with self.lock:
            data_copy = self.data.copy()
        
        dead_clients = set()
        for client in self.clients:
            try:
                await client.send_json(data_copy)
            except Exception:
                dead_clients.add(client)
                
        for client in dead_clients:
            self.clients.remove(client)

state = DashboardState()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Ana web arayüzünü sunar."""
    return templates.TemplateResponse(request, "index.html")

@app.get("/api/debug")
async def debug_state():
    """Anlık state.data'yı JSON olarak döndürür (debug için)."""
    with state.lock:
        d = state.data.copy()
    d["ws_clients"] = len(state.clients)
    return JSONResponse(d)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Metriklerin gerçek zamanlı akışı için WebSocket."""
    await websocket.accept()
    state.clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data.startswith('{"type":"client_frame"'):
                import json
                msg = json.loads(data)
                b64 = msg.get("frame", "").split(',')[1] if "frame" in msg and "," in msg["frame"] else None
                if b64:
                    import base64
                    import numpy as np
                    img_data = base64.b64decode(b64)
                    np_arr = np.frombuffer(img_data, np.uint8)
                    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                    if state.on_client_frame:
                        state.on_client_frame(frame)
    except WebSocketDisconnect:
        state.clients.remove(websocket)
        if len(state.clients) == 0:
            if state.on_video_upload:
                state.on_video_upload("none")
            with state.lock:
                state.frame = None
    except Exception as e:
        if websocket in state.clients:
            state.clients.remove(websocket)
        if len(state.clients) == 0:
            if state.on_video_upload:
                state.on_video_upload("none")
            with state.lock:
                state.frame = None

async def frame_generator():
    """Arka planda güncel kareyi web istemcilerine MJPEG olarak gönderir."""
    while True:
        frame = state.frame
        if frame is not None and CV2_AVAILABLE:
            # Jpeg olarak kodla (kaliteyi düşürerek bant genişliğini koru)
            ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            if ret:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        else:
            # Görüntü yoksa veya Lite moddaysa placeholder gönderilebilir, şimdilik sadece bekle
            pass
        await asyncio.sleep(0.04)  # Maksimum ~25 FPS sınırlaması

@app.get("/video_feed")
async def video_feed():
    """Görüntü akışı endpointi."""
    return StreamingResponse(frame_generator(), media_type="multipart/x-mixed-replace; boundary=frame")

async def broadcast_loop():
    """Arka planda saniyede 10 kez metrikleri web'e basar."""
    while True:
        await state.broadcast()
        await asyncio.sleep(0.1)

import random
import math

async def gps_simulator_loop():
    """Sanal GPS, hız, sıcaklık ve nem verisi üretir."""
    lat = 38.0
    lon = 32.50
    heading = random.uniform(0, 360)
    temperature = 28.5
    humidity = 45.0
    crop_moisture = 13.5
    crop_temperature = 27.0
    
    while True:
        await asyncio.sleep(1.0)
        speed = random.uniform(5.0, 12.0)
        distance_km = speed / 3600.0
        
        d_lat = (distance_km * math.cos(math.radians(heading))) / 111.0
        d_lon = (distance_km * math.sin(math.radians(heading))) / (111.0 * math.cos(math.radians(lat)))
        
        lat += d_lat
        lon += d_lon
        heading += random.uniform(-15, 15)
        
        # Sıcaklık ve nemde ufak dalgalanmalar
        temperature += random.uniform(-0.2, 0.2)
        humidity += random.uniform(-0.5, 0.5)
        crop_moisture += random.uniform(-0.1, 0.1)
        crop_temperature += random.uniform(-0.1, 0.2)
        with state.lock:
            # Sadece çevre sensörlerini simüle et (GPS artık gps_reader'da)
            state.data["temperature"] = temperature
            state.data["humidity"] = humidity
            state.data["crop_moisture"] = crop_moisture
            state.data["crop_temperature"] = crop_temperature

@app.on_event("startup")
async def startup_event():
    """Sunucu başladığında broadcast döngüsünü başlatır."""
    asyncio.create_task(broadcast_loop())
    asyncio.create_task(gps_simulator_loop())

def update_dashboard(frame, data):
    # Update global state with latest metrics for report generation
    if data:
        state.last_speed = data.get('speed', 0)
        state.last_temp = data.get('temperature', 0)
        state.last_humidity = data.get('humidity', 0)
        state.last_distance_m = data.get('harvested_area_m2', 0) / 6.0 if data.get('harvested_area_m2') else 0
        state.last_lat = data.get('lat', 0)
        state.last_lon = data.get('lon', 0)

    """run_live.py üzerinden çağrılacak global güncelleme fonksiyonu."""
    state.update(frame, data)

@app.post("/upload_video")
async def upload_video(file: UploadFile = File(...)):
    """Kullanıcının yüklediği videoyu kaydeder ve sistemi yeni videoya geçirir."""
    filename = file.filename
    upload_dir = os.path.abspath(os.path.join(BASE_DIR, "../../data/raw_videos"))
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    if state.on_video_upload:
        state.on_video_upload(file_path)
        
    return JSONResponse({"status": "success", "filename": filename})

@app.post("/toggle_play")
async def toggle_play():
    if state.on_toggle_play:
        is_playing = state.on_toggle_play()
        return JSONResponse({"status": "success", "is_playing": is_playing})
    return JSONResponse({"status": "error"})

class SetTargetParcelRequest(BaseModel):
    coords: list

@app.post("/set_target_parcel")
async def set_target_parcel(req: SetTargetParcelRequest):
    if hasattr(state, 'on_target_parcel_change') and state.on_target_parcel_change:
        success = state.on_target_parcel_change(req.coords)
        if success:
            return JSONResponse({"status": "success"})
    return JSONResponse({"status": "error"})

class TestVideoRequest(BaseModel):
    video_name: str

@app.post("/api/use_test_video")
async def use_test_video(req: TestVideoRequest):
    if state.on_video_upload:
        # Check if video exists
        video_path = f"data/raw_videos/{req.video_name}"
        if os.path.exists(video_path):
            state.on_video_upload(video_path)
            return JSONResponse({"status": "success", "message": f"Test videosuna geçildi: {req.video_name}"})
        return JSONResponse({"status": "error", "message": "Video bulunamadı"}, status_code=404)
    return JSONResponse({"status": "error", "message": "Callback bulunamadı"}, status_code=500)

@app.post("/api/use_webcam")
async def use_webcam():
    if state.on_video_upload:
        state.on_video_upload("client")
        return JSONResponse({"status": "success", "message": "İstemci kamerasına geçildi"})
    return JSONResponse({"status": "error", "message": "Callback bulunamadı"}, status_code=500)

@app.post("/api/stop_camera")
async def stop_camera():
    if state.on_video_upload:
        state.on_video_upload("none")
        with state.lock:
            state.frame = None
        return JSONResponse({"status": "success", "message": "Kamera kapatıldı"})
    return JSONResponse({"status": "error", "message": "Callback bulunamadı"}, status_code=500)

@app.post("/set_declaration")
async def set_declaration(crop: str):
    """Kullanıcının ÇKS beyanını günceller."""
    state.declaration = crop
    return JSONResponse({"status": "success", "crop": crop})

@app.post("/export_cks")
async def export_cks():
    """Mevcut verileri ÇKS (Otenelabs) bulut sistemine göndermek üzere (simülasyon) kaydeder."""
    import json
    import datetime
    
    export_dir = os.path.abspath(os.path.join(BASE_DIR, "../../exports"))
    os.makedirs(export_dir, exist_ok=True)
    filename = f"cks_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join(export_dir, filename)
    
    # Calculate dominant crop
    metrics = {
        "bugday": state.data.get("wheat_coverage", 0),
        "misir": state.data.get("corn_coverage", 0),
        "aycicegi": state.data.get("sunflower_coverage", 0),
        "arpa": state.data.get("barley_coverage", 0),
    }
    detected_crop = max(metrics.items(), key=lambda x: x[1])
    
    report = {
        "timestamp": datetime.datetime.now().isoformat(),
        "declared_crop": state.declaration,
        "detected_crop": detected_crop[0] if detected_crop[1] > 0 else "Bilinmiyor",
        "confidence": int(detected_crop[1]) if detected_crop[1] > 0 else 0,
        "cks_audit_status": state.data.get("cks_status", "Bekleniyor"),
        "metrics": metrics,
        "harvested_area_m2": state.data.get("harvested_area_m2", 0.0),
        "gps": {
            "lat": state.data.get("lat", 0),
            "lon": state.data.get("lon", 0)
        },
        "parsel_no": "51-113-25-2",
        "ada_parsel": "25/2",
        "owner": "Mehmet Yilmaz",
        "harvest_date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "filename": filename
    }
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=4)
        
    return JSONResponse({"status": "success", "file": filename})

@app.get("/api/parcels")
async def get_parcels():
    """TKGM Parsel verilerini GeoJSON formatında döndürür."""
    geojson_feature_collection = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [33.007600, 40.209900], [33.010200, 40.210100],
                        [33.010200, 40.209600], [33.008100, 40.209400],
                        [33.007600, 40.209900]
                    ]]
                },
                "properties": {
                    "parsel_id": "P157", "ada_no": "124", "parsel_no": "157",
                    "malik_adi": "Ahmet Yılmaz", "alan_donum": 4.82, "urun_tipi": "Buğday"
                }
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [33.010300, 40.210100], [33.013500, 40.210300],
                        [33.013500, 40.209800], [33.010300, 40.209600],
                        [33.010300, 40.210100]
                    ]]
                },
                "properties": {
                    "parsel_id": "P158", "ada_no": "124", "parsel_no": "158",
                    "malik_adi": "Mehmet Demir", "alan_donum": 3.65, "urun_tipi": "Arpa"
                }
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [33.003500, 40.210200], [33.006800, 40.210600],
                        [33.008500, 40.208800], [33.004000, 40.208400],
                        [33.003500, 40.210200]
                    ]]
                },
                "properties": {
                    "parsel_id": "P156", "ada_no": "124", "parsel_no": "156",
                    "malik_adi": "Bilinmiyor", "alan_donum": 5.10, "urun_tipi": "Mısır"
                }
            }
        ]
    }
    return JSONResponse(geojson_feature_collection)

@app.get("/api/reports")
async def get_reports():
    """Tüm JSON raporlarını listeler."""
    import json
    export_dir = os.path.abspath(os.path.join(BASE_DIR, "../../exports"))
    reports = []
    if os.path.exists(export_dir):
        for fname in sorted(os.listdir(export_dir), reverse=True):
            if fname.endswith(".json"):
                with open(os.path.join(export_dir, fname), "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                        data["filename"] = fname
                        reports.append(data)
                    except:
                        pass
    return JSONResponse(reports)

from fastapi.responses import FileResponse
from src.reporting.pdf_report import PDFReportGenerator

@app.get("/download_report/{filename}")
async def download_report(filename: str):
    """Belirtilen JSON raporunu PDF'e çevirip indirir."""
    import json
    export_dir = os.path.abspath(os.path.join(BASE_DIR, "../../exports"))
    filepath = os.path.join(export_dir, filename)
    
    if not os.path.exists(filepath):
        return JSONResponse({"error": "Report not found"}, status_code=404)
        
    with open(filepath, "r", encoding="utf-8") as f:
        session_data = json.load(f)
        
    pdf_gen = PDFReportGenerator(output_dir=export_dir)
    pdf_filename = filename.replace(".json", ".pdf")
    pdf_path = pdf_gen.generate_report(session_data, output_filename=pdf_filename)
    
    return FileResponse(path=pdf_path, filename=pdf_filename, media_type='application/pdf')

from fastapi.responses import FileResponse
from src.reporting.pdf_report import PDFReportGenerator
from datetime import datetime

@app.post("/generate_report")
async def generate_report_endpoint():
    try:
        # Mevcut State verilerini kullanarak rapor oluştur
        session_data = {
            'parsel_no': getattr(state, 'parsel_no', '51-113-25-2'),
            'ada_parsel': getattr(state, 'ada_parsel', '25/2'),
            'owner': getattr(state, 'owner', 'Mehmet Yilmaz'),
            'declared_crop': getattr(state, 'declaration', 'Bilinmiyor'),
            'harvest_date': datetime.now().strftime('%Y-%m-%d'),
            'timestamp': datetime.now().isoformat(),
            'avg_speed': round(getattr(state, 'last_speed', 0.0), 1),
            'avg_temp': round(getattr(state, 'last_temp', 0.0), 1),
            'avg_moisture': round(getattr(state, 'last_humidity', 0.0), 1),
            'estimated_yield': 450,
            'harvested_area_m2': getattr(state, 'last_distance_m', 0.0) * 6.0,
            'gps': {'lat': getattr(state, 'last_lat', 0.0), 'lon': getattr(state, 'last_lon', 0.0)},
            'cks_audit_status': 'Uygun'
        }
        
        report_gen = PDFReportGenerator()
        filepath = report_gen.generate_report(session_data)
        
        if os.path.exists(filepath):
            return FileResponse(path=filepath, filename=os.path.basename(filepath), media_type='application/pdf')
        else:
            return JSONResponse({"status": "error", "message": "PDF oluşturulamadı"}, status_code=500)
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)
