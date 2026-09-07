import cv2
import numpy as np
from ultralytics import YOLO
model = YOLO('runs/detect/runs/detect/agro_train/weights/best.pt')
cap = cv2.VideoCapture('data/raw_videos/WhatsApp Video 2026-07-22 at 11.29.19.mp4')
ret, frame = cap.read()
if ret:
    print("Frame read successfully")
    try:
        results = model(frame, verbose=False, conf=0.5)
        annotated_frame = results[0].plot()
        print("Annotated frame shape:", annotated_frame.shape)
    except Exception as e:
        print("YOLO Error:", e)
