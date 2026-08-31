#!/bin/bash
# Modify main.js to show lite mode overlay if source is lite_mode
sed -i '' '/const activeCropZone = document.getElementById('\''activeCropZone'\'');/a\
\
    if (data.source === "lite_mode") {\
        const blindOverlay = document.getElementById("blind-mode-overlay");\
        if (blindOverlay) {\
            blindOverlay.style.display = "flex";\
            blindOverlay.innerHTML = "<i class=\\\"fa-solid fa-bolt\\\" style=\\\"font-size: 3.5rem; color: #10b981; margin-bottom: 1rem;\\\"></i><h3 style=\\\"color: #fff; margin-bottom: 0.5rem;\\\">Sınırsız (Lite) Mod Aktif</h3><p style=\\\"max-width: 380px; font-size: 0.9rem;\\\">Görüntü işleme motoru şu an kapalıdır. 7/24 Kesintisiz GPS rotası, Takograf, Telemetri ve Harita özellikleri devrededir.</p>";\
        }\
    }\
' /Users/salihacicek/Desktop/bugdaymisir/src/dashboard/static/js/main.js
