import uvicorn
import argparse
import sys
import os

# src klasörünü Python yoluna ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agrovision AI Dashboard Server")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Sunucu adresi")
    parser.add_argument("--port", type=int, default=8000, help="Sunucu portu")
    parser.add_argument("--reload", action="store_true", help="Kodu değiştirince otomatik yenile (Geliştirme için)")
    args = parser.parse_args()
    
    print("="*60)
    print(" 🌾 Agrovision AI - İzleme Paneli Başlatılıyor")
    print("="*60)
    print(f" 🌐 Tarayıcıdan açın: http://localhost:{args.port}")
    print("="*60)
    
    # Uvicorn üzerinden FastAPI uygulamasını çalıştır
    uvicorn.run("src.dashboard.app:app", host=args.port, port=args.port, reload=args.reload)
