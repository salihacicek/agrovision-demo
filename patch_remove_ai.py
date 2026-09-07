import re

with open('src/dashboard/templates/index.html', 'r') as f:
    html = f.read()

# 1. Remove Sistem Ayarları link
html = html.replace('<a href="#" class="nav-link" data-target="tab-gizlilik">Sistem Ayarları</a>', '')

# 2. Add extreme anti-gradient CSS to completely kill the AI look everywhere
anti_ai_css = """
/* KURUMSAL TARIM - AI/NEON İPTALİ */
body, html, .dashboard-container, .main-content {
    background: #fdf8f5 !important; /* Çok uçuk toprak/krem rengi */
}

/* Tüm ikonlardaki gradientleri ez ve düz kurumsal siyah/kahve yap */
body i, 
body .fa-solid, 
body .card-icon, 
body .kpi-icon, 
body .stat-card i,
body .telemetry-card i {
    background: none !important;
    -webkit-background-clip: unset !important;
    -webkit-text-fill-color: unset !important;
    color: #451a03 !important; /* Koyu kahve/siyah */
}

/* Yuvarlak kutulu ikonların arka planını çok uçuk krem yap */
body .icon-box, 
body .stat-icon, 
body .kpi-icon-wrapper {
    background: #f5ece5 !important;
    box-shadow: none !important;
    border: 1px solid #e7d5c7 !important;
}

/* Butonları da klasik yeşil/toprak tonu yap (Neon değil) */
body .btn-primary, body .control-btn.play-btn {
    background: #166534 !important; /* Koyu orman yeşili */
    box-shadow: none !important;
    color: white !important;
    border-radius: 6px !important; /* Fazla yuvarlak değil */
}
body .btn-primary:hover, body .control-btn.play-btn:hover {
    background: #14532d !important;
    transform: none !important;
}

/* Tablo ve Kartların arka planı bembeyaz ve hafif gri gölgeli */
body .card, body .telemetry-card, body .table-container {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05) !important;
    border-radius: 8px !important;
}

/* Harita kenarlığı */
body #map, body #fleet-map {
    border-radius: 8px !important;
    border: 1px solid #cbd5e1 !important;
    box-shadow: none !important;
}
"""

if "KURUMSAL TARIM - AI/NEON İPTALİ" not in html:
    html = html.replace("</style>", anti_ai_css + "\n</style>")

# 3. Rename "Araç Yönetimi" button in hero to SHOP NOW equivalent if needed? 
# The user liked the design. I already set it to "SHOP NOW" in previous patch. Wait, they probably want it in Turkish.
html = html.replace('>SHOP NOW<', '>SİSTEME GİRİŞ<')

with open('src/dashboard/templates/index.html', 'w') as f:
    f.write(html)
