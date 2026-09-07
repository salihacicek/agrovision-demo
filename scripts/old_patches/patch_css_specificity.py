import re

with open('src/dashboard/static/css/style.css', 'r') as f:
    content = f.read()

# Find the start of the premium overrides block
premium_marker = "/* ========================================================= */\n/* PREMIUM UI UPGRADE OVERRIDES                              */\n/* ========================================================= */"
if premium_marker in content:
    content = content.split(premium_marker)[0]

premium_css = """
/* ========================================================= */
/* PREMIUM UI UPGRADE OVERRIDES                              */
/* ========================================================= */

:root {
    --bg-dark: #f1f5f9; 
    --primary: #10b981; 
    --primary-dark: #059669;
    --text-main: #0f172a;
    --text-muted: #64748b;
    --border: #e2e8f0;
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.025);
    --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 10px 10px -5px rgba(0, 0, 0, 0.02);
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-pill: 9999px;
}

body, html {
    background-color: var(--bg-dark) !important;
}

/* YÜKSEK ÖNCELİKLİ NAVBAR (Glassmorphism & Derin Slate) */
body .dashboard-container .top-navbar {
    background: rgba(15, 23, 42, 0.95) !important;
    backdrop-filter: blur(12px) !important;
    border-bottom: 1px solid rgba(255,255,255,0.05) !important;
    box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5) !important;
    height: 76px !important;
}
body .dashboard-container .top-navbar .logo h2 {
    color: #ffffff !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px !important;
}
body .dashboard-container .top-navbar .logo i {
    color: #34d399 !important;
    text-shadow: 0 0 10px rgba(52, 211, 153, 0.4) !important;
}

/* YÜKSEK ÖNCELİKLİ NAV LİNKLERİ (Hap Tasarım) */
body .dashboard-container .top-navbar .nav-link {
    color: #94a3b8 !important;
    font-weight: 500 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    border: 1px solid transparent !important;
    padding: 8px 18px !important;
    border-radius: var(--radius-pill) !important;
    margin: 0 4px !important;
}
body .dashboard-container .top-navbar .nav-link:hover {
    color: #ffffff !important;
    background: rgba(255,255,255,0.05) !important;
}
body .dashboard-container .top-navbar .nav-link.active {
    color: #ffffff !important;
    background: rgba(255,255,255,0.1) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.1) !important;
}

/* YÜKSEK ÖNCELİKLİ KARTLAR (Premium Soft-Shadow & Rounded) */
body .card, body .tracker-header, body .telemetry-card {
    background: #ffffff !important;
    border: 1px solid rgba(0,0,0,0.04) !important;
    border-radius: var(--radius-lg) !important;
    box-shadow: var(--shadow-md) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
body .card:hover, body .telemetry-card:hover {
    transform: translateY(-4px) !important;
    box-shadow: var(--shadow-lg) !important;
    border-color: rgba(16, 185, 129, 0.15) !important;
}

/* Tracker Header (Yüzen Şeffaf Kontrol Barı) */
body .tracker-header {
    border-radius: var(--radius-pill) !important;
    padding: 12px 24px !important;
    background: rgba(255, 255, 255, 0.85) !important;
    backdrop-filter: blur(16px) !important;
    margin-bottom: 2rem !important;
}

/* YÜKSEK ÖNCELİKLİ BUTONLAR (Modern Gradient) */
body .btn, body .control-btn {
    border-radius: var(--radius-pill) !important;
    font-weight: 600 !important;
    letter-spacing: 0.2px !important;
    transition: all 0.3s ease !important;
    box-shadow: var(--shadow-sm) !important;
    border: none !important;
}
body .btn-primary, body .control-btn.play-btn {
    background: linear-gradient(135deg, var(--primary), var(--primary-dark)) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}
body .btn-primary:hover, body .control-btn.play-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 15px rgba(16, 185, 129, 0.3) !important;
    filter: brightness(1.1) !important;
}

/* Telemetri Widget İkonları */
body .telemetry-card {
    position: relative !important;
    overflow: hidden !important;
    padding: 1.5rem !important;
}
body .telemetry-card i.fa-gauge-high,
body .telemetry-card i.fa-temperature-half,
body .telemetry-card i.fa-chart-pie {
    background: #f1f5f9 !important;
    padding: 12px !important;
    border-radius: 50% !important;
    color: var(--secondary) !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin-bottom: 0.5rem !important;
    font-size: 1.2rem !important;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.05) !important;
}

/* Harita border-radius fix */
body #map {
    border-radius: var(--radius-lg) !important;
    box-shadow: var(--shadow-md) !important;
    border: 1px solid rgba(0,0,0,0.05) !important;
}
"""

content += premium_css

with open('src/dashboard/static/css/style.css', 'w') as f:
    f.write(content)
