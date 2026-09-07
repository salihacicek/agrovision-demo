import re

with open('src/dashboard/static/js/main.js', 'r') as f:
    content = f.read()

# 1. Update startOnParcel to store active parcel and sync dropdown
old_start = """window.startOnParcel = function(parcelId) {
    const parcel = parcels.find(p => p.id === parcelId);
    if (!parcel) return;"""

new_start = """window.currentActiveParcelId = null;
window.startOnParcel = function(parcelId) {
    const parcel = parcels.find(p => p.id === parcelId);
    if (!parcel) return;
    
    window.currentActiveParcelId = parcelId;
    const dropdown = document.getElementById('parcel-dropdown');
    if (dropdown) dropdown.value = parcelId;"""
content = content.replace(old_start, new_start)

# 2. Update downloadReport to use window.currentActiveParcelId and NOT auto-download
old_download = """    // Aktif parsel verilerini bul
    const dropdown = document.getElementById('parcel-dropdown');
    let currentParcelId = dropdown ? dropdown.value : null;
    let activeParcel = null;
    let ownerName = "Bilinmiyor";
    
    if (currentParcelId) {"""

new_download = """    // Aktif parsel verilerini bul
    let currentParcelId = window.currentActiveParcelId;
    if (!currentParcelId) {
        const dropdown = document.getElementById('parcel-dropdown');
        currentParcelId = dropdown ? dropdown.value : null;
    }
    
    let activeParcel = null;
    let ownerName = "Bilinmiyor";
    
    if (currentParcelId) {"""
content = content.replace(old_download, new_download)

old_auto = """    // Geçmiş Raporlar Sekmesine Atla
    switchTab('tab-raporlar');
    
    // Hemen PDF de indir
    downloadPdfReportDynamic(payload, btn);
}"""

new_auto = """    // Geçmiş Raporlar Sekmesine Atla
    switchTab('tab-raporlar');
}"""
content = content.replace(old_auto, new_auto)

with open('src/dashboard/static/js/main.js', 'w') as f:
    f.write(content)
