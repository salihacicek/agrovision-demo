from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
import threading
from datetime import datetime
from src.data.database import DatabaseManager

@dataclass
class SessionInfo:
    """Oturum bilgilerini tutan veri sınıfı."""
    session_id: Optional[int] = None
    location: str = "Bilinmeyen Tarla"
    operator: str = "Bilinmeyen Operatör"
    notes: str = ""
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: str = "IDLE"  # IDLE, ACTIVE, PAUSED, COMPLETED
    
    total_frames: int = 0
    total_coverage: float = 0.0
    total_health: float = 0.0
    total_yield: float = 0.0
    crop_counts: Dict[str, int] = field(default_factory=lambda: {"Buğday": 0, "Mısır": 0})
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "location": self.location,
            "operator": self.operator,
            "notes": self.notes,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "status": self.status,
            "total_frames": self.total_frames,
            "avg_coverage": self.get_avg_coverage(),
            "avg_health": self.get_avg_health(),
            "avg_yield": self.get_avg_yield(),
            "dominant_crop": self.get_dominant_crop()
        }

    def get_avg_coverage(self) -> float:
        return self.total_coverage / self.total_frames if self.total_frames > 0 else 0.0

    def get_avg_health(self) -> float:
        return self.total_health / self.total_frames if self.total_frames > 0 else 0.0

    def get_avg_yield(self) -> float:
        return self.total_yield / self.total_frames if self.total_frames > 0 else 0.0

    def get_dominant_crop(self) -> str:
        if not self.crop_counts or all(v == 0 for v in self.crop_counts.values()):
            return "Bilinmiyor"
        return max(self.crop_counts, key=self.crop_counts.get)

class SessionManager:
    """Tarla tarama oturumlarını yöneten sınıf."""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.current_session = SessionInfo()
        self._lock = threading.Lock()

    def start_session(self, location: str, operator: str = "Bilinmiyor", notes: str = "") -> int:
        """Yeni bir tarama oturumu başlatır."""
        with self._lock:
            if self.current_session.status in ["ACTIVE", "PAUSED"]:
                raise ValueError("Zaten aktif veya duraklatılmış bir oturum var.")
            
            session_id = self.db.create_session(location=location, notes=f"Operatör: {operator}\n{notes}")
            self.current_session = SessionInfo(
                session_id=session_id,
                location=location,
                operator=operator,
                notes=notes,
                start_time=datetime.now(),
                status="ACTIVE"
            )
            return session_id

    def pause_session(self):
        """Oturumu duraklatır."""
        with self._lock:
            if self.current_session.status == "ACTIVE":
                self.current_session.status = "PAUSED"

    def resume_session(self):
        """Duraklatılmış oturumu devam ettirir."""
        with self._lock:
            if self.current_session.status == "PAUSED":
                self.current_session.status = "ACTIVE"

    def update_frame_data(self, crop_type: str, coverage: float, health: float, yield_score: float,
                          confidence: float, density: float, lat: Optional[float] = None, lon: Optional[float] = None):
        """Her çerçeve işlendiğinde oturum verilerini günceller."""
        with self._lock:
            if self.current_session.status != "ACTIVE":
                return

            self.current_session.total_frames += 1
            self.current_session.total_coverage += coverage
            self.current_session.total_health += health
            self.current_session.total_yield += yield_score
            
            if crop_type in self.current_session.crop_counts:
                self.current_session.crop_counts[crop_type] += 1
            else:
                self.current_session.crop_counts[crop_type] = 1

            self.db.add_detection(
                session_id=self.current_session.session_id,
                frame_number=self.current_session.total_frames,
                crop_type=crop_type,
                confidence=confidence,
                coverage=coverage,
                health_score=health,
                density=density,
                yield_score=yield_score,
                lat=lat,
                lon=lon
            )

    def end_session(self):
        """Oturumu sonlandırır ve özet verileri kaydeder."""
        with self._lock:
            if self.current_session.status not in ["ACTIVE", "PAUSED"]:
                return

            self.current_session.end_time = datetime.now()
            self.current_session.status = "COMPLETED"

            avg_cov = self.current_session.get_avg_coverage()
            avg_health = self.current_session.get_avg_health()
            dominant_crop = self.current_session.get_dominant_crop()

            self.db.update_session(
                session_id=self.current_session.session_id,
                end_time=self.current_session.end_time.isoformat(),
                avg_coverage=avg_cov,
                avg_health=avg_health,
                crop_type=dominant_crop
            )

            health_summary = {"status": "good" if avg_health > 70 else "poor"}

            self.db.add_session_summary(
                session_id=self.current_session.session_id,
                total_frames=self.current_session.total_frames,
                avg_confidence=0.85, # Örnek sabit değer
                avg_coverage=avg_cov,
                dominant_crop=dominant_crop,
                health_summary=health_summary
            )
