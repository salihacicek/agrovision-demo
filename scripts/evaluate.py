import argparse
from ultralytics import YOLO

def main():
    parser = argparse.ArgumentParser(description="Agrovision AI - Model Değerlendirme")
    parser.add_argument("--model", type=str, required=True, help="Eğitilmiş model (.pt) yolu")
    parser.add_argument("--data", type=str, required=True, help="dataset.yaml dosyasının yolu")
    parser.add_argument("--split", type=str, default="test", help="Değerlendirilecek split (val veya test)")
    
    args = parser.parse_args()
    
    print(f"Değerlendirme başlatılıyor...")
    print(f"Model: {args.model}")
    print(f"Veriseti: {args.data} ({args.split})")
    
    model = YOLO(args.model)
    
    # Sınıf listesini kontrol et (Sadece Buğday ve Mısır olmalı)
    print("Sınıflar:", model.names)
    
    metrics = model.val(
        data=args.data,
        split=args.split,
        conf=0.25,      # Güven eşiği
        iou=0.6,        # NMS IOU eşiği
        save_json=True, # Sonuçları JSON olarak kaydet
        plots=True      # Confusion matrix ve eğrileri çiz
    )
    
    print("\n--- DEĞERLENDİRME SONUÇLARI ---")
    print(f"mAP50-95: {metrics.box.map:.4f}")
    print(f"mAP50:    {metrics.box.map50:.4f}")
    print(f"Precision: {metrics.box.mp:.4f}")
    print(f"Recall:   {metrics.box.mr:.4f}")
    print("-------------------------------")
    print("Detaylı grafikler ve confusion matrix runs/detect/val/ klasörüne kaydedildi.")

if __name__ == "__main__":
    main()
