"""
Agrovision AI - Arayüz Görselleştirici (Overlay Renderer)
Görüntü üzerine profesyonel UI katmanı ekler.
"""

import cv2
import numpy as np
from datetime import datetime

class OverlayRenderer:
    """Görüntü üzerine bilgileri ve panelleri çizen sınıf."""
    
    def __init__(self):
        self.dark_bg = (20, 25, 20)  # Koyu gri/yeşil arka plan
        self.green_accent = (50, 205, 50)  # Canlı yeşil vurgu
        self.yellow_accent = (0, 215, 255)  # Mısır/sınır sarısı
        self.white = (255, 255, 255)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        
    def render(self, frame: np.ndarray, info_dict: dict, masks: dict = None) -> np.ndarray:
        """
        Kare üzerine arayüz katmanını çizer.
        
        Args:
            frame: Orijinal görüntü (BGR).
            info_dict: Ekranda gösterilecek bilgileri içeren sözlük.
            masks: Sınıf maskeleri {"wheat": mask, "corn": mask}.
            
        Returns:
            np.ndarray: İşlenmiş ve arayüz eklenmiş görüntü.
        """
        h, w = frame.shape[:2]
        output = frame.copy()
        
        # 1. Yarı saydam maskeleri ve konturları ekle
        if masks:
            overlay = output.copy()
            
            if "wheat" in masks and masks["wheat"] is not None:
                wheat_mask = masks["wheat"] > 0
                overlay[wheat_mask] = overlay[wheat_mask] * 0.5 + np.array((0, 255, 0)) * 0.5
                
                # Kontur (Sınır çizgisi) - Sarı renk
                contours, _ = cv2.findContours(masks["wheat"].astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cv2.drawContours(output, contours, -1, self.yellow_accent, 2)
                
            if "corn" in masks and masks["corn"] is not None:
                corn_mask = masks["corn"] > 0
                overlay[corn_mask] = overlay[corn_mask] * 0.5 + np.array((0, 215, 255)) * 0.5
                
                # Kontur
                contours, _ = cv2.findContours(masks["corn"].astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cv2.drawContours(output, contours, -1, self.yellow_accent, 2)
                
            cv2.addWeighted(overlay, 0.6, output, 0.4, 0, output)

        # 2. Üst Header Paneli (OTENELABS AGROVISION AI)
        cv2.rectangle(output, (0, 0), (w, 50), self.dark_bg, -1)
        cv2.putText(output, "OTENELABS AGROVISION AI", (15, 33), self.font, 1.0, self.white, 2)
        
        time_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        cv2.putText(output, time_str, (w - 250, 33), self.font, 0.6, self.white, 1)

        # 3. Sol Bilgi Paneli
        panel_w = 350
        # Opak arka plan (saydamlık yerine)
        cv2.rectangle(output, (0, 50), (panel_w, h), self.dark_bg, -1)
        
        y_offset = 90
        cv2.putText(output, "ANALIZ DETAYLARI", (15, y_offset), self.font, 0.7, self.green_accent, 2)
        y_offset += 40
        
        # Crop Type (Tespit Edilen Tür)
        crop_type = info_dict.get("crop_type", "Bilinmiyor")
        conf = info_dict.get("confidence", 0.0)
        cv2.putText(output, f"Ekin: {crop_type} (%{conf:.1f})", (15, y_offset), self.font, 0.6, self.white, 1)
        y_offset += 30
        
        # Coverage (Kapsama)
        coverage = info_dict.get("coverage", 0.0)
        cv2.putText(output, f"Kapsama Alani: %{coverage:.1f}", (15, y_offset), self.font, 0.6, self.white, 1)
        y_offset += 30
        
        # Density (Yoğunluk)
        density = info_dict.get("density_level", "BELIRSIZ")
        cv2.putText(output, f"Yogunluk: {density}", (15, y_offset), self.font, 0.6, self.white, 1)
        y_offset += 30
        
        # Health Score (Sağlık Skoru)
        health = info_dict.get("health_score", 0.0)
        cv2.putText(output, f"Saglik Puani: {health:.1f}/100", (15, y_offset), self.font, 0.6, self.white, 1)
        y_offset += 30
        
        # Yield Estimate (Verim Tahmini)
        yield_cat = info_dict.get("yield_category", "BELIRSIZ")
        cv2.putText(output, f"Tahmini Verim: {yield_cat}", (15, y_offset), self.font, 0.6, self.white, 1)
        y_offset += 50
        
        # 4. FPS & GNSS Info (Sol Alt)
        fps = info_dict.get("fps", 0)
        cv2.putText(output, f"FPS: {fps:.1f}", (15, h - 50), self.font, 0.6, self.green_accent, 1)
        gnss = info_dict.get("gnss", "Veri Yok")
        cv2.putText(output, f"GNSS: {gnss}", (15, h - 20), self.font, 0.5, self.white, 1)

        # 5. Sağ Alt Durum Rozeti (Sistem Durumu)
        status = info_dict.get("status", "AKTIF")
        status_size, _ = cv2.getTextSize(f"SISTEM: {status}", self.font, 0.6, 2)
        cv2.rectangle(output, (w - status_size[0] - 30, h - 40), (w, h), self.dark_bg, -1)
        cv2.putText(output, f"SISTEM: {status}", (w - status_size[0] - 15, h - 15), self.font, 0.6, self.green_accent, 2)
        
        # 6. Mini Sağlık Heatmap (Sağ Üst Köşe)
        heatmap = info_dict.get("heatmap_mini", None)
        if heatmap is not None:
            hm_h, hm_w = heatmap.shape[:2]
            output[60:60+hm_h, w-hm_w-10:w-10] = heatmap
            cv2.rectangle(output, (w-hm_w-10, 60), (w-10, 60+hm_h), self.white, 1)
            cv2.putText(output, "EksGR Indeksi", (w-hm_w-10, 55), self.font, 0.4, self.white, 1)
            
        return output
