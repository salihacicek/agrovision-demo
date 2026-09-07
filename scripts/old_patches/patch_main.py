import re

with open('src/dashboard/static/js/main.js', 'r') as f:
    content = f.read()

# 1. Update farmersDb to include mapId
content = content.replace("tarih: '20.07.2026' }", "tarih: '20.07.2026', mapId: 'P1789' }", 1)
content = content.replace("tarih: '20.07.2026' }", "tarih: '20.07.2026', mapId: 'P1826' }", 1)
content = content.replace("tarih: '20.07.2026' }", "tarih: '20.07.2026', mapId: 'P1959' }", 1)
content = content.replace("tarih: '20.07.2026' }", "tarih: '20.07.2026', mapId: 'P1986' }", 1)
content = content.replace("tarih: '20.07.2026' }", "tarih: '20.07.2026', mapId: 'P2017' }", 1)
content = content.replace("tarih: '20.07.2026' }", "tarih: '20.07.2026', mapId: 'P2044' }", 1)

content = content.replace("tarih: '15.08.2026' }", "tarih: '15.08.2026', mapId: 'P2074' }", 1)
content = content.replace("tarih: '15.08.2026' }", "tarih: '15.08.2026', mapId: 'P2093' }", 1)
content = content.replace("tarih: '15.08.2026' }", "tarih: '15.08.2026', mapId: 'P1789' }", 1)

content = content.replace("tarih: '01.09.2026' }", "tarih: '01.09.2026', mapId: 'P1826' }", 1)
content = content.replace("tarih: '01.09.2026' }", "tarih: '01.09.2026', mapId: 'P1959' }", 1)

# 2. Update incele button inside farmersDb loop
content = content.replace("onclick=\"switchTab('tab-arac-takip')\"", "onclick=\"window.inceleParsel('${p.mapId}')\"")

# 3. Add window.inceleParsel function and update startOnParcel
old_start = """window.startOnParcel = function(parcelId) {
    const parcel = parcels.find(p => p.id === parcelId);
    if (!parcel) return;

    // Haritadaki mevcut rotayı temizle"""

new_start = """window.inceleParsel = function(mapId) {
    if(!mapId) return;
    switchTab('tab-arac-takip');
    const dropdown = document.getElementById('parcel-dropdown');
    if (dropdown) dropdown.value = mapId;
    window.startOnParcel(mapId);
}

window.startOnParcel = function(parcelId) {
    const parcel = parcels.find(p => p.id === parcelId);
    if (!parcel) return;

    // Renklendirme ve stil sıfırlama (highlight)
    if (parcelGeoJsonLayer) {
        parcelGeoJsonLayer.eachLayer(function(l) {
            parcelGeoJsonLayer.resetStyle(l);
            if (l.feature.properties.parsel_id === parcelId) {
                l.setStyle({ fillOpacity: 0.7, weight: 4, color: '#eab308' }); // sarı highlight
                map.flyToBounds(l.getBounds(), { padding: [50, 50], duration: 1.5 });
            }
        });
    }

    // Haritadaki mevcut rotayı temizle"""

content = content.replace(old_start, new_start)

# 4. Update downloadReport for avg speed
old_report = """    // Güncel verileri DOM'dan alalım (veya default)
    const speed = document.getElementById('current-speed') ? document.getElementById('current-speed').textContent : "0.0";"""

new_report = """    // Güncel verileri DOM'dan alalım (veya default)
    const speedArr = trendChart.data.datasets[0].data.filter(s => s > 0);
    const speed = speedArr.length > 0 ? (speedArr.reduce((a, b) => a + b, 0) / speedArr.length).toFixed(1) : "0.0";"""

content = content.replace(old_report, new_report)

with open('src/dashboard/static/js/main.js', 'w') as f:
    f.write(content)
