import functools
import traceback
import signal
from typing import Callable, Any
from .logger import get_logger

logger = get_logger(__name__)

def safe_execute(fallback_value: Any = None):
    """
    Fonksiyonları güvenli bir şekilde çalıştırmak için dekoratör.
    Hata durumunda loglar ve fallback_value döndürür.
    
    Args:
        fallback_value: Hata durumunda döndürülecek varsayılan değer.
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"{func.__name__} çalıştırılırken hata oluştu: {str(e)}")
                logger.debug(traceback.format_exc())
                return fallback_value
        return wrapper
    return decorator

class GracefulKiller:
    """SIGINT ve SIGTERM sinyallerini yakalayarak güvenli kapanış sağlar."""
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, *args):
        logger.info("Güvenli kapanış sinyali alındı. Kapatılıyor...")
        self.kill_now = True
