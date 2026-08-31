from dataclasses import dataclass
from typing import List, Dict, Any
from collections import deque
import numpy as np

@dataclass
class AggregatedResult:
    dominant_crop: str
    avg_health: float
    avg_coverage: float
    trend: str  # increasing, decreasing, stable
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "dominant_crop": self.dominant_crop,
            "avg_health": self.avg_health,
            "avg_coverage": self.avg_coverage,
            "trend": self.trend
        }

class ResultAggregator:
    """Zaman pencereli sonuç toplayıcı."""
    
    def __init__(self, window_size: int = 30):
        self.window_size = window_size
        self.history = deque(maxlen=window_size)

    def reset(self):
        self.history.clear()

    def add_result(self, crop_type: str, health: float, coverage: float):
        """Yeni bir sonucu geçmişe ekler."""
        self.history.append({
            "crop_type": crop_type,
            "health": health,
            "coverage": coverage
        })

    def get_aggregated(self) -> AggregatedResult:
        """Pencere içindeki verilerin özetini döndürür."""
        if not self.history:
            return AggregatedResult("Bilinmiyor", 0.0, 0.0, "stable")

        crops = [item["crop_type"] for item in self.history]
        healths = [item["health"] for item in self.history]
        coverages = [item["coverage"] for item in self.history]

        dominant_crop = max(set(crops), key=crops.count)
        avg_health = np.mean(healths)
        avg_coverage = np.mean(coverages)
        
        # Basit trend analizi
        trend = "stable"
        if len(coverages) >= 10:
            first_half = np.mean(coverages[:len(coverages)//2])
            second_half = np.mean(coverages[len(coverages)//2:])
            if second_half > first_half + 5:
                trend = "increasing"
            elif second_half < first_half - 5:
                trend = "decreasing"

        return AggregatedResult(
            dominant_crop=dominant_crop,
            avg_health=float(avg_health),
            avg_coverage=float(avg_coverage),
            trend=trend
        )
