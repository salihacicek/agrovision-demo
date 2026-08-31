from dataclasses import dataclass, field
from typing import Optional, Callable, Dict, Any
import time
import numpy as np

@dataclass
class PipelineConfig:
    frame_skip: int = 1
    process_width: int = 640
    process_height: int = 640
    conf_threshold: float = 0.5

@dataclass
class PipelineStatus:
    is_running: bool = False
    total_frames: int = 0
    processed_frames: int = 0
    avg_inference_time_ms: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_running": self.is_running,
            "total_frames": self.total_frames,
            "processed_frames": self.processed_frames,
            "avg_inference_time_ms": self.avg_inference_time_ms
        }

class FramePipeline:
    """Ana görüntü işleme ardışık düzeni (pipeline)."""

    def __init__(self, camera, model, session_manager, gps_reader, config: PipelineConfig):
        self.camera = camera
        self.model = model
        self.session_manager = session_manager
        self.gps_reader = gps_reader
        self.config = config
        self.status = PipelineStatus()
        
        # Callbacks
        self.on_detection: Optional[Callable] = None
        self.on_error: Optional[Callable] = None
        self.latest_annotated_frame = None

    def run(self):
        """Pipeline'ı başlatır ve sürekli çalıştırır."""
        self.status.is_running = True
        frame_count = 0
        
        # Sınıf isimlerini güzel Türkçe formatla (YOLO plot için)
        if hasattr(self.model, 'names'):
            for k, v in self.model.names.items():
                if v == "ayc": self.model.names[k] = "Ayçiçeği"
                elif v == "bugday": self.model.names[k] = "Buğday"
                elif v == "misir": self.model.names[k] = "Mısır"
                elif v == "arpa": self.model.names[k] = "Arpa"
        
        while self.status.is_running:
            frame = self.camera.read()
            if frame is None:
                if self.camera.config.source == "none":
                    self.latest_annotated_frame = None
                time.sleep(0.01)
                continue
                
            frame_count += 1
            self.status.total_frames += 1
            
            # Kare atlama
            if frame_count % self.config.frame_skip != 0:
                continue
                
            try:
                self._process_frame(frame)
            except Exception as e:
                with open("pipeline_error.log", "a") as f:
                    f.write(f"Error in _process_frame: {str(e)}\n")
            
    def _process_frame(self, frame: np.ndarray):
        """Tek bir kareyi işler."""
        start_time = time.time()
        
        try:
            # Model çıkarımı
            results = self.model(frame, verbose=False, conf=self.config.conf_threshold)
            
            # YOLO plot() için isimleri Türkçe yap
            for r in results:
                if hasattr(r, 'names'):
                    for k, v in list(r.names.items()):
                        if v == "ayc": r.names[k] = "Ayçiçeği"
                        elif v == "bugday": r.names[k] = "Buğday"
                        elif v == "misir": r.names[k] = "Mısır"
                        elif v == "arpa": r.names[k] = "Arpa"
                        
            self.latest_annotated_frame = results[0].plot()
            
            # GPS verisi
            gps_data = self.gps_reader.get_data()
            
            # Sonuç analizi
            for r in results:
                # Örnek basit analiz (YOLOv8 için)
                boxes = r.boxes
                for box in boxes:
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    
                    crop_type = self.model.names[cls_id]
                    
                    # Gerçekçi olmayan örnek değerler, pratikte model ve görüntü analizinden gelir
                    coverage = conf * 100 
                    health = 85.0 if conf > 0.8 else 60.0
                    yield_score = health * 0.9
                    density = coverage / 100.0
                    
                    self.session_manager.update_frame_data(
                        crop_type=crop_type,
                        coverage=coverage,
                        health=health,
                        yield_score=yield_score,
                        confidence=conf,
                        density=density,
                        lat=gps_data.lat,
                        lon=gps_data.lon
                    )
                    
                    if self.on_detection:
                        self.on_detection(frame, crop_type, conf)
                        
            # Performans metrikleri
            process_time_ms = (time.time() - start_time) * 1000
            self.status.avg_inference_time_ms = (self.status.avg_inference_time_ms * self.status.processed_frames + process_time_ms) / (self.status.processed_frames + 1)
            self.status.processed_frames += 1

        except Exception as e:
            if self.on_error:
                self.on_error(str(e))

    def stop(self):
        """Pipeline çalışmasını durdurur."""
        self.status.is_running = False
