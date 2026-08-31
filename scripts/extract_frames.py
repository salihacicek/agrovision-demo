import cv2
import os
import argparse

def extract_frames(video_path, output_dir, frame_interval=30):
    """
    Videodan belirli aralıklarla fotoğraf kareleri çıkartır.
    
    Args:
        video_path: İşlenecek videonun yolu
        output_dir: Fotoğrafların kaydedileceği klasör
        frame_interval: Kaç karede bir fotoğraf alınacağı (örn: 30 FPS bir videoda 30 yazılırsa saniyede 1 fotoğraf alır)
    """
    if not os.path.exists(video_path):
        print(f"Hata: Video bulunamadı -> {video_path}")
        return

    os.makedirs(output_dir, exist_ok=True)
    
    # Videoyu aç
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Hata: Video açılamadı.")
        return

    # Video bilgilerini al
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Video yüklendi: {video_path}")
    print(f"FPS: {fps} | Toplam Kare: {total_frames}")
    
    # Saniyede 1 kare almak için interval'i FPS'e eşitleyebiliriz (Eğer kullanıcı girmediyse)
    if frame_interval == -1:
        frame_interval = fps

    count = 0
    saved_count = 0
    
    # Dosya isimlendirmesi için videonun adını al
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Sadece belirlenen aralıktaki kareleri kaydet
        if count % frame_interval == 0:
            output_path = os.path.join(output_dir, f"{video_name}_frame_{saved_count:04d}.jpg")
            cv2.imwrite(output_path, frame)
            saved_count += 1
            
            # Konsolda ilerlemeyi göster
            if saved_count % 10 == 0:
                print(f"Çıkarılan fotoğraf sayısı: {saved_count} ...")
                
        count += 1

    cap.release()
    print("="*40)
    print(f"İşlem Tamamlandı! Toplam {saved_count} adet fotoğraf çıkartıldı.")
    print(f"Fotoğraflar şu klasöre kaydedildi: {output_dir}")
    print("="*40)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Videodan Eğitim İçin Fotoğraf Çıkarma Aracı")
    parser.add_argument("--video", type=str, required=True, help="Çevrilecek videonun tam yolu")
    parser.add_argument("--out", type=str, default="data/raw_frames", help="Fotoğrafların kaydedileceği klasör")
    parser.add_argument("--interval", type=int, default=-1, help="Kaç karede bir alınacağı (Örn: Saniyede 1 kare için video FPS değeri girilir. Varsayılan: saniyede 1)")
    
    args = parser.parse_args()
    extract_frames(args.video, args.out, args.interval)
