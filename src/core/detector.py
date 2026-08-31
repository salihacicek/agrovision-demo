import torch
import numpy as np
from dataclasses import dataclass
from typing import Optional
from ultralytics import YOLO
from ..utils.logger import get_logger
from ..utils.error_handler import safe_execute

logger = get_logger(__name__)

@dataclass
class DetectionResult:
    """Algılama sonuçlarını tutan veri sınıfı."""
    boxes: np.ndarray       # [N, 4] formatında bounding box'lar (xyxy)
    confidences: np.ndarray # [N] formatında güven skorları
    class_ids: np.ndarray   # [N] formatında sınıf ID'leri
    masks: Optional[np.ndarray] = None # [N, H, W] formatında maskeler
    
class Detector:
    """YOLO11 tabanlı nesne tespiti ve segmentasyon sınıfı."""
    
    def __init__(self, model_path: str, conf_thres: float = 0.5, iou_thres: float = 0.45):
        """
        Args:
            model_path (str): Model dosyasının yolu (.pt).
            conf_thres (float): Güven eşiği.
            iou_thres (float): NMS için IoU eşiği.
        """
        self.model_path = model_path
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        self.device = self._select_device()
        self.model = None
        self.classes = {0: "arpa", 1: "ayc", 2: "bugday", 3: "misir"}
        
        self.load_model()
        
    def _select_device(self) -> str:
        """Kullanılabilir en iyi cihazı seçer (MPS > CUDA > CPU)."""
        if torch.backends.mps.is_available():
            return "mps"
        elif torch.cuda.is_available():
            return "cuda"
        return "cpu"
        
    def load_model(self):
        """Modeli yükler ve GPU'ya/MPS'e gönderir."""
        try:
            logger.info(f"Model yükleniyor: {self.model_path} (Cihaz: {self.device})")
            self.model = YOLO(self.model_path)
            self.model.to(self.device)
            # Warm-up (ilk tahmini yaparak motoru ısıt)
            dummy_img = np.zeros((640, 640, 3), dtype=np.uint8)
            self.model(dummy_img, verbose=False)
            logger.info("Model başarıyla yüklendi ve ısıtıldı.")
        except Exception as e:
            logger.error(f"Model yüklenirken hata oluştu: {str(e)}")
            raise
            
    @safe_execute(fallback_value=DetectionResult(np.array([]), np.array([]), np.array([])))
    def predict(self, frame: np.ndarray) -> DetectionResult:
        """
        Görüntü üzerinde tahmin yapar.
        
        Args:
            frame (np.ndarray): İşlenecek görüntü (BGR).
            
        Returns:
            DetectionResult: Algılama sonuçları.
        """
        if self.model is None:
            logger.warning("Model yüklü değil, tahmin yapılamıyor.")
            return DetectionResult(np.array([]), np.array([]), np.array([]))
            
        # Model tahmini
        results = self.model(frame, conf=self.conf_thres, iou=self.iou_thres, verbose=False)
        result = results[0]
        
        # Sonuçları ayrıştır
        boxes = result.boxes.xyxy.cpu().numpy()
        confidences = result.boxes.conf.cpu().numpy()
        class_ids = result.boxes.cls.cpu().numpy().astype(int)
        
        masks = None
        if result.masks is not None:
            masks = result.masks.data.cpu().numpy()
            
        # Tüm geçerli sınıfları filtrele (0: arpa, 1: ayc, 2: bugday, 3: misir)
        valid_indices = np.isin(class_ids, [0, 1, 2, 3])
        
        filtered_masks = masks[valid_indices] if masks is not None else None
        
        return DetectionResult(
            boxes=boxes[valid_indices],
            confidences=confidences[valid_indices],
            class_ids=class_ids[valid_indices],
            masks=filtered_masks
        )
