import time
import argparse
import numpy as np
import cv2
from ultralytics import YOLO

def benchmark(model_path, image_size, num_iterations=100):
    print(f"\nBenchmarking model: {model_path} | Image Size: {image_size}")
    
    try:
        model = YOLO(model_path)
    except Exception as e:
        print(f"Model yüklenemedi: {e}")
        return
        
    # Dummy input
    dummy_image = np.random.randint(0, 255, (image_size, image_size, 3), dtype=np.uint8)
    
    # Warmup
    print("Isınma turu...")
    for _ in range(10):
        model(dummy_image, verbose=False)
        
    # Benchmark
    print(f"{num_iterations} iterasyon için test ediliyor...")
    start_time = time.time()
    for _ in range(num_iterations):
        model(dummy_image, verbose=False)
    end_time = time.time()
    
    total_time = end_time - start_time
    avg_time_ms = (total_time / num_iterations) * 1000
    fps = num_iterations / total_time
    
    print("-" * 30)
    print(f"Toplam Zaman : {total_time:.2f} saniye")
    print(f"Kare Başına  : {avg_time_ms:.2f} ms")
    print(f"Tahmini FPS  : {fps:.2f}")
    print("-" * 30)

def main():
    parser = argparse.ArgumentParser(description="Agrovision AI - Performans Testi")
    parser.add_argument("--models", nargs="+", default=["yolov8n.pt", "yolov8s.pt"], help="Test edilecek model listesi")
    parser.add_argument("--sizes", nargs="+", type=int, default=[320, 640], help="Test edilecek görüntü boyutları")
    parser.add_argument("--iter", type=int, default=50, help="İterasyon sayısı")
    
    args = parser.parse_args()
    
    print("AGROVISION AI - DONANIM PERFORMANS TESTİ")
    print("=" * 40)
    
    for model_path in args.models:
        for size in args.sizes:
            benchmark(model_path, size, args.iter)

if __name__ == "__main__":
    main()
