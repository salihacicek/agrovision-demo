import re

with open('src/dashboard/templates/index.html', 'r') as f:
    html = f.read()

# Replace the old premium css block with an EXTREME premium one
old_css_start = '<style id="premium-ui-overrides">'
old_css_end = '</style>'

if old_css_start in html and old_css_end in html:
    start_idx = html.find(old_css_start)
    end_idx = html.find(old_css_end) + len(old_css_end)
    
    new_css = """<style id="premium-ui-overrides">
:root {
    --primary: #10b981; 
    --primary-dark: #059669;
    --radius-pill: 9999px;
}

/* HARİKA MESH GRADIENT ARKA PLAN */
body, html {
    background-color: #f8fafc !important;
    background-image: 
        radial-gradient(at 0% 0%, rgba(16, 185, 129, 0.15) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(59, 130, 246, 0.15) 0px, transparent 50%) !important;
    background-attachment: fixed;
}

/* FLOATING NAVBAR (Apple/Stripe Tarzı Yüzen Menü) */
body .dashboard-container .top-navbar {
    background: rgba(15, 23, 42, 0.85) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    box-shadow: 0 20px 40px -10px rgba(0,0,0,0.3) !important;
    height: 70px !important;
    margin: 16px 24px !important;
    width: calc(100% - 48px) !important;
    border-radius: 24px !important;
    display: flex !important;
    align-items: center !important;
}

body .dashboard-container .top-navbar .logo h2 {
    color: #ffffff !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px !important;
    font-size: 1.4rem !important;
}
body .dashboard-container .top-navbar .logo i {
    color: #10b981 !important;
    text-shadow: 0 0 15px rgba(16, 185, 129, 0.6) !important;
    font-size: 1.5rem !important;
}

/* NAV LİNKLERİ */
body .dashboard-container .top-navbar .nav-link {
    color: #94a3b8 !important;
    font-weight: 600 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    padding: 10px 20px !important;
    border-radius: 20px !important;
    margin: 0 6px !important;
    font-size: 0.95rem !important;
}
body .dashboard-container .top-navbar .nav-link:hover {
    color: #ffffff !important;
    background: rgba(255,255,255,0.08) !important;
}
body .dashboard-container .top-navbar .nav-link.active {
    color: #ffffff !important;
    background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05)) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
}

/* ANA SAYFA KARTLARI (Büyük ve Gösterişli) */
body .landing-card {
    background: rgba(255, 255, 255, 0.7) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255, 255, 255, 1) !important;
    border-radius: 24px !important;
    padding: 3rem 2rem !important;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01) !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
body .landing-card:hover {
    transform: translateY(-8px) scale(1.02) !important;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15) !important;
    background: rgba(255, 255, 255, 0.95) !important;
    border-color: rgba(16, 185, 129, 0.3) !important;
}
body .landing-card i {
    font-size: 3.5rem !important;
    background: linear-gradient(135deg, #10b981, #3b82f6) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    margin-bottom: 1.5rem !important;
    display: inline-block !important;
}
body .landing-card h3 {
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    color: #0f172a !important;
}
body .landing-card p {
    color: #64748b !important;
    font-size: 1rem !important;
}

/* DİĞER KARTLAR VE HARİTA */
body .card, body .telemetry-card {
    background: rgba(255, 255, 255, 0.8) !important;
    backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(255,255,255,1) !important;
    border-radius: 20px !important;
    box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05) !important;
}
body #map {
    border-radius: 20px !important;
    border: 4px solid #ffffff !important;
    box-shadow: 0 15px 35px rgba(0,0,0,0.1) !important;
}

/* BUTONLAR */
body .btn-primary, body .control-btn.play-btn {
    background: linear-gradient(135deg, #10b981, #059669) !important;
    box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3) !important;
    border-radius: 9999px !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
    border: none !important;
}
body .btn-primary:hover, body .control-btn.play-btn:hover {
    transform: translateY(-3px) scale(1.05) !important;
    box-shadow: 0 12px 25px rgba(16, 185, 129, 0.4) !important;
}
</style>"""
    
    html = html[:start_idx] + new_css + html[end_idx:]

with open('src/dashboard/templates/index.html', 'w') as f:
    f.write(html)
