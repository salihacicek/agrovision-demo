import re

with open('src/dashboard/static/js/main.js', 'r') as f:
    content = f.read()

# Update selectFarmer to handle empty selection
old_select = """window.selectFarmer = function(farmerId) {
    const farmer = farmersDb[farmerId];
    if (!farmer) return;"""

new_select = """window.selectFarmer = function(farmerId) {
    if (!farmerId || farmerId === "") {
        // Çiftçi seçilmedi, boş ekran göster
        document.getElementById('cks-farmer-name').textContent = "Lütfen bir çiftçi seçin";
        document.getElementById('cks-farmer-tc').textContent = "-";
        document.getElementById('cks-farmer-no').textContent = "-";
        document.getElementById('cks-farmer-city').textContent = "-";
        document.getElementById('cks-farmer-count').textContent = "0 Parsel Kaydı";
        const tbody = document.getElementById('cks-parcels-tbody');
        if (tbody) tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding:2rem;">Görüntülenecek parsel bulunamadı.</td></tr>`;
        return;
    }
    const farmer = farmersDb[farmerId];
    if (!farmer) return;"""

content = content.replace(old_select, new_select)

# Remove the window.selectFarmer('osman') from populateNewTabs
content = content.replace("window.selectFarmer('osman');", "window.selectFarmer(''); // Boş başlat")

with open('src/dashboard/static/js/main.js', 'w') as f:
    f.write(content)
