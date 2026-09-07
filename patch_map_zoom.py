import re

with open('src/dashboard/static/js/main.js', 'r') as f:
    js = f.read()

# 1. Remove fitBounds on route change (which was causing the random zoom-out)
js = js.replace("        map.fitBounds(parcelGeoJsonLayer.getBounds());\n        routeSegments.push(currentSegment);", "        routeSegments.push(currentSegment);")

# 2. Prevent auto-snap-back after 5 seconds by replacing the timer logic
old_timer = """// 5 saniye sonra otomatik takibe geri dön
map.on('dragend', () => {
    if (dragResumeTimer) clearTimeout(dragResumeTimer);
    dragResumeTimer = setTimeout(() => {
        userDraggedMap = false;
    }, 5000);
});"""

new_timer = """// Kullanıcı haritayı sürüklediğinde kalıcı olarak otomatik takibi bırak (kendi nerede bıraktıysa orada kalsın)
map.on('dragend', () => {
    // Timeout kaldırıldı - Kullanıcı sayfayı yenileyene veya parsele tıklayana kadar manuel mod
});

// Ayrıca zoom yapıldığında da takibi bırakalım ki kendi zoom seviyesinde kalsın
map.on('zoom', () => {
    userDraggedMap = true;
});"""

js = js.replace(old_timer, new_timer)

with open('src/dashboard/static/js/main.js', 'w') as f:
    f.write(js)
