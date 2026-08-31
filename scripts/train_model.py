import os
import sys
import torch
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ultralytics import YOLO
from src.utils.logger import get_logger

logger = get_logger(__name__)

def train_model():
    """YOLOv8/11 segmentasyon modelini eğitir."""
    
    # MPS/CUDA kontrolü
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    logger.info(f"Eğitim için cihaz seçildi: {device}")
    
    # Model (Segmentasyon yerine normal Nesne Algılama modeli kullanıyoruz çünkü kutu çizen fotoğraflar da var)
    model_name = "yolov8n.pt"
    logger.info(f"Model yükleniyor: {model_name}")
    model = YOLO(model_name)
    
    # Veri seti yolu
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "roboflow", "data.yaml"))
    
    if not os.path.exists(data_path):
        logger.error(f"Veri seti bulunamadı: {data_path}")
        return
        
    logger.info("Eğitim başlıyor...")
    
    # Eğitim parametreleri
    # 520 fotoğraf için 30 epoch başlangıç için ideal (hızlı sonuç verir)
    results = model.train(
        data=data_path,
        epochs=30,
        imgsz=512,
        batch=16,
        device=device,
        project="runs/detect",
        name="agro_train",
        exist_ok=True # Aynı isimde varsa üzerine yazar
    )
    
    logger.info("Eğitim tamamlandı!")
    logger.info(f"En iyi model şuraya kaydedildi: runs/detect/agro_train/weights/best.pt")

if __name__ == "__main__":
    train_model()
