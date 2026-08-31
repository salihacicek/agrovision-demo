"""
Agrovision AI - Verim Tahmin Modülü
Sağlık, kapsama ve yoğunluk verilerine dayanarak rekolte tahmini yapar.
"""

from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class YieldResult:
    """Verim tahmin sonuçlarını tutan veri sınıfı."""
    yield_score: float # 0-100 arası
    quality_category: str # DÜŞÜK, ORTA, İYİ, MÜKEMMEL
    
    def to_dict(self) -> Dict[str, Any]:
        """JSON formatında serileştirilebilir bir sözlük döndürür."""
        return {
            "yield_score": float(self.yield_score),
            "quality_category": self.quality_category
        }

class YieldEstimator:
    """Ürün verimini ve kalitesini tahmin eden sınıf."""
    
    def __init__(self, coverage_weight: float = 0.4, health_weight: float = 0.4, density_weight: float = 0.2):
        """
        Başlatıcı.
        
        Args:
            coverage_weight: Kapsama alanının verime etkisi.
            health_weight: Bitki sağlığının verime etkisi.
            density_weight: Yoğunluğun verime etkisi.
        """
        self.weights = {
            "coverage": coverage_weight,
            "health": health_weight,
            "density": density_weight
        }
        
    def estimate(self, coverage_percent: float, health_score: float, density_percent: float) -> YieldResult:
        """
        Verim tahminini hesaplar.
        
        Args:
            coverage_percent: Kapsama alanı yüzdesi (0-100)
            health_score: Genel sağlık puanı (0-100)
            density_percent: Yoğunluk yüzdesi (0-100)
            
        Returns:
            YieldResult: Verim tahmin sonucu.
        """
        yield_score = (
            coverage_percent * self.weights["coverage"] +
            health_score * self.weights["health"] +
            density_percent * self.weights["density"]
        )
        yield_score = max(0.0, min(100.0, yield_score))
        
        if yield_score < 40.0:
            category = "DÜŞÜK"
        elif yield_score < 65.0:
            category = "ORTA"
        elif yield_score < 85.0:
            category = "İYİ"
        else:
            category = "MÜKEMMEL"
            
        return YieldResult(yield_score=yield_score, quality_category=category)
