import re

with open('src/dashboard/static/js/main.js', 'r') as f:
    js = f.read()

old_code = """        if (targetId === 'tab-arac-takip') {
            target.style.display = 'grid';
            setTimeout(() => { if (typeof map !== 'undefined') map.invalidateSize(); }, 200);
        }"""

new_code = """        if (targetId === 'tab-arac-takip') {
            target.style.display = 'grid';
            setTimeout(() => { 
                if (typeof map !== 'undefined') {
                    map.invalidateSize(); 
                    if (typeof parcelGeoJsonLayer !== 'undefined' && parcelGeoJsonLayer) {
                        map.fitBounds(parcelGeoJsonLayer.getBounds());
                    }
                }
            }, 200);
        }"""

js = js.replace(old_code, new_code)
js = js.replace('v=49', 'v=50')

with open('src/dashboard/static/js/main.js', 'w') as f:
    f.write(js)
