import re

with open('src/dashboard/templates/index.html', 'r') as f:
    html = f.read()

unify_css = """
/* TELEMETRİ BÖLÜMÜNÜ BÜTÜNLEŞTİRME */
body .telemetry-section {
    display: flex !important;
    background: #FAF6ED !important;
    border-radius: 12px !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    gap: 0 !important;
    overflow: hidden !important;
    margin-top: 1.5rem !important;
}

body .telemetry-section > .card {
    flex: 1 !important;
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    border-right: 1px solid #e2e8f0 !important;
    margin: 0 !important;
}

body .telemetry-section > .card:last-child {
    border-right: none !important;
}
"""

if "TELEMETRİ BÖLÜMÜNÜ BÜTÜNLEŞTİRME" not in html:
    html = html.replace("</style>", unify_css + "\n</style>")

# Bump CSS cache
html = html.replace('style.css?v=57', 'style.css?v=58')

with open('src/dashboard/templates/index.html', 'w') as f:
    f.write(html)
