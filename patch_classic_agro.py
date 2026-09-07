import re

with open('src/dashboard/templates/index.html', 'r') as f:
    html = f.read()

# 1. Update HTML
old_tab_start = '<div id="tab-anasayfa" class="tab-pane active">'
old_tab_end_str = '</div> <!-- /landing-content -->\n                </div>\n            </div>'

start_idx = html.find(old_tab_start)
end_idx = html.find(old_tab_end_str) + len(old_tab_end_str)

new_html = """<div id="tab-anasayfa" class="tab-pane active">
                <div class="landing-page-classic">
                    <div class="hero-banner">
                        <div class="hero-overlay-classic"></div>
                        <div class="hero-content-classic">
                            <h1>Agricultural Products</h1>
                            <p>PROIN ID VOLUTPAT METUS, VEL BIBENDUM METUS</p>
                            <button class="hero-btn" onclick="switchTab('tab-arac-takip')">SHOP NOW</button>
                        </div>
                    </div>
                    
                    <div class="features-section">
                        <div class="feature-card" onclick="switchTab('tab-arac-takip')">
                            <div class="icon-wrapper"><i class="fa-solid fa-map-location-dot"></i></div>
                            <h3>CANLI İZLEME</h3>
                            <p>Canlı biçerdöver rotaları ve telemetri verilerinin anlık takibi. Hasat sürecini optimize edin.</p>
                            <span class="read-more">+ READ MORE</span>
                        </div>
                        
                        <div class="feature-card" onclick="switchTab('tab-filo')">
                            <div class="icon-wrapper"><i class="fa-solid fa-truck-fast"></i></div>
                            <h3>ARAÇ YÖNETİMİ</h3>
                            <p>Tüm filonun harita üzerinde anlık takibi. Araçların operasyonel durumlarını anlık görün.</p>
                            <span class="read-more">+ READ MORE</span>
                        </div>
                        
                        <div class="feature-card" onclick="switchTab('tab-cks')">
                            <div class="icon-wrapper"><i class="fa-solid fa-address-card"></i></div>
                            <h3>ÇKS & PARSELLER</h3>
                            <p>Çiftçi Kayıt Sistemi entegrasyonu ve kayıtlı parsellerin yönetim süreçleri.</p>
                            <span class="read-more">+ READ MORE</span>
                        </div>
                    </div>
                </div>
            </div>"""

if start_idx != -1 and end_idx != -1:
    html = html[:start_idx] + new_html + html[end_idx:]

# 2. Add the classic CSS and override the navbar
# We will inject it right before </style>
classic_css = """
/* CLASSIC AGRO LANDING PAGE */
body .landing-page-classic {
    width: 100% !important;
    height: 100% !important;
    overflow-y: auto !important;
    background: #ffffff !important;
}

body .hero-banner {
    position: relative !important;
    width: 100% !important;
    height: 500px !important;
    background: url('/static/assets/img/hero-bg.jpg') center/cover no-repeat !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
}
body .hero-overlay-classic {
    position: absolute !important;
    top: 0 !important; left: 0 !important; right: 0 !important; bottom: 0 !important;
    background: rgba(80, 40, 10, 0.4) !important; /* Warm earthy tint */
}
body .hero-content-classic {
    position: relative !important;
    z-index: 2 !important;
}
body .hero-content-classic h1 {
    font-size: 4.5rem !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    margin-bottom: 0.5rem !important;
    text-shadow: 0 2px 10px rgba(0,0,0,0.5) !important;
}
body .hero-content-classic p {
    color: #ffffff !important;
    font-size: 1.1rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    margin-bottom: 2rem !important;
    font-weight: 600 !important;
}
body .hero-btn {
    background: #4ade80 !important;
    color: #064e3b !important;
    padding: 12px 35px !important;
    border: none !important;
    border-radius: 4px !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    cursor: pointer !important;
    transition: all 0.3s !important;
}
body .hero-btn:hover {
    background: #22c55e !important;
}

body .features-section {
    padding: 6rem 2rem !important;
    background: #ffffff !important;
    display: flex !important;
    justify-content: center !important;
    gap: 4rem !important;
    flex-wrap: wrap !important;
}
body .feature-card {
    text-align: center !important;
    width: 300px !important;
    cursor: pointer !important;
}
body .feature-card .icon-wrapper {
    width: 110px !important;
    height: 110px !important;
    background: #fdf8f5 !important;
    border-radius: 50% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin: 0 auto 2rem auto !important;
    box-shadow: 0 10px 20px rgba(180, 83, 9, 0.1) !important;
    transition: transform 0.3s ease !important;
}
body .feature-card:hover .icon-wrapper {
    transform: translateY(-8px) !important;
}
body .feature-card .icon-wrapper i {
    font-size: 2.5rem !important;
    color: #d97706 !important;
}
body .feature-card h3 {
    font-size: 1.25rem !important;
    color: #78350f !important;
    margin-bottom: 1rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.5px !important;
}
body .feature-card p {
    color: #64748b !important;
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
    margin-bottom: 1.5rem !important;
}
body .feature-card .read-more {
    color: #d97706 !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
}

/* NAVBAR BEYAZ & DÜZ YAP (Extreme Premium İptali) */
body .dashboard-container .top-navbar {
    background: #ffffff !important;
    backdrop-filter: none !important;
    border: none !important;
    border-bottom: 1px solid #f1f5f9 !important;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05) !important;
    height: 80px !important;
    margin: 0 !important;
    width: 100% !important;
    border-radius: 0 !important;
}
body .dashboard-container .top-navbar .logo h2 {
    color: #78350f !important; /* Earthy brown */
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}
body .dashboard-container .top-navbar .logo i {
    color: #d97706 !important;
    text-shadow: none !important;
}
body .dashboard-container .top-navbar .nav-link {
    color: #475569 !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    text-transform: uppercase !important;
    border-radius: 0 !important;
}
body .dashboard-container .top-navbar .nav-link:hover {
    color: #d97706 !important;
    background: transparent !important;
}
body .dashboard-container .top-navbar .nav-link.active {
    color: #78350f !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* HARİTA VE DİĞER EKRANLARIN ARKA PLANINI DÜZELT */
body, html {
    background: #f8fafc !important; /* Mesh gradienti iptal et */
}
"""

html = html.replace("</style>", classic_css + "\n</style>")

with open('src/dashboard/templates/index.html', 'w') as f:
    f.write(html)
