import os
import urllib.request
from typing import Callable, Optional
from ..utils.logger import get_logger

logger = get_logger(__name__)

class ModelManager:
    """Model dosyalarının yaşam döngüsünü yöneten sınıf."""
    
    def __init__(self, models_dir: str = "models"):
        """
        Args:
            models_dir (str): Modellerin saklanacağı dizin.
        """
        self.models_dir = models_dir
        os.makedirs(self.models_dir, exist_ok=True)
        
    def download_model(self, url: str, model_name: str, progress_callback: Optional[Callable[[int, int], None]] = None) -> str:
        """
        Model ağırlıklarını indirir.
        
        Args:
            url (str): Model indirme URL'si.
            model_name (str): Kaydedilecek model adı (örn: best.pt).
            progress_callback (Callable): İndirme ilerlemesini bildirmek için callback.
            
        Returns:
            str: İndirilen modelin dosya yolu.
        """
        model_path = os.path.join(self.models_dir, model_name)
        
        if os.path.exists(model_path):
            logger.info(f"Model zaten mevcut: {model_path}")
            return model_path
            
        logger.info(f"Model indiriliyor: {url} -> {model_path}")
        
        def reporthook(block_num, block_size, total_size):
            if progress_callback:
                downloaded = block_num * block_size
                progress_callback(downloaded, total_size)
                
        try:
            urllib.request.urlretrieve(url, model_path, reporthook)
            logger.info("Model indirme tamamlandı.")
            return model_path
        except Exception as e:
            logger.error(f"Model indirilirken hata oluştu: {str(e)}")
            if os.path.exists(model_path):
                os.remove(model_path) # Hatalı dosyayı temizle
            raise
            
    def get_model_info(self, model_path: str) -> dict:
        """
        Model metadatasını döndürür.
        
        Args:
            model_path (str): Model dosyasının yolu.
            
        Returns:
            dict: Model bilgileri.
        """
        return {
            "name": os.path.basename(model_path),
            "size_mb": round(os.path.getsize(model_path) / (1024 * 1024), 2) if os.path.exists(model_path) else 0,
            "classes": ["Buğday", "Mısır"],
            "framework": "Ultralytics YOLO11"
        }
