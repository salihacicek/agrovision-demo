import re

with open('src/dashboard/static/js/main.js', 'r') as f:
    content = f.read()

# 1. Update switchTab to handle tab-filo
old_switch = """        if (targetId === 'tab-arac-takip') {
            target.style.display = 'grid';
            setTimeout(() => { if (typeof map !== 'undefined') map.invalidateSize(); }, 200);
        } else if (targetId === 'tab-anasayfa') {"""

new_switch = """        if (targetId === 'tab-arac-takip') {
            target.style.display = 'grid';
            setTimeout(() => { if (typeof map !== 'undefined') map.invalidateSize(); }, 200);
        } else if (targetId === 'tab-filo') {
            target.style.display = 'block';
            setTimeout(() => { 
                if (typeof fleetMap !== 'undefined' && !fleetMapInitialized) {
                    initFleetMap();
                } else if (typeof fleetMap !== 'undefined') {
                    fleetMap.invalidateSize(); 
                }
            }, 200);
        } else if (targetId === 'tab-anasayfa') {"""

content = content.replace(old_switch, new_switch)

# 2. Append the fleet map logic to the end of main.js
fleet_js = """

// ==========================================
// FİLO YÖNETİMİ (FLEET MANAGEMENT) MANTIĞI
// ==========================================

let fleetMap;
let fleetMapInitialized = false;
let fleetMarkers = {};

const fleetData = [
    { id: 'v1', plate: 'TR-06-AG-101', driver: 'Ahmet Yılmaz', status: 'Hasatta', statusClass: 'status-hasat', fuel: 75, lat: 40.0880, lon: 32.9950, speed: '8.5' },
    { id: 'v2', plate: 'TR-51-HC-402', driver: 'Mehmet Demir', status: 'Hasatta', statusClass: 'status-hasat', fuel: 42, lat: 37.9680, lon: 34.6730, speed: '9.2' },
    { id: 'v3', plate: 'TR-51-HC-403', driver: 'Ali Kaya', status: 'Beklemede', statusClass: 'status-yol', fuel: 88, lat: 37.9800, lon: 34.6600, speed: '0.0' },
    { id: 'v4', plate: 'TR-06-AG-102', driver: 'Hasan Yücel', status: 'Hasatta', statusClass: 'status-hasat', fuel: 15, lat: 40.0800, lon: 32.9800, speed: '7.8' },
    { id: 'v5', plate: 'TR-38-KY-205', driver: 'Kemal Sun', status: 'Bakımda', statusClass: 'status-bakim', fuel: 90, lat: 38.7300, lon: 35.4800, speed: '0.0' }
];

function initFleetMap() {
    if (fleetMapInitialized) return;
    
    // Haritayı başlat (Türkiye ortalanmış)
    fleetMap = L.map('fleet-map', {
        attributionControl: false
    }).setView([39.0, 34.0], 6);
    
    L.control.attribution({prefix: '🇹🇷 Agrovision AI | Filo Haritası'}).addTo(fleetMap);
    
    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: 'Tiles &copy; Esri World Imagery',
        maxZoom: 22
    }).addTo(fleetMap);
    
    // Araç pinlerini ekle
    const tractorIcon = L.divIcon({
        className: 'custom-fleet-marker',
        html: `<div style="background: #3b82f6; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 3px solid white; box-shadow: 0 4px 6px rgba(0,0,0,0.3); color: white; font-size: 16px;"><i class="fa-solid fa-tractor"></i></div>`,
        iconSize: [36, 36],
        iconAnchor: [18, 18]
    });
    
    const bounds = [];
    
    fleetData.forEach(v => {
        const marker = L.marker([v.lat, v.lon], { icon: tractorIcon }).addTo(fleetMap);
        marker.bindPopup(`<b>${v.plate}</b><br>${v.driver}<br>Hız: ${v.speed} km/s`);
        fleetMarkers[v.id] = marker;
        bounds.push([v.lat, v.lon]);
    });
    
    if (bounds.length > 0) {
        fleetMap.fitBounds(bounds, { padding: [50, 50] });
    }
    
    renderFleetList();
    fleetMapInitialized = true;
}

function renderFleetList() {
    const listContainer = document.getElementById('fleet-list');
    if (!listContainer) return;
    
    let html = '';
    fleetData.forEach(v => {
        html += `
            <div class="fleet-item" onclick="flyToFleetVehicle('${v.id}')">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                    <div>
                        <div style="font-weight: 700; color: #1e293b;">${v.plate}</div>
                        <div style="font-size: 0.8rem; color: #64748b; margin-top: 2px;"><i class="fa-regular fa-user"></i> ${v.driver}</div>
                    </div>
                    <span class="fleet-status-badge ${v.statusClass}">${v.status}</span>
                </div>
                
                <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem; color: #64748b;">
                    <div>Yakıt: %${v.fuel}</div>
                    <div>Hız: ${v.speed} km/s</div>
                </div>
                <div class="fuel-bar-container">
                    <div class="fuel-bar-fill" style="width: ${v.fuel}%; background: ${v.fuel < 20 ? '#ef4444' : '#3b82f6'};"></div>
                </div>
            </div>
        `;
    });
    listContainer.innerHTML = html;
}

window.flyToFleetVehicle = function(id) {
    const v = fleetData.find(x => x.id === id);
    if (v && fleetMap) {
        fleetMap.flyTo([v.lat, v.lon], 15, { duration: 1.5 });
        if (fleetMarkers[id]) {
            fleetMarkers[id].openPopup();
        }
    }
};

"""
content += fleet_js

with open('src/dashboard/static/js/main.js', 'w') as f:
    f.write(content)
