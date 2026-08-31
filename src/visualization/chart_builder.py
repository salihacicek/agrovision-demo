"""
Agrovision AI - Grafik Üretici
OpenCV kullanarak temel istatistik grafikleri oluşturur.
"""

import cv2
import numpy as np

class ChartBuilder:
    """Matplotlib yerine OpenCV çizim fonksiyonlarıyla basit grafikler oluşturan sınıf."""
    
    def __init__(self):
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.bg_color = (30, 30, 30)
        self.line_color = (50, 205, 50)  # Yeşil
        self.text_color = (255, 255, 255)
        
    def create_line_chart(self, data: list, width: int = 300, height: int = 150, title: str = "Trend") -> np.ndarray:
        """
        Basit bir çizgi grafiği (trend) oluşturur.
        
        Args:
            data: Sayısal değerler listesi (0-100 arası varsayılır).
            width: Grafik genişliği.
            height: Grafik yüksekliği.
            title: Grafik başlığı.
            
        Returns:
            np.ndarray: Grafik görüntüsü (BGR).
        """
        chart = np.full((height, width, 3), self.bg_color, dtype=np.uint8)
        
        cv2.putText(chart, title, (10, 20), self.font, 0.5, self.text_color, 1)
        
        if not data or len(data) < 2:
            cv2.putText(chart, "Yeterli veri yok", (10, height//2), self.font, 0.5, (100, 100, 100), 1)
            return chart
            
        pad = 30
        plot_w = width - 2 * pad
        plot_h = height - 2 * pad
        
        cv2.line(chart, (pad, height - pad), (width - pad, height - pad), (100, 100, 100), 1)
        cv2.line(chart, (pad, pad), (pad, height - pad), (100, 100, 100), 1)
        
        max_val = 100.0 
        
        points = []
        for i, val in enumerate(data):
            x = int(pad + (i / (len(data) - 1)) * plot_w)
            y = int(height - pad - (val / max_val) * plot_h)
            points.append((x, y))
            
        for i in range(1, len(points)):
            cv2.line(chart, points[i-1], points[i], self.line_color, 2)
            
        if points:
            last_val = data[-1]
            last_pt = points[-1]
            cv2.circle(chart, last_pt, 4, self.line_color, -1)
            cv2.putText(chart, f"%{last_val:.1f}", (last_pt[0] - 30, last_pt[1] - 10), self.font, 0.4, self.text_color, 1)
            
        return chart
        
    def create_bar_chart(self, data_dict: dict, width: int = 300, height: int = 150, title: str = "Dagilim") -> np.ndarray:
        """
        Basit bir çubuk grafiği oluşturur.
        
        Args:
            data_dict: {"Kategori": değer} sözlüğü.
            width: Genişlik.
            height: Yükseklik.
            title: Başlık.
            
        Returns:
            np.ndarray: Grafik görüntüsü.
        """
        chart = np.full((height, width, 3), self.bg_color, dtype=np.uint8)
        cv2.putText(chart, title, (10, 20), self.font, 0.5, self.text_color, 1)
        
        if not data_dict:
            return chart
            
        pad = 30
        plot_w = width - 2 * pad
        plot_h = height - 2 * pad
        
        keys = list(data_dict.keys())
        values = list(data_dict.values())
        max_val = max(100.0, max(values) if values else 100.0)
        
        bar_w = plot_w // len(keys)
        
        for i, (key, val) in enumerate(data_dict.items()):
            x = pad + i * bar_w + 10
            h = int((val / max_val) * plot_h)
            y = height - pad - h
            
            cv2.rectangle(chart, (x, y), (x + bar_w - 20, height - pad), (0, 150, 255), -1)
            cv2.putText(chart, key[:3], (x, height - 10), self.font, 0.4, self.text_color, 1)
            cv2.putText(chart, f"%{int(val)}", (x, y - 5), self.font, 0.4, self.text_color, 1)
            
        return chart
