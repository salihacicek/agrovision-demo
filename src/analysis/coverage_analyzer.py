"""
Agrovision AI - Kapsama Alanı Analiz Modülü
Buğday ve mısırın piksel bazlı alan kaplama analizi.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class CoverageResult:
    """Kapsama alanı analiz sonuçlarını tutan veri sınıfı."""
    total_coverage_percent: float
    wheat_coverage_percent: float
    corn_coverage_percent: float
    coverage_trend: List[float]
    
    def to_dict(self) -> Dict[str, Any]:
        """JSON formatında serileştirilebilir bir sözlük döndürür."""
        return {
            "total_coverage_percent": float(self.total_coverage_percent),
            "wheat_coverage_percent": float(self.wheat_coverage_percent),
            "corn_coverage_percent": float(self.corn_coverage_percent),
            "coverage_trend": [float(x) for x in self.coverage_trend]
        }

class CoverageAnalyzer:
    """Görüntüdeki ekin kaplama oranını hesaplayan sınıf."""
    
    def __init__(self, history_size: int = 30):
        """
        Başlatıcı.
        
        Args:
            history_size: Trend analizi için tutulacak geçmiş kare sayısı.
        """
        self.history_size = history_size
        self.coverage_history: List[float] = []
        
    def analyze(self, frame_shape: tuple, wheat_mask: np.ndarray, corn_mask: np.ndarray) -> CoverageResult:
        """
        Verilen maskeler üzerinden ekinlerin kapsama alanını hesaplar.
        
        Args:
            frame_shape: Görüntü boyutları (H, W, C)
            wheat_mask: Buğday piksellerini içeren ikili (binary) maske
            corn_mask: Mısır piksellerini içeren ikili (binary) maske
            
        Returns:
            CoverageResult: Kapsama alanı analiz sonuçları.
        """
        total_pixels = frame_shape[0] * frame_shape[1]
        if total_pixels == 0:
            return CoverageResult(0.0, 0.0, 0.0, self.coverage_history.copy())
            
        wheat_pixels = np.sum(wheat_mask > 0)
        corn_pixels = np.sum(corn_mask > 0)
        
        wheat_percent = (wheat_pixels / total_pixels) * 100.0
        corn_percent = (corn_pixels / total_pixels) * 100.0
        total_percent = min(100.0, wheat_percent + corn_percent)
        
        # Trend analizi için geçmişe ekle
        self.coverage_history.append(total_percent)
        if len(self.coverage_history) > self.history_size:
            self.coverage_history.pop(0)
            
        return CoverageResult(
            total_coverage_percent=total_percent,
            wheat_coverage_percent=wheat_percent,
            corn_coverage_percent=corn_percent,
            coverage_trend=self.coverage_history.copy()
        )
