import argparse
import os
from ultralytics import YOLO

def main():
    parser = argparse.ArgumentParser(description="Agrovision AI - Model Eğitimi (Buğday/Mısır)")
    parser.add_argument("--data", type=str, required=True, help="dataset.yaml dosyasının yolu")
    parser.add_argument("--model", type=str, default="yolov8n.pt", help="Başlangıç modeli (örn: yolov8n.pt)")
    parser.add_argument("--epochs", type=int, default=100, help="Eğitim epoch sayısı")
    parser.add_argument("--imgsz", type=int, default=640, help="Görüntü boyutu")
    parser.add_argument("--batch", type=int, default=16, help="Batch boyutu")
    parser.add_argument("--name", type=str, default="agrovision_model", help="Eğitim çalıştırması için isim")
    
    args = parser.parse_args()
    
    print(f"Eğitim başlıyor: {args.name}")
    print(f"Model: {args.model}, Veriseti: {args.data}")
    
    # Modeli yükle
    model = YOLO(args.model)
    
    # Tarımsal sahneler için veri artırma (augmentation) parametreleriyle eğitim
    results = model.train(
        data=args.data,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        name=args.name,
        device="cpu", # Mac için MPS veya CPU
        
        # Tarım sahaları için özel artırmalar
        hsv_h=0.015,  # Renk tonu
        hsv_s=0.7,    # Doygunluk (Güneş/Gölge farkları için)
        hsv_v=0.4,    # Parlaklık
        degrees=10.0, # Hafif rotasyon
        translate=0.1,
        scale=0.5,
        shear=2.0,
        flipud=0.0,   # Yukarı-aşağı çevirme (genelde dron değilse 0)
        fliplr=0.5,   # Sağ-sol çevirme
        mosaic=1.0,
        mixup=0.1
    )
    
    print(f"Eğitim tamamlandı. En iyi model 'runs/detect/{args.name}/weights/best.pt' konumuna kaydedildi.")

if __name__ == "__main__":
    main()
