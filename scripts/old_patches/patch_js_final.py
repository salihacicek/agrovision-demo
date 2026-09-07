import re

with open('src/dashboard/static/js/main.js', 'r') as f:
    content = f.read()

marker_start = "window.selectFarmer = function(farmerId) {"
marker_end = "        tbody.innerHTML = html;"

idx_start = content.find(marker_start)
idx_end = content.find(marker_end) + len("        tbody.innerHTML = html;")

new_js = """window.selectFarmer = function(farmerId) {
    const container = document.getElementById('parcels-container');
    const title = document.getElementById('selected-farmer-title');
    const tbody = document.getElementById('cks-parcels-tbody');
    
    if (!farmerId || farmerId === "") {
        if (container) container.style.display = 'none';
        return;
    }
    
    const farmer = farmersDb[farmerId];
    if (!farmer) return;

    if (container) container.style.display = 'block';
    if (title) title.textContent = farmer.name;

    if (tbody) {
        let html = '';
        farmer.parcels.forEach(p => {
            html += `
                <tr style="border-bottom: 1px solid #e2e8f0; transition: background-color 0.2s;" onmouseover="this.style.backgroundColor='#f1f5f9'" onmouseout="this.style.backgroundColor='transparent'">
                    <td style="padding: 1rem 1.5rem; color: #1e293b; font-weight: 500;">${p.no}</td>
                    <td style="padding: 1rem 1.5rem; color: #64748b;">${p.ada}</td>
                    <td style="padding: 1rem 1.5rem; color: #64748b;">${p.alan}</td>
                    <td style="padding: 1rem 1.5rem; color: #64748b;">${p.malik}</td>
                    <td style="padding: 1rem 1.5rem; color: #1e293b; font-weight: 600;">${p.kayitli}</td>
                    <td style="padding: 1rem 1.5rem; color: #64748b;">${p.tarih}</td>
                    <td style="padding: 1rem 1.5rem; text-align: center;">
                        <button class="btn btn-secondary" style="padding: 4px 8px; font-size: 0.8rem;" onclick="window.inceleParsel('${p.mapId}')">
                            <i class="fa-solid fa-eye"></i> İncele
                        </button>
                    </td>
                </tr>
            `;
        });
        tbody.innerHTML = html;"""

content = content[:idx_start] + new_js + content[idx_end:]

with open('src/dashboard/static/js/main.js', 'w') as f:
    f.write(content)
