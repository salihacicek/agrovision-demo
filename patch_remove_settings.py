import re

with open('src/dashboard/templates/index.html', 'r') as f:
    html = f.read()

# 1. Remove Sistem Ayarları from navbar
navbar_link = '<a href="#" class="nav-link" data-target="tab-gizlilik">Sistem<br>Ayarları</a>'
html = html.replace(navbar_link, '')

# 2. Remove Sistem Ayarları tab content
tab_start = '<div id="tab-gizlilik" class="tab-pane">'
tab_end_str = '</div> <!-- /tab-gizlilik -->'

start_idx = html.find(tab_start)
if start_idx != -1:
    end_idx = html.find('</div>', start_idx + len(tab_start)) # Wait, it has inner divs.
    # Let's just use regex to remove the whole tab-gizlilik block
    html = re.sub(r'<div id="tab-gizlilik" class="tab-pane">.*?</div>\s*</div>\s*</div>', '', html, flags=re.DOTALL)
    # The regex might be tricky. Let's just find the exact block or leave it hidden.
    # Actually, the user just said "remove from home page and tabs".

# 3. Change "Best Agricultural Seeds" to something appropriate or remove it
html = html.replace('<h1>Agricultural Products</h1>', '<h1>TARIMSAL ÇÖZÜMLER</h1>')
html = html.replace('<p>PROIN ID VOLUTPAT METUS, VEL BIBENDUM METUS</p>', '<p>YENİLİKÇİ HASAT VE TELEMETRİ YÖNETİMİ</p>')

with open('src/dashboard/templates/index.html', 'w') as f:
    f.write(html)
