import time
import psutil
from collections import deque

class PerformanceMonitor:
    """Sistem performansını ve FPS'i izleyen sınıf."""
    
    def __init__(self, history_size=30):
        """
        Args:
            history_size (int): FPS hesaplaması için tutulacak geçmiş frame sayısı.
        """
        self.history_size = history_size
        self.frame_times = deque(maxlen=history_size)
        self.start_time = None
        
    def start_frame(self):
        """Kare işleme başlangıcını kaydeder."""
        self.start_time = time.time()
        
    def end_frame(self):
        """Kare işleme bitişini kaydeder ve süreyi ekler."""
        if self.start_time is not None:
            self.frame_times.append(time.time() - self.start_time)
            
    def get_fps(self):
        """
        Ortalama FPS'i hesaplar.
        
        Returns:
            float: Saniyedeki kare sayısı (FPS).
        """
        if not self.frame_times:
            return 0.0
        avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        return 1.0 / avg_frame_time if avg_frame_time > 0 else 0.0
        
    def get_memory_usage(self):
        """
        Mevcut bellek kullanımını döndürür.
        
        Returns:
            float: Kullanılan bellek (MB).
        """
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024
        
    def get_report(self):
        """
        Kapsamlı performans raporu oluşturur.
        
        Returns:
            dict: Performans metriklerini içeren sözlük.
        """
        return {
            "fps": round(self.get_fps(), 2),
            "memory_mb": round(self.get_memory_usage(), 2),
            "cpu_percent": psutil.cpu_percent(),
            "avg_frame_time_ms": round((sum(self.frame_times) / len(self.frame_times)) * 1000, 2) if self.frame_times else 0
        }
