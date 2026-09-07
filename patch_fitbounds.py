import re

with open('src/dashboard/static/js/main.js', 'r') as f:
    js = f.read()

old_code = """        parcelGeoJsonLayer = L.geoJSON(geojsonData, {
            style: tkgmStyle,"""

new_code = """        parcelGeoJsonLayer = L.geoJSON(geojsonData, {
            style: tkgmStyle,"""

# Actually I need to add fitBounds AFTER the geoJSON is added to the map.
# Let's find: `}).addTo(map);` for the parcelGeoJsonLayer block.

if "}).addTo(map);" in js:
    # We replace the first instance inside loadTKGMParcels
    js = js.replace("}).addTo(map);", "}).addTo(map);\n        map.fitBounds(parcelGeoJsonLayer.getBounds());", 1)

with open('src/dashboard/static/js/main.js', 'w') as f:
    f.write(js)
