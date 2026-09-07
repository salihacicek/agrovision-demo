import re

with open('src/dashboard/static/js/main.js', 'r') as f:
    content = f.read()

# Replace downloadReport and downloadPdfReport
marker_start = "let currentHarvestedDönüm = \"0.0\";"
marker_end = "function toggleReportDetail(rowId) {"

idx_start = content.find(marker_start)
idx_end = content.find(marker_end)

new_js = """let currentHarvestedDönüm = "0.0";

// Yeni Rapor Oluştur ve Sekmeye Geç
let reportCounter = 3;
function downloadReport() {
    const btn = document.querySelector('.tracker-header .btn-primary');
    
    // Aktif parsel verilerini bul
    const dropdown = document.getElementById('parcel-dropdown');
    let currentParcelId = dropdown ? dropdown.value : null;
    let activeParcel = null;
    let ownerName = "Bilinmiyor";
    
    if (currentParcelId) {
        // parcels listesinden harita id'siyle eşleştir
        activeParcel = parcels.find(p => p.id === currentParcelId);
        // ownerName bul (farmersDb)
        for (let key in farmersDb) {
            let f = farmersDb[key];
            let p = f.parcels.find(x => x.mapId === currentParcelId);
            if (p) {
                ownerName = f.name;
                activeParcel = {...activeParcel, ...p};
                break;
            }
        }
    }
    
    // Verileri hesapla
    const speedArr = trendChart.data.datasets[0].data.filter(s => s > 0);
    const speed = speedArr.length > 0 ? parseFloat((speedArr.reduce((a, b) => a + b, 0) / speedArr.length).toFixed(1)) : 0.0;
    
    let tempStr = document.getElementById('temp-val') ? document.getElementById('temp-val').textContent : "32.0 °C";
    let moistureStr = document.getElementById('crop-moisture-val') ? document.getElementById('crop-moisture-val').textContent : "%12.5";
    
    let temp = parseFloat(tempStr.replace(/[^0-9.]/g, '')) || 32.0;
    let moisture = parseFloat(moistureStr.replace(/[^0-9.]/g, '')) || 12.5;
    
    let harvested_area_donum = parseFloat(currentHarvestedDönüm.replace(/[^0-9.]/g, '')) || 0.0;
    let harvested_area_m2 = harvested_area_donum * 1000;
    
    let total_area_m2 = 0.0;
    let completion_pct = 0.0;
    let crop_type = "Bilinmiyor";
    let p_no = "Bilinmiyor";
    let p_ada = "Bilinmiyor";
    let p_city = "Bilinmiyor";
    
    if (activeParcel) {
        total_area_m2 = parseFloat(activeParcel.alan) || 0.0;
        completion_pct = total_area_m2 > 0 ? Math.min(100, (harvested_area_m2 / total_area_m2) * 100) : 0.0;
        crop_type = activeParcel.kayitli || "Bilinmiyor";
        p_no = activeParcel.no || "Bilinmiyor";
        p_ada = activeParcel.ada || "Bilinmiyor";
        
        // Find city from owner
        for (let key in farmersDb) {
            if (farmersDb[key].name === ownerName) {
                p_city = farmersDb[key].city;
            }
        }
    }
    
    // Verim Tahmini
    let base_yield = crop_type.toLowerCase() === 'mısır' ? 800 : (crop_type.toLowerCase() === 'buğday' ? 450 : 350);
    if (temp > 35) base_yield -= 50;
    if (temp < 20) base_yield -= 30;
    if (moisture > 15) base_yield -= 40;
    
    const payload = {
        parsel_no: p_no,
        ada_parsel: p_ada,
        owner: ownerName,
        declared_crop: crop_type,
        total_area_m2: total_area_m2,
        harvested_area_m2: harvested_area_m2,
        completion_pct: completion_pct,
        estimated_yield: base_yield,
        avg_speed: speed,
        avg_temp: temp,
        avg_moisture: moisture,
        lat: activeParcel ? (activeParcel.coords && activeParcel.coords[0] ? activeParcel.coords[0][0] : 0.0) : 0.0,
        lon: activeParcel ? (activeParcel.coords && activeParcel.coords[0] ? activeParcel.coords[0][1] : 0.0) : 0.0
    };
    
    const now = new Date();
    const dateStr = now.toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' });
    const timeStr = now.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' });
    
    const rowId = 'rep' + reportCounter;
    reportCounter++;
    
    const payloadStr = encodeURIComponent(JSON.stringify(payload));
    
    const tbody = document.getElementById('reports-tbody');
    if (tbody) {
        const newRowHTML = `
            <tr style="border-bottom: 1px solid #e2e8f0; background-color: #f0fdf4;">
                <td style="padding: 1rem 1.5rem; color: #1e293b; font-weight: 500;">${dateStr}<br><span style="font-size: 0.8rem; color: #64748b;">${timeStr}</span></td>
                <td style="padding: 1rem 1.5rem; color: #334155;">${currentParcelId || 'Bilinmiyor'} (${p_city})</td>
                <td style="padding: 1rem 1.5rem; color: #334155;">${harvested_area_donum} Dönüm (%${completion_pct.toFixed(1)})</td>
                
                <td style="padding: 1rem 1.5rem; text-align: right;">
                    <button class="btn btn-secondary" style="display: inline-block; padding: 0.4rem 0.8rem; font-size: 0.85rem;" onclick="viewReportDetails('${payloadStr}', '${dateStr}', '${timeStr}')">
                        <i class="fa-solid fa-eye"></i> İncele
                    </button>
                </td>
            </tr>
        `;
        tbody.insertAdjacentHTML('afterbegin', newRowHTML);
    }
    
    // Geçmiş Raporlar Sekmesine Atla
    switchTab('tab-raporlar');
    
    // Hemen PDF de indir
    downloadPdfReportDynamic(payload, btn);
}

function viewReportDetails(payloadStr, dateStr, timeStr) {
    const payload = JSON.parse(decodeURIComponent(payloadStr));
    
    document.getElementById('modal-report-date').textContent = `${dateStr} ${timeStr}`;
    document.getElementById('modal-report-owner').textContent = payload.owner;
    document.getElementById('modal-report-parcel').textContent = `Ada: ${payload.ada_parsel} | Parsel No: ${payload.parsel_no}`;
    document.getElementById('modal-report-crop').textContent = payload.declared_crop;
    
    document.getElementById('modal-report-total').textContent = (payload.total_area_m2 / 1000).toFixed(1) + ' Dönüm';
    document.getElementById('modal-report-harvested').textContent = (payload.harvested_area_m2 / 1000).toFixed(1) + ' Dönüm';
    document.getElementById('modal-report-pct').textContent = '%' + payload.completion_pct.toFixed(1);
    
    document.getElementById('modal-report-speed').textContent = payload.avg_speed + ' km/s';
    document.getElementById('modal-report-yield').textContent = payload.estimated_yield + ' kg/dekar';
    document.getElementById('modal-report-temp').textContent = payload.avg_temp + ' °C';
    document.getElementById('modal-report-moisture').textContent = '%' + payload.avg_moisture;
    
    // PDF Butonunu ayarla
    const pdfBtn = document.getElementById('modal-pdf-btn');
    pdfBtn.onclick = function() {
        downloadPdfReportDynamic(payload, pdfBtn);
    };
    
    document.getElementById('report-modal').style.display = 'flex';
}

function closeReportModal() {
    document.getElementById('report-modal').style.display = 'none';
}

function downloadPdfReportDynamic(payload, btnElement) {
    const originalText = btnElement.innerHTML;
    btnElement.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> İndiriliyor...';
    btnElement.disabled = true;
    
    fetch('/generate_report', { 
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(response => {
        if (!response.ok) throw new Error("Rapor oluşturulamadı");
        return response.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = `AgrovisionAI_Rapor_${new Date().toISOString().split('T')[0]}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        
        btnElement.innerHTML = originalText;
        btnElement.disabled = false;
    })
    .catch(err => {
        console.error(err);
        alert("Rapor indirilirken bir hata oluştu.");
        btnElement.innerHTML = originalText;
        btnElement.disabled = false;
    });
}

"""

content = content[:idx_start] + new_js + content[idx_end:]

with open('src/dashboard/static/js/main.js', 'w') as f:
    f.write(content)
