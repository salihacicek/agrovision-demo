import logging
import logging.config
import yaml
import os
from pathlib import Path

class ColoredFormatter(logging.Formatter):
    """Konsol çıktıları için renklendirilmiş log formatlayıcı."""
    
    COLORS = {
        'WARNING': '\033[93m', # Sarı
        'INFO': '\033[92m',    # Yeşil
        'DEBUG': '\033[94m',   # Mavi
        'CRITICAL': '\033[91m',# Kırmızı
        'ERROR': '\033[91m'    # Kırmızı
    }
    RESET = '\033[0m'

    def format(self, record):
        log_message = super().format(record)
        return f"{self.COLORS.get(record.levelname, self.RESET)}{log_message}{self.RESET}"

def setup_logging(config_path="config/logging_config.yaml"):
    """
    Loglama sistemini yapılandırır.
    
    Args:
        config_path (str): Loglama konfigürasyon dosyasının yolu.
    """
    os.makedirs("logs", exist_ok=True)
    
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            # Renkli formatlayıcıyı ekle
            logging.config.dictConfig(config)
            
            # Konsol handler'ına renkli formatlayıcıyı ata
            for handler in logging.getLogger().handlers:
                if isinstance(handler, logging.StreamHandler) and not isinstance(handler, logging.FileHandler):
                    handler.setFormatter(ColoredFormatter(config['formatters']['colored']['format']))
    else:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        logging.warning(f"Log konfigürasyon dosyası bulunamadı: {config_path}. Varsayılan ayarlar kullanılıyor.")

def get_logger(name):
    """
    Belirtilen isimde bir logger döndürür.
    
    Args:
        name (str): Logger ismi.
    Returns:
        logging.Logger: Yapılandırılmış logger nesnesi.
    """
    return logging.getLogger(name)
