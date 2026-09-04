FROM python:3.10-slim

# Kurulum için gerekli sistem paketleri (OpenCV için)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Gereksinimleri kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY . .

# HF Spaces requires specific permissions to write logs/uploads sometimes, so give full access to /app
RUN chmod -R 777 /app

# Hugging Face Spaces varsayılan portu
EXPOSE 7860

CMD ["python", "scripts/run_live.py", "--dashboard", "--port", "7860", "--model", "runs/detect/runs/detect/agro_train/weights/best.pt", "--source", "none", "--sim-gps"]
