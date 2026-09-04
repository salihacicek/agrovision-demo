import re

with open('src/dashboard/static/js/main.js', 'r') as f:
    content = f.read()

old_incele = """window.inceleParsel = function(mapId) {
    if(!mapId) return;
    switchTab('tab-arac-takip');
    const dropdown = document.getElementById('parcel-dropdown');
    if (dropdown) dropdown.value = mapId;
    
    if (parcelGeoJsonLayer) {"""

new_incele = """window.inceleParsel = function(mapId) {
    if(!mapId) return;
    switchTab('tab-arac-takip');
    const dropdown = document.getElementById('parcel-dropdown');
    if (dropdown) dropdown.value = mapId;
    
    // Eski rotaları sil
    if (typeof routeSegments !== 'undefined') {
        routeSegments.forEach(seg => map.removeLayer(seg));
        routeSegments = [];
    }
    if (typeof currentSegment !== 'undefined') currentSegment = null;
    if (typeof lastRouteLatLng !== 'undefined') lastRouteLatLng = null;
    
    if (parcelGeoJsonLayer) {"""

content = content.replace(old_incele, new_incele)

with open('src/dashboard/static/js/main.js', 'w') as f:
    f.write(content)
