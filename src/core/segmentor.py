import cv2
import numpy as np
from typing import List, Dict, Tuple
from .detector import DetectionResult
from ..utils.logger import get_logger

logger = get_logger(__name__)

class Segmentor:
    """Segmentasyon maskeleri üzerinde işlem yapan post-processor sınıfı."""
    
    def __init__(self, min_area: int = 100):
        """
        Args:
            min_area (int): Dikkate alınacak minimum maske alanı (piksel cinsinden).
        """
        self.min_area = min_area
        
    def refine_mask(self, mask: np.ndarray) -> np.ndarray:
        """
        Morfolojik işlemlerle maskeyi iyileştirir (gürültü azaltma, boşluk doldurma).
        
        Args:
            mask (np.ndarray): Girdi maskesi (ikili).
            
        Returns:
            np.ndarray: İyileştirilmiş maske.
        """
        kernel = np.ones((3, 3), np.uint8)
        # Açılma: küçük gürültüleri siler
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        # Kapanma: küçük boşlukları doldurur
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        return mask
        
    def extract_contours(self, mask: np.ndarray) -> List[np.ndarray]:
        """
        Maske üzerinden konturları çıkarır.
        
        Args:
            mask (np.ndarray): İkili maske.
            
        Returns:
            List[np.ndarray]: Kontur listesi.
        """
        contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        valid_contours = [c for c in contours if cv2.contourArea(c) > self.min_area]
        return valid_contours
        
    def calculate_coverage(self, detection_result: DetectionResult, frame_shape: Tuple[int, int]) -> Dict[int, float]:
        """
        Sınıf bazlı maske kapsama (coverage) oranını hesaplar.
        
        Args:
            detection_result (DetectionResult): Algılama sonuçları.
            frame_shape (Tuple[int, int]): Görüntü boyutu (Y, X).
            
        Returns:
            Dict[int, float]: Sınıf ID'sine göre kapsama oranları (0-1 arası).
        """
        coverage = {0: 0.0, 1: 0.0}
        
        if detection_result.masks is None or len(detection_result.masks) == 0:
            return coverage
            
        total_pixels = frame_shape[0] * frame_shape[1]
        
        for cls_id in [0, 1]:
            # İlgili sınıfa ait maskeleri al
            indices = np.where(detection_result.class_ids == cls_id)[0]
            if len(indices) == 0:
                continue
                
            class_masks = detection_result.masks[indices]
            # Tüm maskeleri birleştir (mantıksal VEYA)
            combined_mask = np.any(class_masks > 0.5, axis=0).astype(np.uint8)
            
            # Maskeyi orijinal boyuta yeniden ölçeklendir (eğer farklıysa)
            if combined_mask.shape != frame_shape[:2]:
                combined_mask = cv2.resize(combined_mask, (frame_shape[1], frame_shape[0]), interpolation=cv2.INTER_NEAREST)
                
            refined_mask = self.refine_mask(combined_mask)
            mask_area = np.count_nonzero(refined_mask)
            coverage[cls_id] = mask_area / total_pixels
            
        return coverage
