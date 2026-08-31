import sqlite3
import os
import json
from contextlib import contextmanager
from typing import List, Dict, Any, Optional
from datetime import datetime

DB_PATH = os.path.join("data", "agrovision.db")

class DatabaseManager:
    """SQLite veritabanı yöneticisi."""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    @contextmanager
    def get_connection(self):
        """Veritabanı bağlantısı sağlar."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def _init_db(self):
        """Tabloları oluşturur."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # sessions tablosu
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time TEXT,
                end_time TEXT,
                location TEXT,
                avg_coverage REAL,
                avg_health REAL,
                crop_type TEXT,
                notes TEXT
            )
            ''')
            
            # detections tablosu
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS detections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                timestamp TEXT,
                frame_number INTEGER,
                crop_type TEXT,
                confidence REAL,
                coverage REAL,
                health_score REAL,
                density REAL,
                yield_score REAL,
                lat REAL,
                lon REAL,
                FOREIGN KEY (session_id) REFERENCES sessions (id)
            )
            ''')
            
            # session_summary tablosu
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS session_summary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                total_frames INTEGER,
                avg_confidence REAL,
                avg_coverage REAL,
                dominant_crop TEXT,
                health_summary_json TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions (id)
            )
            ''')
            
            conn.commit()

    def create_session(self, location: str, notes: str = "") -> int:
        """Yeni bir oturum oluşturur ve kimliğini döndürür."""
        start_time = datetime.now().isoformat()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO sessions (start_time, location, notes) VALUES (?, ?, ?)",
                (start_time, location, notes)
            )
            conn.commit()
            return cursor.lastrowid

    def update_session(self, session_id: int, end_time: str, avg_coverage: float, avg_health: float, crop_type: str):
        """Oturum bilgilerini günceller (oturum bittiğinde)."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE sessions SET end_time = ?, avg_coverage = ?, avg_health = ?, crop_type = ? WHERE id = ?",
                (end_time, avg_coverage, avg_health, crop_type, session_id)
            )
            conn.commit()

    def add_detection(self, session_id: int, frame_number: int, crop_type: str, confidence: float,
                      coverage: float, health_score: float, density: float, yield_score: float,
                      lat: Optional[float] = None, lon: Optional[float] = None):
        """Tek bir çerçevenin tespit sonuçlarını kaydeder."""
        timestamp = datetime.now().isoformat()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO detections (
                    session_id, timestamp, frame_number, crop_type, confidence,
                    coverage, health_score, density, yield_score, lat, lon
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (session_id, timestamp, frame_number, crop_type, confidence,
                  coverage, health_score, density, yield_score, lat, lon))
            conn.commit()

    def add_session_summary(self, session_id: int, total_frames: int, avg_confidence: float,
                            avg_coverage: float, dominant_crop: str, health_summary: dict):
        """Oturum özetini kaydeder."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO session_summary (
                    session_id, total_frames, avg_confidence, avg_coverage,
                    dominant_crop, health_summary_json
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (session_id, total_frames, avg_confidence, avg_coverage,
                  dominant_crop, json.dumps(health_summary)))
            conn.commit()

    def get_session_stats(self, session_id: int) -> Dict[str, Any]:
        """Oturum istatistiklerini getirir."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM session_summary WHERE session_id = ?", (session_id,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return {}

    def get_historical_data(self) -> List[Dict[str, Any]]:
        """Geçmiş tüm oturumların özet bilgilerini getirir."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sessions ORDER BY start_time DESC")
            return [dict(row) for row in cursor.fetchall()]

    def get_field_comparison(self, location: str) -> List[Dict[str, Any]]:
        """Belirli bir konumdaki tarla performanslarının zaman içindeki değişimini getirir."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sessions WHERE location = ? ORDER BY start_time ASC", (location,))
            return [dict(row) for row in cursor.fetchall()]
