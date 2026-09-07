import re

with open('src/dashboard/static/js/main.js', 'r') as f:
    content = f.read()

old_download = """function downloadReport() {
    const btn = document.querySelector('.tracker-header .btn-primary');
    
    // Aktif parsel verilerini bul
    let currentParcelId = window.currentActiveParcelId;"""

new_download = """function downloadReport() {
    // Aktif parsel verilerini bul
    let currentParcelId = window.currentActiveParcelId;
    if (!currentParcelId) {
        const dropdown = document.getElementById('parcel-dropdown');
        currentParcelId = dropdown ? dropdown.value : null;
    }
    
    if (!currentParcelId) {
        alert("Lütfen önce listeden veya haritadan bir parsel seçip başlatın. Parsel verisi olmadan rapor alınamaz!");
        return;
    }

    const btn = document.querySelector('.tracker-header .btn-primary');"""

content = content.replace(old_download, new_download)

with open('src/dashboard/static/js/main.js', 'w') as f:
    f.write(content)
