import re

with open('src/dashboard/static/js/main.js', 'r') as f:
    js = f.read()

# Remove the bad line
js = js.replace("        map.fitBounds(parcelGeoJsonLayer.getBounds());\n", "")

# Add it safely inside loadTKGMParcels block
# Let's find: `        }).addTo(map);` (with exact spaces, because attribution has no spaces before it)

if "        }).addTo(map);" in js:
    js = js.replace("        }).addTo(map);", "        }).addTo(map);\n        map.fitBounds(parcelGeoJsonLayer.getBounds());")

with open('src/dashboard/static/js/main.js', 'w') as f:
    f.write(js)
