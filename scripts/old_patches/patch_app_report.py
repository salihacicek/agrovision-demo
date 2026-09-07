import re

with open('src/dashboard/app.py', 'r') as f:
    content = f.read()

old_block = """class ReportRequest(BaseModel):
    avg_speed: float = 0.0

@app.post("/generate_report")
async def generate_report_endpoint(req: ReportRequest):
    try:
        # Mevcut State verilerini kullanarak rapor oluştur
        session_data = {
            'parsel_no': getattr(state, 'parsel_no', '51-113-25-2'),
            'ada_parsel': getattr(state, 'ada_parsel', '25/2'),
            'owner': getattr(state, 'owner', 'Mehmet Yilmaz'),
            'declared_crop': getattr(state, 'declaration', 'Bilinmiyor'),
            'harvest_date': datetime.now().strftime('%Y-%m-%d'),
            'timestamp': datetime.now().isoformat(),
            'avg_speed': req.avg_speed if req.avg_speed > 0 else round(getattr(state, 'last_speed', 0.0), 1),
            'avg_temp': round(getattr(state, 'last_temp', 0.0), 1),
            'avg_moisture': round(getattr(state, 'last_humidity', 0.0), 1),
            'estimated_yield': 450,
            'harvested_area_m2': getattr(state, 'last_distance_m', 0.0) * 6.0,
            'gps': {'lat': getattr(state, 'last_lat', 0.0), 'lon': getattr(state, 'last_lon', 0.0)},
            'cks_audit_status': 'Uygun'
        }"""

new_block = """from typing import Optional

class ReportRequest(BaseModel):
    parsel_no: str = "Bilinmiyor"
    ada_parsel: str = "Bilinmiyor"
    owner: str = "Bilinmiyor"
    declared_crop: str = "Bilinmiyor"
    total_area_m2: float = 0.0
    harvested_area_m2: float = 0.0
    completion_pct: float = 0.0
    estimated_yield: float = 0.0
    avg_speed: float = 0.0
    avg_temp: float = 0.0
    avg_moisture: float = 0.0
    lat: float = 0.0
    lon: float = 0.0

@app.post("/generate_report")
async def generate_report_endpoint(req: ReportRequest):
    try:
        session_data = {
            'parsel_no': req.parsel_no,
            'ada_parsel': req.ada_parsel,
            'owner': req.owner,
            'declared_crop': req.declared_crop,
            'harvest_date': datetime.now().strftime('%Y-%m-%d'),
            'timestamp': datetime.now().isoformat(),
            'avg_speed': req.avg_speed,
            'avg_temp': req.avg_temp,
            'avg_moisture': req.avg_moisture,
            'estimated_yield': req.estimated_yield,
            'total_area_m2': req.total_area_m2,
            'harvested_area_m2': req.harvested_area_m2,
            'completion_pct': req.completion_pct,
            'gps': {'lat': req.lat, 'lon': req.lon},
            'cks_audit_status': 'Uygun'
        }"""

content = content.replace(old_block, new_block)

with open('src/dashboard/app.py', 'w') as f:
    f.write(content)
