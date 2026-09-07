import urllib.request
import os

os.makedirs('src/reporting/fonts', exist_ok=True)

# Roboto Regular and Bold from Google Fonts API/CDN
regular_url = "https://github.com/googlefonts/roboto/raw/main/src/hinted/Roboto-Regular.ttf"
bold_url = "https://github.com/googlefonts/roboto/raw/main/src/hinted/Roboto-Bold.ttf"

try:
    print("Downloading Regular...")
    urllib.request.urlretrieve(regular_url, "src/reporting/fonts/Roboto-Regular.ttf")
    print("Downloading Bold...")
    urllib.request.urlretrieve(bold_url, "src/reporting/fonts/Roboto-Bold.ttf")
    print("SUCCESS")
except Exception as e:
    print("FAILED:", str(e))
