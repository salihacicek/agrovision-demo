import re

with open('src/dashboard/static/js/main.js', 'r') as f:
    content = f.read()

old_start = """    window.isTeleporting = true;

    // Backend'e yeni parselin koordinatlarını gönder
    fetch('/set_target_parcel', {"""

new_start = """    window.isTeleporting = true;
    
    // Telemetri grafiklerini ve sayaçlarını sıfırla
    if (typeof trendChart !== 'undefined') {
        trendChart.data.labels = [];
        trendChart.data.datasets[0].data = [];
        trendChart.update();
    }
    if (document.getElementById('donum-val')) {
        document.getElementById('donum-val').textContent = "0.0 Dönüm";
    }
    if (typeof currentHarvestedDönüm !== 'undefined') {
        currentHarvestedDönüm = "0.0";
    }

    // Backend'e yeni parselin koordinatlarını gönder
    fetch('/set_target_parcel', {"""

content = content.replace(old_start, new_start)

with open('src/dashboard/static/js/main.js', 'w') as f:
    f.write(content)
