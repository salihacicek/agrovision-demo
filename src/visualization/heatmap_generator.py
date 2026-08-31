"""
Agrovision AI - Heatmap Üretici
Indeks haritalarını ve yoğunluk haritalarını renkli ısı haritalarına dönüştürür.
"""

import cv2
import numpy as np

class HeatmapGenerator:
    """Farklı veriler için renkli ısı haritaları (heatmap) üreten sınıf."""
    
    @staticmethod
    def generate_from_index(index_map: np.ndarray, colormap=cv2.COLORMAP_JET) -> np.ndarray:
        """
        Sayısal bir indeks haritasını heatmap'e dönüştürür.
        
        Args:
            index_map: Sayısal 2B array.
            colormap: OpenCV Colormap sabiti.
            
        Returns:
            np.ndarray: BGR formatında renkli heatmap.
        """
        min_val, max_val = np.min(index_map), np.max(index_map)
        if max_val == min_val:
            normalized = np.zeros_like(index_map, dtype=np.uint8)
        else:
            normalized = ((index_map - min_val) / (max_val - min_val) * 255).astype(np.uint8)
            
        return cv2.applyColorMap(normalized, colormap)
        
    @staticmethod
    def blend_with_frame(frame: np.ndarray, heatmap: np.ndarray, alpha: float = 0.5) -> np.ndarray:
        """
        Orijinal görüntü ile heatmap'i harmanlar.
        
        Args:
            frame: Orijinal kare (BGR).
            heatmap: Renkli ısı haritası (BGR).
            alpha: Heatmap saydamlığı (0.0 - 1.0).
            
        Returns:
            np.ndarray: Birleştirilmiş görüntü.
        """
        if frame.shape != heatmap.shape:
            heatmap = cv2.resize(heatmap, (frame.shape[1], frame.shape[0]))
        return cv2.addWeighted(heatmap, alpha, frame, 1 - alpha, 0)
