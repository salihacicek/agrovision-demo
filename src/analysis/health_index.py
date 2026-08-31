"""
Agrovision AI - Bitki Sağlık İndeksi Modülü
RGB görüntüler üzerinden vejetasyon indekslerinin hesaplanması.
"""

import cv2
import numpy as np
from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class HealthIndexResult:
    """Bitki sağlık indeksi sonuçlarını tutan veri sınıfı."""
    overall_health_score: float
    exg_mean: float
    exr_mean: float
    exgr_mean: float
    vari_mean: float
    gli_mean: float
    rgbvi_mean: float
    heatmap_colored: Optional[np.ndarray] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """JSON formatında serileştirilebilir bir sözlük döndürür."""
        return {
            "overall_health_score": float(self.overall_health_score),
            "exg_mean": float(self.exg_mean),
            "exr_mean": float(self.exr_mean),
            "exgr_mean": float(self.exgr_mean),
            "vari_mean": float(self.vari_mean),
            "gli_mean": float(self.gli_mean),
            "rgbvi_mean": float(self.rgbvi_mean)
        }

class HealthIndexCalculator:
    """RGB görüntüler üzerinden 6 farklı bitki sağlık indeksini hesaplayan sınıf."""
    
    def __init__(self, epsilon: float = 1e-6):
        """
        Başlatıcı.
        
        Args:
            epsilon: Sıfıra bölmeyi engellemek için küçük bir değer.
        """
        self.epsilon = epsilon
        
    def calculate(self, frame: np.ndarray, mask: Optional[np.ndarray] = None) -> HealthIndexResult:
        """
        Verilen kare (ve varsa maske) üzerinde sağlık indekslerini hesaplar.
        
        Args:
            frame: Girdi görüntüsü (BGR formatında).
            mask: İsteğe bağlı, sadece belirli pikselleri değerlendirmek için maske.
            
        Returns:
            HealthIndexResult: Sağlık indeksi sonuçları.
        """
        # BGR'dan RGB'ye çevir ve normalize et (0-1)
        # OpenCV resimleri BGR okuduğu için kanalları ayırıyoruz
        b, g, r = cv2.split(frame.astype(np.float32) / 255.0)
        
        # ExG (Excess Green Index) = 2*g - r - b
        exg = 2 * g - r - b
        
        # ExR (Excess Red Index) = 1.4*r - g
        exr = 1.4 * r - g
        
        # ExGR = ExG - ExR
        exgr = exg - exr
        
        # VARI (Visible Atmospherically Resistant Index) = (g - r) / (g + r - b + epsilon)
        vari = (g - r) / (g + r - b + self.epsilon)
        
        # GLI (Green Leaf Index) = (2*g - r - b) / (2*g + r + b + epsilon)
        gli = (2 * g - r - b) / (2 * g + r + b + self.epsilon)
        
        # RGBVI (RGB Vegetation Index) = (g*g - r*b) / (g*g + r*b + self.epsilon)
        rgbvi = (g * g - r * b) / (g * g + r * b + self.epsilon)
        
        # Sadece maske içindeki pikselleri değerlendir
        if mask is not None:
            # Maske 2B (H,W) olduğunu varsayıyoruz
            valid_pixels = mask > 0
            if not np.any(valid_pixels):
                return self._empty_result()
            
            exg_mean = np.mean(exg[valid_pixels])
            exr_mean = np.mean(exr[valid_pixels])
            exgr_mean = np.mean(exgr[valid_pixels])
            vari_mean = np.mean(vari[valid_pixels])
            gli_mean = np.mean(gli[valid_pixels])
            rgbvi_mean = np.mean(rgbvi[valid_pixels])
            
            # Heatmap oluştur (maskelenmiş alanlar için ExGR baz alınarak)
            exgr_norm = np.clip((exgr + 1) / 2 * 255, 0, 255).astype(np.uint8)
            heatmap_colored = cv2.applyColorMap(exgr_norm, cv2.COLORMAP_JET)
            # Maske dışındaki kısımları siyah yap
            heatmap_colored[~valid_pixels] = 0
            
        else:
            exg_mean = np.mean(exg)
            exr_mean = np.mean(exr)
            exgr_mean = np.mean(exgr)
            vari_mean = np.mean(vari)
            gli_mean = np.mean(gli)
            rgbvi_mean = np.mean(rgbvi)
            
            exgr_norm = np.clip((exgr + 1) / 2 * 255, 0, 255).astype(np.uint8)
            heatmap_colored = cv2.applyColorMap(exgr_norm, cv2.COLORMAP_JET)
        
        # Genel bitki sağlık puanı (0-100 aralığında bir ağırlıklı ortalama varsayımı)
        score = (np.clip(exg_mean, 0, 1) * 40 + np.clip(vari_mean + 0.5, 0, 1) * 30 + np.clip(gli_mean + 0.5, 0, 1) * 30)
        overall_score = np.clip(score, 0, 100)
        
        return HealthIndexResult(
            overall_health_score=overall_score,
            exg_mean=exg_mean,
            exr_mean=exr_mean,
            exgr_mean=exgr_mean,
            vari_mean=vari_mean,
            gli_mean=gli_mean,
            rgbvi_mean=rgbvi_mean,
            heatmap_colored=heatmap_colored
        )
        
    def _empty_result(self) -> HealthIndexResult:
        """Boş sonuç döner."""
        return HealthIndexResult(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, None)
