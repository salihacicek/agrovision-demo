#!/bin/bash
echo "Agrovision AI Sunucu Baslatiliyor..."

# Eğer eski çalışan python varsa kapat
pkill -f "run_lite.py"
pkill -f "run_live.py"
pkill -f "cloudflared"

# Conda ortamını aktif et ve python uygulamasını başlat (Arka planda)
cd "$(dirname "$0")"
/opt/anaconda3/bin/conda run -n agrovision python scripts/run_lite.py --port 8080 &

echo "Sistem baslatildi. 5 saniye bekleniyor..."
sleep 5

echo "--------------------------------------------------------"
echo "Internet Tuneli (Cloudflare) Aciliyor..."
echo "Lutfen cikan yazilar arasindaki 'https://..........trycloudflare.com' linkini kopyalayip kullanin."
echo "--------------------------------------------------------"

/opt/homebrew/bin/cloudflared tunnel --url http://localhost:8080
