import cv2
import threading
import time
from dataclasses import dataclass
from typing import Optional, Union, Dict, Any
import numpy as np

@dataclass
class CameraConfig:
    source: Union[int, str] = 0
    width: int = 640
    height: int = 480
    fps: int = 30
    buffer_size: int = 1

@dataclass
class CameraStatus:
    is_open: bool = False
    fps: float = 0.0
    dropped_frames: int = 0
    reconnect_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_open": self.is_open,
            "fps": self.fps,
            "dropped_frames": self.dropped_frames,
            "reconnect_count": self.reconnect_count
        }

class CameraStream:
    """Kamera veya video akışını yöneten sınıf."""
    
    def __init__(self, config: CameraConfig):
        self.config = config
        self.status = CameraStatus()
        self.cap = None
        self.frame: Optional[np.ndarray] = None
        
        self._running = False
        self._thread = None
        self._lock = threading.Lock()
        self._new_source_requested = None
        self._paused = False
        self._video_fps = 30.0
        self.client_frame = None

    def start(self):
        """Kamera akışını başlatır."""
        if self._running:
            return
            
        self._connect()
        self._running = True
        self._thread = threading.Thread(target=self._update, daemon=True)
        self._thread.start()

    def _connect(self):
        """Kameraya bağlanır."""
        if self.cap is not None:
            self.cap.release()
            
        if self.config.source == "none":
            self.cap = None
            self.status.is_open = False
            return
            
        if self.config.source == "client":
            self.cap = None
            self.status.is_open = True
            return
            
        self.cap = cv2.VideoCapture(self.config.source)
        
        if isinstance(self.config.source, int):
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.height)
            self.cap.set(cv2.CAP_PROP_FPS, self.config.fps)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, self.config.buffer_size)
            self._video_fps = self.config.fps
        else:
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            self._video_fps = fps if fps > 0 else 30.0
            
        self.status.is_open = self.cap.isOpened()

    def _update(self):
        """Kareden kareye okuma yapan arka plan döngüsü."""
        prev_time = time.time()
        
        while self._running:
            if self._paused:
                time.sleep(0.1)
                continue
                
            if self._new_source_requested is not None:
                self.config.source = self._new_source_requested
                self._new_source_requested = None
                self._connect()

            if self.config.source == "none":
                with self._lock:
                    self.frame = None
                time.sleep(0.1)
                continue
                
            if self.config.source == "client":
                with self._lock:
                    if self.client_frame is not None:
                        self.frame = self.client_frame
                        self.client_frame = None
                time.sleep(0.05)
                continue

            if not self.status.is_open:
                time.sleep(1)
                self.status.reconnect_count += 1
                self._connect()
                continue
                
            ret, frame = self.cap.read()
            
            if not ret:
                self.status.is_open = False
                continue
                
            with self._lock:
                if self.frame is not None:
                    self.status.dropped_frames += 1
                self.frame = frame
                
            current_time = time.time()
            elapsed = current_time - prev_time
            target_delay = 1.0 / self._video_fps
            
            if not isinstance(self.config.source, int):
                sleep_time = target_delay - elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    current_time = time.time()
            
            self.status.fps = 1.0 / (current_time - prev_time)
            prev_time = current_time

    def read(self) -> Optional[np.ndarray]:
        """Güncel kareyi döndürür ve tamponu temizler (yeni kareyi beklemek için)."""
        with self._lock:
            frame = self.frame
            self.frame = None
            return frame

    def stop(self):
        """Kamera akışını durdurur."""
        self._running = False
        if self._thread:
            self._thread.join()
        if self.cap:
            self.cap.release()
        self.status.is_open = False

    def change_source(self, new_source):
        """Video kaynağını güvenli bir şekilde değiştirir."""
        self._new_source_requested = new_source
        self._paused = False  # Yeni video yüklendiğinde otomatik başlat
        
    def pause(self):
        """Akışı duraklatır."""
        self._paused = True
        
    def resume(self):
        """Akışı devam ettirir."""
        self._paused = False
        
    def receive_client_frame(self, frame):
        """İstemciden (tarayıcıdan) gelen kareyi alır."""
        with self._lock:
            self.client_frame = frame
            
    @property
    def is_paused(self):
        return self._paused
