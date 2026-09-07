import re

with open('src/dashboard/templates/index.html', 'r') as f:
    html = f.read()

# 1. Update Hero Image to highres
html = html.replace("url('/static/assets/img/hero-bg.jpg')", "url('/static/assets/img/hero-bg-highres.jpg')")

# 2. Fix the padding of features-section to pull it up
html = html.replace('padding: 6rem 2rem !important;', 'padding: 3rem 2rem 5rem 2rem !important;')
# Make hero banner slightly shorter if needed, or leave at 500px.
html = html.replace('height: 500px !important;', 'height: 450px !important;')

# 3. Fix the hero button color and text
# The text was previously "SİSTEME GİRİŞ" (which I put in via patch_remove_ai.py).
html = html.replace('>SİSTEME GİRİŞ<', '>CANLI İZLEMEYE BAŞLA<')
html = html.replace('background: #4ade80 !important;', 'background: #eab308 !important; /* Soft wheat yellow */')
html = html.replace('color: #064e3b !important;', 'color: #422006 !important; /* Dark brown text */')
html = html.replace('background: #22c55e !important;', 'background: #ca8a04 !important;')

# 4. Remove "+ READ MORE"
html = html.replace('<span class="read-more">+ READ MORE</span>', '')

# 5. Add the 4th card (Hasat Raporları) to features-section
# Find the end of ÇKS card
cks_card = """                        <div class="feature-card" onclick="switchTab('tab-cks')">
                            <div class="icon-wrapper"><i class="fa-solid fa-address-card"></i></div>
                            <h3>ÇKS & PARSELLER</h3>
                            <p>Çiftçi Kayıt Sistemi entegrasyonu ve kayıtlı parsellerin yönetim süreçleri.</p>
                            
                        </div>"""
raporlar_card = """
                        <div class="feature-card" onclick="switchTab('tab-raporlar')">
                            <div class="icon-wrapper"><i class="fa-solid fa-file-pdf"></i></div>
                            <h3>HASAT RAPORLARI</h3>
                            <p>Önceki hasatların telemetri kayıtları, detaylı analiz ve PDF raporlama.</p>
                        </div>"""
html = html.replace(cks_card, cks_card + raporlar_card)

# 6. Change feature-card icons to White on Dark Brown
html = html.replace('background: #fdf8f5 !important;', 'background: #292524 !important; /* Koyu antrasit/kahve */')
html = html.replace('color: #d97706 !important;', 'color: #ffffff !important; /* Beyaz ikon */')

# 7. Remove the neon inline borders from Fleet KPI cards
html = html.replace('border-left: 4px solid #3b82f6;', 'border-left: 4px solid #78350f; /* Koyu kahve */')
html = html.replace('border-left: 4px solid #10b981;', 'border-left: 4px solid #166534; /* Orman yeşili */')
html = html.replace('border-left: 4px solid #f59e0b;', 'border-left: 4px solid #ca8a04; /* Buğday sarısı */')
html = html.replace('border-left: 4px solid #ef4444;', 'border-left: 4px solid #991b1b; /* Koyu kırmızı */')

with open('src/dashboard/templates/index.html', 'w') as f:
    f.write(html)
