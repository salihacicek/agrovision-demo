import os
import csv
import json
from datetime import datetime
from src.data.database import DatabaseManager

class ExportManager:
    """Oturum verilerini dışa aktaran sınıf."""
    
    def __init__(self, db_manager: DatabaseManager, export_dir: str = "data/exports"):
        self.db = db_manager
        self.export_dir = export_dir
        os.makedirs(self.export_dir, exist_ok=True)

    def export_session_csv(self, session_id: int) -> str:
        """Oturum tespit verilerini CSV formatında dışa aktarır."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM detections WHERE session_id = ?", (session_id,))
            rows = cursor.fetchall()

        if not rows:
            return ""

        filename = os.path.join(self.export_dir, f"session_{session_id}_detections.csv")
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(rows[0].keys())
            for row in rows:
                writer.writerow(row)
                
        return filename

    def export_session_json(self, session_id: int) -> str:
        """Oturum özeti ve tespitlerini JSON formatında dışa aktarır."""
        stats = self.db.get_session_stats(session_id)
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM detections WHERE session_id = ?", (session_id,))
            detections = [dict(row) for row in cursor.fetchall()]

        data = {
            "session_stats": stats,
            "detections": detections,
            "export_time": datetime.now().isoformat()
        }

        filename = os.path.join(self.export_dir, f"session_{session_id}_full.json")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        return filename

    def export_session_geojson(self, session_id: int) -> str:
        """GIS araçları için GeoJSON formatında dışa aktarım."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM detections WHERE session_id = ? AND lat IS NOT NULL AND lon IS NOT NULL", (session_id,))
            rows = cursor.fetchall()

        features = []
        for row in rows:
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [row['lon'], row['lat']]
                },
                "properties": {
                    "crop_type": row['crop_type'],
                    "health_score": row['health_score'],
                    "coverage": row['coverage']
                }
            }
            features.append(feature)

        geojson_data = {
            "type": "FeatureCollection",
            "features": features
        }

        filename = os.path.join(self.export_dir, f"session_{session_id}_map.geojson")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(geojson_data, f, ensure_ascii=False, indent=4)
            
        return filename
