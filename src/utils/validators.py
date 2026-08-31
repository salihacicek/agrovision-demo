import os
import numpy as np

def validate_frame(frame):
    """
    Görüntü karesinin geçerliliğini kontrol eder.
    
    Args:
        frame (np.ndarray): Kontrol edilecek görüntü karesi.
        
    Returns:
        bool: Kare geçerliyse True, değilse False.
    """
    if frame is None or not isinstance(frame, np.ndarray):
        return False
    if frame.size == 0 or len(frame.shape) < 2:
        return False
    return True

def validate_config(config: dict, required_keys: list):
    """
    Konfigürasyon sözlüğünün gerekli anahtarları içerip içermediğini kontrol eder.
    
    Args:
        config (dict): Kontrol edilecek konfigürasyon.
        required_keys (list): Gerekli anahtarların listesi.
        
    Returns:
        bool: Tüm gerekli anahtarlar varsa True.
    """
    for key in required_keys:
        if key not in config:
            return False
    return True

def validate_path(path: str, check_exists: bool = True):
    """
    Dosya veya dizin yolunu doğrular.
    
    Args:
        path (str): Kontrol edilecek yol.
        check_exists (bool): Yolun varlığını kontrol et.
        
    Returns:
        bool: Yol geçerliyse True.
    """
    if not path or not isinstance(path, str):
        return False
    if check_exists and not os.path.exists(path):
        return False
    return True

def validate_gps(lat: float, lon: float):
    """
    GPS koordinatlarının geçerliliğini kontrol eder.
    
    Args:
        lat (float): Enlem.
        lon (float): Boylam.
        
    Returns:
        bool: Koordinatlar geçerliyse True.
    """
    try:
        lat, lon = float(lat), float(lon)
        return -90 <= lat <= 90 and -180 <= lon <= 180
    except (ValueError, TypeError):
        return False
