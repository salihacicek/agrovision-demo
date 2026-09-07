import re

with open('src/dashboard/templates/index.html', 'r') as f:
    html = f.read()

old_btn = """                                <button id="toggle-play-btn" class="control-btn play-btn" onclick="togglePlay()">
                                    <i class="fa-solid fa-pause"></i> <span>Durdur</span>
                                </button>"""

new_btn = """                                <button id="toggle-play-btn" class="control-btn play-btn paused" onclick="togglePlay()">
                                    <i class="fa-solid fa-play"></i> <span>Başlat</span>
                                </button>"""

html = html.replace(old_btn, new_btn)
html = html.replace('v=48', 'v=49')

with open('src/dashboard/templates/index.html', 'w') as f:
    f.write(html)


with open('src/dashboard/static/js/main.js', 'r') as f:
    js = f.read()

# Change let isTrackingPaused = false; to true; if it exists
js = re.sub(r'let isTrackingPaused\s*=\s*false;', 'let isTrackingPaused = true;', js)

with open('src/dashboard/static/js/main.js', 'w') as f:
    f.write(js)

