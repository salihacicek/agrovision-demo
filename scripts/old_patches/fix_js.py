import re

with open('src/dashboard/static/js/main.js', 'r') as f:
    content = f.read()

# We want to replace everything from the start of `// Nav linklerine tıklama dinleyicisi ekle` to the end.
marker = "// Nav linklerine tıklama dinleyicisi ekle"
start_idx = content.find(marker)

if start_idx != -1:
    new_end = """// Nav linklerine tıklama dinleyicisi ekle (DOMContentLoaded'da güvenli)
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const t = link.getAttribute('data-target');
            if (t) switchTab(t);
        });
    });

    // Sayfa ilk açıldığında anasayfa sekmesini aç
    switchTab('tab-anasayfa');
});

// --- ÇKS Çiftçi Veritabanı ---
const farmersDb = {
    'osman': {
        name: 'Osman Cingitaş', tc: '12345678901', no: '2025-0158', city: 'Niğde',
        parcels: [
            { no: '51-113-25-1', ada: '25/1', alan: '25.000', malik: 'Osman Cingitaş', kayitli: 'Buğday', tarih: '20.07.2026' },
            { no: '51-113-25-2', ada: '25/2', alan: '25.000', malik: 'Osman Cingitaş', kayitli: 'Mısır', tarih: '20.07.2026' },
            { no: '51-113-25-3', ada: '25/3', alan: '25.000', malik: 'Osman Cingitaş', kayitli: 'Mısır', tarih: '20.07.2026' },
            { no: '51-113-25-4', ada: '25/4', alan: '25.000', malik: 'Osman Cingitaş', kayitli: 'Mısır', tarih: '20.07.2026' },
            { no: '51-115-25-5', ada: '25/5', alan: '25.000', malik: 'Osman Cingitaş', kayitli: 'Ayçiçeği', tarih: '20.07.2026' },
            { no: '51-113-25-6', ada: '25/6', alan: '25.000', malik: 'Osman Cingitaş', kayitli: 'Ayçiçeği', tarih: '20.07.2026' },
        ]
    },
    'ahmet': {
        name: 'Ahmet Yılmaz', tc: '34567890123', no: '2025-0842', city: 'Konya',
        parcels: [
            { no: '42-054-10-1', ada: '10/1', alan: '45.500', malik: 'Ahmet Yılmaz', kayitli: 'Buğday', tarih: '15.08.2026' },
            { no: '42-054-10-2', ada: '10/2', alan: '32.100', malik: 'Ahmet Yılmaz', kayitli: 'Arpa', tarih: '15.08.2026' },
            { no: '42-054-10-3', ada: '10/3', alan: '18.000', malik: 'Ahmet Yılmaz', kayitli: 'Mısır', tarih: '15.08.2026' },
        ]
    },
    'mehmet': {
        name: 'Mehmet Demir', tc: '98765432109', no: '2025-1105', city: 'Ankara',
        parcels: [
            { no: '06-112-05-1', ada: '5/1', alan: '60.000', malik: 'Mehmet Demir', kayitli: 'Ayçiçeği', tarih: '01.09.2026' },
            { no: '06-112-05-2', ada: '5/2', alan: '12.500', malik: 'Mehmet Demir', kayitli: 'Yulaf', tarih: '01.09.2026' },
        ]
    }
};

window.selectFarmer = function(farmerId) {
    const farmer = farmersDb[farmerId];
    if (!farmer) return;

    // 1. Çiftçi Bilgilerini Güncelle
    document.getElementById('cks-farmer-name').textContent = farmer.name;
    document.getElementById('cks-farmer-tc').textContent = farmer.tc;
    document.getElementById('cks-farmer-no').textContent = farmer.no;
    document.getElementById('cks-farmer-city').textContent = farmer.city;
    document.getElementById('cks-farmer-count').textContent = farmer.parcels.length;

    // 2. Parsel Tablosunu Güncelle
    const tbody = document.getElementById('parsel-listesi-body');
    if (tbody) {
        let html = '';
        farmer.parcels.forEach(p => {
            html += `
                <tr style="border-bottom: 1px solid #e2e8f0;">
                    <td style="padding: 1rem 1.5rem; color: #1e293b; font-weight: 500;">${p.no}</td>
                    <td style="padding: 1rem 1.5rem; color: #64748b;">${p.ada}</td>
                    <td style="padding: 1rem 1.5rem; color: #64748b;">${p.alan}</td>
                    <td style="padding: 1rem 1.5rem; color: #64748b;">${p.malik}</td>
                    <td style="padding: 1rem 1.5rem; color: #1e293b; font-weight: 600;">${p.kayitli}</td>
                    <td style="padding: 1rem 1.5rem; color: #64748b;">${p.tarih}</td>
                    <td style="padding: 1rem 1.5rem;">
                        <button class="btn btn-secondary" style="padding: 4px 8px; font-size: 0.8rem;" onclick="switchTab('tab-arac-takip')">
                            <i class="fa-solid fa-eye"></i> İncele
                        </button>
                    </td>
                </tr>
            `;
        });
        tbody.innerHTML = html;
    }
}

window.populateNewTabs = function() {
    // Sayfa ilk açıldığında Osman Cingitaş'ı yükle
    window.selectFarmer('osman');
}

// Dom yüklendikten veya js scripti çalıştığında hemen doldur
window.populateNewTabs();

document.addEventListener('DOMContentLoaded', () => { fetch('/reset_simulation', { method: 'POST' }).then(() => { routeSegments.forEach(seg => map.removeLayer(seg)); routeSegments = []; currentSegment = null; lastRouteLatLng = null; window.isTeleporting = true; }); });
"""
    content = content[:start_idx] + new_end
    with open('src/dashboard/static/js/main.js', 'w') as f:
        f.write(content)
