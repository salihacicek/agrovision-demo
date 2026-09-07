import re

with open('src/dashboard/templates/index.html', 'r') as f:
    html = f.read()

# 1. Update HTML structure of landing page
old_landing_html = """                <div class="landing-page">
                    <div class="landing-logo">
                        <div class="icon-circle">
                            <i class="fa-solid fa-leaf"></i>
                        </div>
                        <h1>Agrovision AI</h1>
                        <p>Tarımda İnovasyon ve Sürdürülebilirlik</p>
                    </div>"""

new_landing_html = """                <div class="landing-page">
                    <div class="landing-overlay"></div>
                    <div class="landing-content">
                        <div class="landing-logo">
                            <h1>Best Agricultural Seeds</h1>
                            <p>Agrovision AI ile Tarımda Hassas Telemetri ve Sürdürülebilirlik</p>
                        </div>"""

# Close landing-content div after landing-cards
old_cards_end = """                        <div class="landing-card" onclick="switchTab('tab-gizlilik')">
                            <i class="fa-solid fa-gear"></i>
                            <h3>Sistem Ayarları</h3>
                            <p>Sensör ve konfigürasyon yapılandırması</p>
                        </div>
                    </div>
                </div>"""

new_cards_end = """                        <div class="landing-card" onclick="switchTab('tab-gizlilik')">
                            <i class="fa-solid fa-gear"></i>
                            <h3>Sistem Ayarları</h3>
                            <p>Sensör ve konfigürasyon yapılandırması</p>
                        </div>
                    </div>
                    </div> <!-- /landing-content -->
                </div>"""

if old_landing_html in html:
    html = html.replace(old_landing_html, new_landing_html)
    html = html.replace(old_cards_end, new_cards_end)

# 2. Add the CSS to the premium overrides
css_to_add = """
/* HERO LANDING PAGE YÜKSELTME */
body .landing-page {
    position: fixed !important;
    top: 0 !important; 
    left: 0 !important; 
    width: 100vw !important; 
    height: 100vh !important;
    background: url('/static/assets/img/hero-bg.jpg') center/cover no-repeat !important;
    z-index: 0 !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 0 !important;
    margin: 0 !important;
    border-radius: 0 !important;
}

body .landing-overlay {
    position: absolute !important; 
    top: 0 !important; left: 0 !important; right: 0 !important; bottom: 0 !important;
    background: linear-gradient(to bottom, rgba(15,23,42,0.4) 0%, rgba(15,23,42,0.8) 100%) !important;
    z-index: 1 !important;
}

body .landing-content {
    position: relative !important;
    z-index: 2 !important;
    width: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    margin-top: 60px !important; /* Navbar boşluğu */
}

body .landing-logo h1 {
    font-size: 4rem !important;
    font-weight: 800 !important;
    color: #ffffff !important;
    text-shadow: 0 4px 20px rgba(0,0,0,0.5) !important;
    margin-bottom: 1rem !important;
    letter-spacing: -1px !important;
}

body .landing-logo p {
    font-size: 1.25rem !important;
    color: #cbd5e1 !important;
    margin-bottom: 4rem !important;
    font-weight: 500 !important;
}

/* KARTLARIN ARKA PLANINI DAHA ŞEFFAF VE UYUMLU YAP */
body .landing-card {
    background: rgba(15, 23, 42, 0.4) !important;
    backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important;
}
body .landing-card h3 {
    color: #ffffff !important;
}
body .landing-card p {
    color: #94a3b8 !important;
}
body .landing-card:hover {
    background: rgba(15, 23, 42, 0.7) !important;
    border-color: rgba(16, 185, 129, 0.5) !important;
}

/* NAVBAR HERO İLE KARIŞMASIN DİYE Z-INDEX GÜNCELLEMESİ */
body .dashboard-container .top-navbar {
    position: relative !important;
    z-index: 1000 !important;
}
"""

if "HERO LANDING PAGE" not in html:
    html = html.replace("</style>", css_to_add + "\n</style>")

with open('src/dashboard/templates/index.html', 'w') as f:
    f.write(html)
