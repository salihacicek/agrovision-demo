import re

with open('src/dashboard/templates/index.html', 'r') as f:
    html = f.read()

# Replace the global background with a softer dark taupe
old_global1 = """/* HARİTA VE DİĞER EKRANLARIN ARKA PLANINI DÜZELT */
body, html {
    background: #FAF6ED !important; /* Premium elite cream */
}"""
new_global1 = """/* HARİTA VE DİĞER EKRANLARIN ARKA PLANINI DÜZELT */
body, html {
    background: #4a4036 !important; /* Soft earthy dark taupe */
}"""
html = html.replace(old_global1, new_global1)

old_global2 = """/* KURUMSAL TARIM - AI/NEON İPTALİ */
body, html, .dashboard-container, .main-content {
    background: #FAF6ED !important; /* Premium elite cream */
}"""
new_global2 = """/* KURUMSAL TARIM - AI/NEON İPTALİ */
body, html, .dashboard-container, .main-content {
    background: #4a4036 !important; /* Soft earthy dark taupe */
}"""
html = html.replace(old_global2, new_global2)

# Bump CSS cache
html = html.replace('style.css?v=54', 'style.css?v=55')

with open('src/dashboard/templates/index.html', 'w') as f:
    f.write(html)
