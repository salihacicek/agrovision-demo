"""
Agrovision AI - Yoğunluk Hesaplama Modülü
Ekinlerin bölgesel yoğunluk analizini yapar.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class DensityResult:
    """Yoğunluk analiz sonuçlarını tutan veri sınıfı."""
    density_level: str  # DÜŞÜK, ORTA, YÜKSEK
    density_percent: float
    density_map: np.ndarray
    histogram_data: Dict[str, float]
    
    def to_dict(self) -> Dict[str, Any]:
        """JSON formatında serileştirilebilir bir sözlük döndürür."""
        return {
            "density_level": self.density_level,
            "density_percent": float(self.density_percent),
            "histogram_data": {k: float(v) for k, v in self.histogram_data.items()}
        }

class DensityCalculator:
    """Ekin yoğunluğunu grid tabanlı hesaplayan sınıf."""
    
    def __init__(self, grid_size: int = 10):
        """
        Başlatıcı.
        
        Args:
            grid_size: Görüntünün kaça kaçlık gridlere bölüneceği.
        """
        self.grid_size = grid_size
        
    def calculate(self, frame_shape: tuple, mask: np.ndarray) -> DensityResult:
        """
        Verilen maske üzerinden yoğunluk haritasını ve seviyesini hesaplar.
        
        Args:
            frame_shape: Görüntü boyutları (H, W)
            mask: Ekinlerin genel maskesi (1 ekin, 0 arka plan)
            
        Returns:
            DensityResult: Yoğunluk analiz sonuçları.
        """
        h, w = mask.shape
        cell_h = h // self.grid_size
        cell_w = w // self.grid_size
        
        density_map = np.zeros((self.grid_size, self.grid_size), dtype=np.float32)
        
        total_density = 0.0
        
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                y_start, y_end = i * cell_h, (i + 1) * cell_h
                x_start, x_end = j * cell_w, (j + 1) * cell_w
                
                cell_mask = mask[y_start:y_end, x_start:x_end]
                cell_pixels = cell_mask.size
                if cell_pixels > 0:
                    active_pixels = np.sum(cell_mask > 0)
                    density = (active_pixels / cell_pixels) * 100.0
                else:
                    density = 0.0
                    
                density_map[i, j] = density
                total_density += density
                
        avg_density = total_density / (self.grid_size * self.grid_size)
        
        if avg_density < 30.0:
            level = "DÜŞÜK"
        elif avg_density < 60.0:
            level = "ORTA"
        else:
            level = "YÜKSEK"
            
        low_cells = np.sum(density_map < 30)
        med_cells = np.sum((density_map >= 30) & (density_map < 60))
        high_cells = np.sum(density_map >= 60)
        total_cells = self.grid_size * self.grid_size
        
        histogram_data = {
            "DÜŞÜK": (low_cells / total_cells) * 100,
            "ORTA": (med_cells / total_cells) * 100,
            "YÜKSEK": (high_cells / total_cells) * 100
        }
        
        return DensityResult(
            density_level=level,
            density_percent=avg_density,
            density_map=density_map,
            histogram_data=histogram_data
        )
