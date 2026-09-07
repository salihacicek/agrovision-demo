import re

with open('src/dashboard/static/js/main.js', 'r') as f:
    content = f.read()

# 1. Update downloadPdfReport to send avg_speed
old_fetch = "fetch('/generate_report', { method: 'POST' })"
new_fetch = """
    const speedArr = trendChart.data.datasets[0].data.filter(s => s > 0);
    const avgSpeed = speedArr.length > 0 ? parseFloat((speedArr.reduce((a, b) => a + b, 0) / speedArr.length).toFixed(1)) : 0.0;
    
    fetch('/generate_report', { 
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ avg_speed: avgSpeed })
    })
"""
content = content.replace(old_fetch, new_fetch)

# 2. Update window.inceleParsel to ONLY fly and highlight, and open popup, NO startOnParcel
old_incele = """window.inceleParsel = function(mapId) {
    if(!mapId) return;
    switchTab('tab-arac-takip');
    const dropdown = document.getElementById('parcel-dropdown');
    if (dropdown) dropdown.value = mapId;
    window.startOnParcel(mapId);
}"""

new_incele = """window.inceleParsel = function(mapId) {
    if(!mapId) return;
    switchTab('tab-arac-takip');
    const dropdown = document.getElementById('parcel-dropdown');
    if (dropdown) dropdown.value = mapId;
    
    if (parcelGeoJsonLayer) {
        parcelGeoJsonLayer.eachLayer(function(l) {
            parcelGeoJsonLayer.resetStyle(l);
            if (l.feature.properties.parsel_id === mapId) {
                l.setStyle({ fillOpacity: 0.7, weight: 4, color: '#eab308' });
                map.flyToBounds(l.getBounds(), { padding: [50, 50], duration: 1.5 });
                setTimeout(() => { l.openPopup(); }, 1500); // Popup aç
            }
        });
    }
}"""

content = content.replace(old_incele, new_incele)

with open('src/dashboard/static/js/main.js', 'w') as f:
    f.write(content)
