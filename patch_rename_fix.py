import re

with open('src/dashboard/static/js/main.js', 'r') as f:
    js_content = f.read()

# Fix JS init
old_js = """        } else if (targetId === 'tab-filo') {
            target.style.display = 'block';
            setTimeout(() => { 
                if (typeof fleetMap !== 'undefined' && !fleetMapInitialized) {
                    initFleetMap();
                } else if (typeof fleetMap !== 'undefined') {
                    fleetMap.invalidateSize(); 
                }
            }, 200);"""

new_js = """        } else if (targetId === 'tab-filo') {
            target.style.display = 'block';
            setTimeout(() => { 
                if (!fleetMapInitialized) {
                    initFleetMap();
                } else if (fleetMap) {
                    fleetMap.invalidateSize(); 
                }
            }, 200);"""
js_content = js_content.replace(old_js, new_js)

with open('src/dashboard/static/js/main.js', 'w') as f:
    f.write(js_content)


with open('src/dashboard/templates/index.html', 'r') as f:
    html_content = f.read()

html_content = html_content.replace('Filo Yönetimi', 'Araç Yönetimi')
html_content = html_content.replace('Filo Yönetim Merkezi', 'Araç Yönetim Merkezi')
html_content = html_content.replace('Filo Haritası', 'Araç Haritası')
html_content = html_content.replace('Canlı Filo Konumları', 'Canlı Araç Konumları')
html_content = html_content.replace('v=46', 'v=47')

with open('src/dashboard/templates/index.html', 'w') as f:
    f.write(html_content)
