// Agrovision AI - Dashboard Frontend Logic

// --- Harita Kurulumu (Leaflet) ---
// Canvas renderer kullanıyoruz: SVG'ye kıyasla çok daha pürüzsüz ve performanslı çizim sağlar
const canvasRenderer = L.canvas({ padding: 0.5 });

const map = L.map('map', {
    attributionControl: false,
    maxZoom: 22,
    preferCanvas: true  // Tüm katmanlar için canvas kullan
}).setView([40.0880, 32.9950], 17);

L.control.attribution({prefix: '🇹🇷 Agrovision AI | Harita Sistemi'}).addTo(map);

L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri World Imagery',
    maxZoom: 22,
    maxNativeZoom: 18
}).addTo(map);

// --- TKGM GeoJSON Katmanı Kurulumu ---
let parcelGeoJsonLayer;
let routeSegments = [];
let parcels = []; // startOnParcel uyumluluğu için global dizi

// Parseller için istenen Özel GIS Stili (2px stroke, %40 transparan dolgu)
const tkgmStyle = {
    color: "#f59e0b",
    weight: 2,
    opacity: 1,
    fillColor: "#f59e0b",
    fillOpacity: 0.4,
    lineJoin: 'round',
    renderer: canvasRenderer
};

// Lokal JSON dosyasından GeoJSON Verisini Çek ve Render Et
async function loadTKGMParcels() {
    try {
        const response = await fetch('/static/assets/data/parseller.json');
        if (!response.ok) throw new Error("Parsel verisi alınamadı");
        
        const geojsonData = await response.json();
        parcels = []; // Sıfırla

        if (parcelGeoJsonLayer) {
            map.removeLayer(parcelGeoJsonLayer);
        }

        parcelGeoJsonLayer = L.geoJSON(geojsonData, {
            style: tkgmStyle,
            onEachFeature: function (feature, layer) {
                const props = feature.properties;
                
                // Tarlanın gerçek kıvrımlarını (tüm noktaları) Enlem, Boylam formatına çevir
                const latlngs = feature.geometry.coordinates[0].map(coord => [coord[1], coord[0]]);

                parcels.push({
                    id: props.parsel_id,
                    coords: latlngs // 4 köşeli sahte sınır kutusunu değil, tarlanın gerçek koordinatlarını gönder
                });
                const popupContent = `
                    <div style="text-align: center; font-family: 'Inter', sans-serif;">
                        <b>Ada: ${props.ada_no} | Parsel: ${props.parsel_no}</b><br>
                        Malik: ${props.malik_adi}<br>
                        Alan: ${props.alan_donum} Dönüm<br>
                        Kayıtlı Ürün: ${props.urun_tipi}<br><br>
                        <button onclick="startOnParcel('${props.parsel_id}')" 
                                style="background: #3b82f6; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer;">
                            Bu Parselde Başla
                        </button>
                    </div>
                `;
                layer.bindPopup(popupContent);
                
                layer.on({
                    mouseover: function (e) {
                        const l = e.target;
                        l.setStyle({ fillOpacity: 0.4, weight: 3, color: '#ef4444' });
                    },
                    mouseout: function (e) {
                        parcelGeoJsonLayer.resetStyle(e.target);
                    }
                });

                // Her parselin ortasına id yazan bir marker ekle
                const bounds = layer.getBounds();
                const center = bounds.getCenter();
                L.marker(center, {
                    icon: L.divIcon({
                        className: '',
                        html: `<div class="parcel-label">${props.parsel_id}</div>`,
                        iconAnchor: [16, 10]
                    })
                }).bindPopup(popupContent).addTo(map);
            }
        }).addTo(map);
        
    } catch (error) {
        console.error("GIS Katman Hatası:", error);
    }
}

// Harita yüklendiğinde fonksiyonu tetikle
loadTKGMParcels();


// Yeni parsele geçildiğinde hasat rotasını temizlemek için global fonksiyon
window.inceleParsel = function(mapId) {
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
    
    if (parcelGeoJsonLayer) {
        parcelGeoJsonLayer.eachLayer(function(l) {
            parcelGeoJsonLayer.resetStyle(l);
            if (l.feature.properties.parsel_id === mapId) {
                l.setStyle({ fillOpacity: 0.7, weight: 4, color: '#eab308' });
                map.flyToBounds(l.getBounds(), { padding: [50, 50], duration: 1.5 });
                setTimeout(() => { l.openPopup(); }, 1500); // Popup aç
            }
        });
    }
}

window.currentActiveParcelId = null;
window.startOnParcel = function(parcelId) {
    const parcel = parcels.find(p => p.id === parcelId);
    if (!parcel) return;
    
    window.currentActiveParcelId = parcelId;
    const dropdown = document.getElementById('parcel-dropdown');
    if (dropdown) dropdown.value = parcelId;

    // Renklendirme ve stil sıfırlama (highlight)
    if (parcelGeoJsonLayer) {
        parcelGeoJsonLayer.eachLayer(function(l) {
            parcelGeoJsonLayer.resetStyle(l);
            if (l.feature.properties.parsel_id === parcelId) {
                l.setStyle({ fillOpacity: 0.7, weight: 4, color: '#eab308' }); // sarı highlight
                map.flyToBounds(l.getBounds(), { padding: [50, 50], duration: 1.5 });
            }
        });
    }

    // Haritadaki mevcut rotayı temizle
    routeSegments.forEach(seg => map.removeLayer(seg));
    routeSegments = [];
    currentSegment = null;
    lastRouteLatLng = null;
    window.isTeleporting = true;
    
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
    fetch('/set_target_parcel', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ coords: parcel.coords })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log(parcelId + " parseline geçiş yapıldı.");
            map.closePopup();
        } else {
            console.error("Parsel değiştirilemedi.");
        }
    })
    .catch(err => console.error("Hata:", err));
};

// --- Biçerdöver Marker: CSS Geçişli DivIcon (60 FPS pürüzsüz hareket) ---
const harvesterIcon = L.divIcon({
    className: '',
    html: `<div class="harvester-dot">
             <div class="harvester-pulse"></div>
             <div class="harvester-core"></div>
           </div>`,
    iconSize: [28, 28],
    iconAnchor: [14, 14],
    popupAnchor: [0, -16]
});

// ── P157 içinde başlat (GPS sim'in ilk waypoint'i burası) ──
let marker = L.marker([40.210020, 33.010096], { icon: harvesterIcon }).addTo(map);
marker.bindPopup("<b>Agrovision AI</b><br>Biçerdöver Aktif").openPopup();

// Hasat izi — hız limitine göre mavi/kırmızı segmentler
const SPEED_LIMIT = 8.0; // km/h üstü = tane kaybı tehlikesi (kırmızı)
let currentSegment = null;
let currentSegmentIsRed = false;
let lastRouteLatLng = null;

function addRoutePoint(lat, lon, speed) {
    const latlng = [lat, lon];
    
    // Zıplama / Işınlanma kontrolü (Eski paketten yeni pakete geçerken gecikme yüzünden oluşan dev çizgiyi önler)
    if (lastRouteLatLng) {
        const dLat = lat - lastRouteLatLng[0];
        const dLon = lon - lastRouteLatLng[1];
        const jumpDistance = Math.sqrt(dLat * dLat + dLon * dLon);
        
        // Eğer anlık sıçrama 0.0002 dereceden (yaklaşık 20 metre) büyükse bu bir ışınlanmadır.
        // Çizgiyi kes ve yeni noktadan sessizce başlat.
        if (jumpDistance > 0.0002) {
            currentSegment = null;
            lastRouteLatLng = latlng;
            window.isTeleporting = false;
            return;
        }
    }
    
    window.isTeleporting = false; // Temizle
    const isHighSpeed = speed >= SPEED_LIMIT;

    // Segment rengi değiştiyse veya hiç segment yoksa yeni segment başlat
    if (!currentSegment || isHighSpeed !== currentSegmentIsRed) {
        // Önceki segmentten son noktayı al (bağlantı kopmaması için)
        const startPoints = lastRouteLatLng ? [lastRouteLatLng, latlng] : [latlng];
        currentSegment = L.polyline(startPoints, {
            color: isHighSpeed ? '#ef4444' : '#3b82f6',
            weight: isHighSpeed ? 6 : 5,
            opacity: 0.85,
            lineJoin: 'round',
            lineCap: 'round'
        }).addTo(map);
        routeSegments.push(currentSegment);
        currentSegmentIsRed = isHighSpeed;
    } else {
        currentSegment.addLatLng(latlng);
    }
    lastRouteLatLng = latlng;
}

// --- Gerçek zamanlı interpolasyon için hedef pozisyon ---
let targetLat = 40.210020;
let targetLon = 33.010096;
let currentDisplayLat = 40.210020;
let currentDisplayLon = 33.010096;
let interpolationFrame = null;
const INTERP_SPEED = 0.18;

// Kullanıcı haritayı sürüklerse otomatik takibi geçici olarak durdur
let userDraggedMap = false;
let dragResumeTimer = null;

function interpolatePosition() {
    const dlat = targetLat - currentDisplayLat;
    const dlon  = targetLon  - currentDisplayLon;
    
    if (Math.abs(dlat) > 1e-8 || Math.abs(dlon) > 1e-8) {
        currentDisplayLat += dlat * INTERP_SPEED;
        currentDisplayLon  += dlon  * INTERP_SPEED;
        marker.setLatLng([currentDisplayLat, currentDisplayLon]);
        
        // Sadece kullanıcı sürüklemiyorsa haritayı otomatik takip et
        if (!userDraggedMap) {
            map.panTo([currentDisplayLat, currentDisplayLon], { animate: false });
        }
    }
    
    requestAnimationFrame(interpolatePosition);
}
requestAnimationFrame(interpolatePosition);

// Kullanıcı haritayı sürüklemeye başlayınca takibi durdur
map.on('dragstart', () => {
    userDraggedMap = true;
    if (dragResumeTimer) clearTimeout(dragResumeTimer);
});

// 5 saniye sonra otomatik takibe geri dön
map.on('dragend', () => {
    if (dragResumeTimer) clearTimeout(dragResumeTimer);
    dragResumeTimer = setTimeout(() => {
        userDraggedMap = false;
    }, 5000);
});

// ─── WebSocket Bağlantısı — Sunucudan canlı veri al ────────────────
const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const WS_URL = `${wsProtocol}//${window.location.host}/ws`;
let ws;

function connectWebSocket() {
    ws = new WebSocket(WS_URL);

    ws.onopen = () => {
        console.log('✅ WebSocket bağlandı:', WS_URL);
    };

    ws.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            updateDashboard(data);
        } catch(e) {
            console.error('WS mesaj parse hatası:', e);
        }
    };

    ws.onerror = (err) => {
        console.warn('WebSocket hatası, yeniden bağlanılacak...', err);
    };

    ws.onclose = () => {
        console.log('WebSocket kapandı, 2 saniye sonra yeniden bağlanılacak...');
        setTimeout(connectWebSocket, 2000);
    };
}
connectWebSocket();




// --- Grafik Kurulumu (Chart.js) ---
const ctx = document.getElementById('trendChart').getContext('2d');
Chart.defaults.color = '#94a3b8';
Chart.defaults.font.family = 'Inter';

const trendChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array(20).fill(''),
            datasets: [
                {
                    label: 'Hız (km/s)',
                    data: Array(20).fill(0),
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            scales: {
                y: { beginAtZero: true, max: 15 },
                x: { display: false }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });

async function loadReports() {
    const tbody = document.getElementById('reportsList');
    if (!tbody) return;
    
    tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;">Yükleniyor...</td></tr>';
    
    try {
        const response = await fetch('/api/reports');
        if (!response.ok) throw new Error("Raporlar alinamadi");
        const reports = await response.json();
        
        tbody.innerHTML = '';
        if (reports.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;">Henüz rapor bulunmuyor.</td></tr>';
            return;
        }
        
        reports.forEach((report, index) => {
            // Ana Satir
            const trMain = document.createElement('tr');
            trMain.className = 'main-row';
            
            // Formatlama
            const dt = new Date(report.timestamp);
            const dateStr = dt.toLocaleString('tr-TR');
            const donum = (report.harvested_area_m2 / 1000).toFixed(2);
            const detectedStr = `${report.detected_crop.charAt(0).toUpperCase() + report.detected_crop.slice(1)} (%${report.confidence})`;
            const declaredStr = report.declared_crop ? report.declared_crop.charAt(0).toUpperCase() + report.declared_crop.slice(1) : '-';
            
            let statusHtml = '';
            let s = (report.cks_audit_status || '').toUpperCase();
            if (s.includes('UYGUN') && !s.includes('UYUMSUZ')) {
                statusHtml = `<span class="status-badge uygun">Uygun</span>`;
            } else if (s.includes('UYUMSUZ')) {
                statusHtml = `<span class="status-badge uyumsuz">Uyumsuz</span>`;
            } else {
                statusHtml = `<span class="status-badge" style="background:#f1f5f9;color:#64748b;">${report.cks_audit_status}</span>`;
            }
            
            trMain.innerHTML = `
                <td style="text-align:center;"><i class="fa-solid fa-chevron-down expand-icon"></i></td>
                <td>${dateStr}</td>
                <td>${declaredStr}</td>
                <td>${detectedStr}</td>
                <td>${donum} Dönüm</td>
                <td>${statusHtml}</td>
                <td><button class="btn btn-secondary download-btn" data-file="${report.filename}"><i class="fa-solid fa-download"></i> İndir</button></td>
            `;
            
            // Detay Satiri
            const trDetail = document.createElement('tr');
            trDetail.className = 'detail-row';
            const detailHtml = `
                <td colspan="7">
                    <div class="detail-content">
                        <h4><i class="fa-solid fa-file-lines"></i> OtEne Labs - Parsel Durum Raporu Önizlemesi</h4>
                        <div class="detail-grid">
                            <div>
                                <p><strong>Parsel Bilgileri</strong></p>
                                <p>Parsel No: ${report.parsel_no}</p>
                                <p>Ada/Parsel: ${report.ada_parsel}</p>
                                <p>Alan: ${report.harvested_area_m2.toFixed(0)} m2 (${donum} donum)</p>
                                <p>Malik: ${report.owner}</p>
                            </div>
                            <div>
                                <p><strong>ÇKS Kayıt Bilgileri</strong></p>
                                <p>Kayıtlı Ürün: ${declaredStr}</p>
                                <p>Hasat Tarihi: ${report.harvest_date}</p>
                                <p>Çiftçi: ${report.owner}</p>
                            </div>
                            <div>
                                <p><strong>AI Tespit Sonuçları</strong></p>
                                <p>Tespit Edilen: ${detectedStr}</p>
                                <p>Güven Oranı: %${report.confidence}</p>
                                <p>Durum: ${s}</p>
                            </div>
                        </div>
                    </div>
                </td>
            `;
            trDetail.innerHTML = detailHtml;
            
            // Accordion Tıklama Olayı (Buton harici yerler için)
            trMain.addEventListener('click', (e) => {
                if (e.target.closest('.download-btn')) return; // indirme butonuna basıldıysa açma
                
                trDetail.classList.toggle('open');
                const icon = trMain.querySelector('.expand-icon');
                if(icon) icon.classList.toggle('open');
            });
            
            // İndirme Olayı
            const dlBtn = trMain.querySelector('.download-btn');
            if (dlBtn) {
                dlBtn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    window.location.href = '/download_report/' + report.filename;
                });
            }
            
            tbody.appendChild(trMain);
            tbody.appendChild(trDetail);
        });
        
    } catch (error) {
        console.error("Raporlar yüklenemedi:", error);
        tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; color:red;">Hata oluştu.</td></tr>';
    }
}

// --- GİZLİLİK VE KVKK YÖNETİMİ MANTIĞI ---
document.addEventListener('DOMContentLoaded', () => {
    const modeRadios = document.querySelectorAll('input[name="privacy_mode"]');
    const modeCards = document.querySelectorAll('.mode-option-card');
    const topMask = document.getElementById('topMask');
    const activeCropZone = document.getElementById('activeCropZone');


    const roiActiveStatus = document.getElementById('roiActiveStatus');
    const blindOverlay = document.getElementById('blind-mode-overlay');
    const liveBadge = document.getElementById('livePrivacyBadge');
    const btnSavePrivacy = document.getElementById('btnSavePrivacySettings');
    const btnDownloadKvkk = document.getElementById('btnDownloadKvkkCert');
    const chkAutoMask = document.getElementById('chkAutoMask');

    function applyPrivacyMode(mode) {
        // Kart seçili stillerini güncelle
        modeCards.forEach(card => card.classList.remove('selected'));
        const selectedCard = document.querySelector(`input[name="privacy_mode"][value="${mode}"]`)?.closest('.mode-option-card');
        if (selectedCard) selectedCard.classList.add('selected');

        // Simülatör ve Canlı Ekranı Güncelle
        if (mode === 'cutter') {
            if (topMask) {
                topMask.style.display = 'flex';
                topMask.style.flex = '1';
                topMask.innerHTML = '<span class="mask-badge"><i class="fa-solid fa-eye-slash"></i> Maskelenmiş Çevre / Gökyüzü (Gizlilik Korumalı)</span>';
            }
            if (activeCropZone) {
                activeCropZone.style.display = 'flex';
                activeCropZone.style.height = '110px';
            }
            if (roiActiveStatus) roiActiveStatus.textContent = 'Alt %40 Tabla Odaklı (Önerilen)';
            if (blindOverlay) blindOverlay.style.display = 'none';
            if (liveBadge) {
                liveBadge.style.background = 'rgba(16, 185, 129, 0.15)';
                liveBadge.style.color = '#10b981';
                liveBadge.innerHTML = '<i class="fa-solid fa-shield-halved"></i> KVKK & Tabla Korumalı';
            }
        } else if (mode === 'blind') {
            if (topMask) {
                topMask.style.display = 'flex';
                topMask.style.flex = '1';
                topMask.innerHTML = '<span class="mask-badge" style="background: rgba(59, 130, 246, 0.2); color: #60a5fa; border-color: rgba(59, 130, 246, 0.4);"><i class="fa-solid fa-eye-slash"></i> Tam Kör Mod (Canlı Akış Gizli)</span>';
            }
            if (activeCropZone) activeCropZone.style.display = 'none';
            if (roiActiveStatus) roiActiveStatus.textContent = 'Kör Dashboard (Video Yok - Yalnızca Metrikler)';
            if (blindOverlay) blindOverlay.style.display = 'flex';
            if (liveBadge) {
                liveBadge.style.background = 'rgba(59, 130, 246, 0.15)';
                liveBadge.style.color = '#3b82f6';
                liveBadge.innerHTML = '<i class="fa-solid fa-eye-slash"></i> Kör Mod Aktif';
            }
        } else if (mode === 'full') {
            if (topMask) topMask.style.display = 'none';
            if (activeCropZone) {
                activeCropZone.style.display = 'flex';
                activeCropZone.style.height = '100%';
            }
            if (roiActiveStatus) roiActiveStatus.textContent = 'Tam Kadraj (Standart Geniş Açı)';
            if (blindOverlay) blindOverlay.style.display = 'none';
            if (liveBadge) {
                liveBadge.style.background = 'rgba(148, 163, 184, 0.15)';
                liveBadge.style.color = '#94a3b8';
                liveBadge.innerHTML = '<i class="fa-solid fa-expand"></i> Standart Geniş Kadraj';
            }
        }
    }

    modeRadios.forEach(radio => {
        radio.addEventListener('change', (e) => {
            applyPrivacyMode(e.target.value);
        });
    });

    if (chkAutoMask) {
        chkAutoMask.addEventListener('change', (e) => {
            if (topMask) {
                topMask.style.opacity = e.target.checked ? '1' : '0.3';
            }
        });
    }

    if (btnSavePrivacy) {
        btnSavePrivacy.addEventListener('click', () => {
            const currentMode = document.querySelector('input[name="privacy_mode"]:checked')?.value || 'cutter';
            btnSavePrivacy.innerHTML = '<i class="fa-solid fa-circle-check"></i> Ayarlar Kaydedildi!';
            btnSavePrivacy.classList.remove('btn-primary');
            btnSavePrivacy.classList.add('btn-success');

            setTimeout(() => {
                btnSavePrivacy.innerHTML = '<i class="fa-solid fa-floppy-disk"></i> Ayarları Kaydet';
                btnSavePrivacy.classList.remove('btn-success');
                btnSavePrivacy.classList.add('btn-primary');
            }, 2500);
        });
    }

    if (btnDownloadKvkk) {
        btnDownloadKvkk.addEventListener('click', () => {
            alert("📋 Agrovision AI - KVKK & Çiftçi Mahremiyeti Taahhüt Belgesi:\n\n1. Sistemde ham video kaydı tutulmaz (%100 RAM içi anlık çıkarım).\n2. Kamera dar açılı tabla odağında çalışır; çevre yapılar ve insan yüzleri filtrelenir.\n3. Sadece hasat telemetrisi (işlenen dönüm, ortalama ürün tipi) saklanır.\n\nBelge hazırlandı.");
        });
    }
});


// --- Oynat/Durdur Kontrolü ---
function togglePlay() {
    if (!window.currentActiveParcelId) {
        alert("Lütfen önce listeden veya haritadan bir parsel seçip 'Bu Parselde Başla' işlemini yapın!");
        return;
    }
    fetch('/toggle_play', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if(data.status === 'success') {
                const btn = document.getElementById('toggle-play-btn');
                const icon = btn.querySelector('i');
                const text = btn.querySelector('span');
                
                if (data.is_playing) {
                    // Sistem şu an çalışıyor
                    btn.classList.remove('paused');
                    icon.className = 'fa-solid fa-pause';
                    text.textContent = 'Durdur';
                    isTrackingPaused = false;
                } else {
                    // Sistem durduruldu
                    btn.classList.add('paused');
                    icon.className = 'fa-solid fa-play';
                    text.textContent = 'Başlat';
                    isTrackingPaused = true;
                }
            }
        });
}


let currentHarvestedDönüm = "0.0";

// Yeni Rapor Oluştur ve Sekmeye Geç
let reportCounter = 3;
function downloadReport() {
    // Aktif parsel verilerini bul
    let currentParcelId = window.currentActiveParcelId;
    if (!currentParcelId) {
        const dropdown = document.getElementById('parcel-dropdown');
        currentParcelId = dropdown ? dropdown.value : null;
    }
    
    if (!currentParcelId) {
        alert("Lütfen önce listeden veya haritadan bir parsel seçip başlatın. Parsel verisi olmadan rapor alınamaz!");
        return;
    }

    const btn = document.querySelector('.tracker-header .btn-primary');
    if (!currentParcelId) {
        const dropdown = document.getElementById('parcel-dropdown');
        currentParcelId = dropdown ? dropdown.value : null;
    }
    
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

function toggleReportDetail(rowId) {
    const row = document.getElementById(rowId);
    if (row.style.display === 'none') {
        row.style.display = 'table-row';
    } else {
        row.style.display = 'none';
    }
}


function updateDashboard(data) {
    if (!data) return;


    // ── Harita: interpolasyon hedefini güncelle ──
    if (data.lat && data.lon) {
        targetLat = data.lat;
        targetLon = data.lon;
        // Hız limitine göre mavi/kırmızı rota çizgisi
        addRoutePoint(data.lat, data.lon, data.speed || 0);
    }

    // ── Grafik: Hız grafiği ──
    if (data.speed !== undefined) {
        const now = new Date();
        const timeLabel = now.getHours() + ':' + now.getMinutes().toString().padStart(2,'0') + ':' + now.getSeconds().toString().padStart(2,'0');
        trendChart.data.labels.push(timeLabel);
        trendChart.data.datasets[0].data.push(data.speed);
        if (trendChart.data.labels.length > 20) {
            trendChart.data.labels.shift();
            trendChart.data.datasets[0].data.shift();
        }
        trendChart.update('none');
    }

    // ── DOM: Telemetri değerleri ──
    if (data.speed !== undefined) {
        const el = document.getElementById('current-speed');
        if (el) el.textContent = data.speed.toFixed(1);
    }
    if (data.temperature !== undefined) {
        const el = document.getElementById('temp-val');
        if (el) el.textContent = data.temperature.toFixed(1) + ' °C';
    }
    if (data.humidity !== undefined) {
        const el = document.getElementById('humidity-val');
        if (el) el.textContent = '%' + data.humidity.toFixed(1);
    }
    if (data.crop_moisture !== undefined) {
        const el = document.getElementById('crop-moisture-val');
        if (el) el.textContent = '%' + data.crop_moisture.toFixed(1);
    }
    if (data.harvested_area_m2 !== undefined) {
        currentHarvestedDönüm = (data.harvested_area_m2 / 1000).toFixed(2);
        const el = document.getElementById('harvested-area');
        if (el) el.textContent = currentHarvestedDönüm;
    }

    // ── Ortalama değerler kartı ──
    if (data.temperature !== undefined) {
        const el = document.getElementById('avg-temp');
        if (el) el.textContent = data.temperature.toFixed(1);
    }
    if (data.crop_moisture !== undefined) {
        const el = document.getElementById('avg-moisture');
        if (el) el.textContent = '%' + data.crop_moisture.toFixed(1);
    }

    // ── Oynat/Durdur Butonunu Sunucu ile Senkronize Et ──
    if (data.is_paused !== undefined) {
        const btn = document.getElementById('toggle-play-btn');
        if (btn) {
            const icon = btn.querySelector('i');
            const text = btn.querySelector('span');
            if (data.is_paused) {
                btn.classList.add('paused');
                icon.className = 'fa-solid fa-play';
                text.textContent = 'Başlat';
                if (typeof isTrackingPaused !== 'undefined') isTrackingPaused = true;
            } else {
                btn.classList.remove('paused');
                icon.className = 'fa-solid fa-pause';
                text.textContent = 'Durdur';
                if (typeof isTrackingPaused !== 'undefined') isTrackingPaused = false;
            }
        }
    }

    // Lite Mode Kontrolü
    if (data.source === "lite_mode") {
        const blindOverlay = document.getElementById("blind-mode-overlay");
        if (blindOverlay) {
            blindOverlay.style.display = "flex";
            blindOverlay.innerHTML = "<i class=\"fa-solid fa-bolt\" style=\"font-size: 3.5rem; color: #10b981; margin-bottom: 1rem;\"></i><h3 style=\"color: #fff; margin-bottom: 0.5rem;\">Sınırsız (Lite) Mod Aktif</h3><p style=\"max-width: 380px; font-size: 0.9rem;\">Görüntü işleme motoru şu an kapalıdır. 7/24 Kesintisiz GPS rotası, Takograf, Telemetri ve Harita özellikleri devrededir.</p>";
        }
    }
}


// --- SEKME (TAB) DEĞİŞTİRME MANTIĞI ---
// Global fonksiyon — onclick ile direkt çağrılabilir, DOMContentLoaded'a gerek yok

function switchTab(targetId) {
    const allPanes = document.querySelectorAll('.tab-pane');
    const allLinks = document.querySelectorAll('.nav-link');

    // Önce hepsini gizle
    allPanes.forEach(p => {
        p.classList.remove('active');
        p.style.display = 'none';
    });
    allLinks.forEach(l => l.classList.remove('active'));

    // Hedef sekmeyi göster
    const target = document.getElementById(targetId);
    if (target) {
        target.classList.add('active');
        if (targetId === 'tab-arac-takip') {
            target.style.display = 'grid';
            setTimeout(() => { if (typeof map !== 'undefined') map.invalidateSize(); }, 200);
        } else if (targetId === 'tab-anasayfa') {
            target.style.display = 'flex';
        } else {
            target.style.display = 'block';
        }
    }

    // Navbar linkini aktif yap
    const activeLink = document.querySelector(`.nav-link[data-target="${targetId}"]`);
    if (activeLink) activeLink.classList.add('active');
}

// Nav linklerine tıklama dinleyicisi ekle (DOMContentLoaded'da güvenli)
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
        name: 'Osman Cingitaş', tc: '12345678901', no: '2025-0158', city: 'Ankara',
        parcels: [
            { no: '51-113-25-1', ada: '25/1', alan: 25000, malik: 'Osman Cingitaş', kayitli: 'Ayçiçeği', tarih: '20.07.2026', mapId: 'P1789' },
            { no: '51-113-25-2', ada: '25/2', alan: 25000, malik: 'Osman Cingitaş', kayitli: 'Mısır', tarih: '20.07.2026', mapId: 'P1826' },
            { no: '51-113-25-3', ada: '25/3', alan: 25000, malik: 'Osman Cingitaş', kayitli: 'Mısır', tarih: '20.07.2026', mapId: 'P1959' },
            { no: '51-113-25-4', ada: '25/4', alan: 25000, malik: 'Osman Cingitaş', kayitli: 'Mısır', tarih: '20.07.2026', mapId: 'P1986' }
        ]
    },
    'mehmet': {
        name: 'Mehmet Yıldız', tc: '98765432109', no: '2025-1105', city: 'Ankara',
        parcels: [
            { no: '06-112-05-1', ada: '5/1', alan: 60000, malik: 'Mehmet Yıldız', kayitli: 'Mısır', tarih: '01.09.2026', mapId: 'P2017' },
            { no: '06-112-05-2', ada: '5/2', alan: 12500, malik: 'Mehmet Yıldız', kayitli: 'Arpa', tarih: '01.09.2026', mapId: 'P2044' },
            { no: '06-112-05-3', ada: '5/3', alan: 15000, malik: 'Mehmet Yıldız', kayitli: 'Buğday', tarih: '01.09.2026', mapId: 'P2074' },
            { no: '06-112-05-4', ada: '5/4', alan: 18000, malik: 'Mehmet Yıldız', kayitli: 'Mısır', tarih: '01.09.2026', mapId: 'P2093' }
        ]
    }
};

window.selectFarmer = function(farmerId) {
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
        tbody.innerHTML = html;
    }
}

window.populateNewTabs = function() {
    // Sayfa ilk açıldığında Osman Cingitaş'ı yükle
    window.selectFarmer(''); // Boş başlat
}

// Dom yüklendikten veya js scripti çalıştığında hemen doldur
window.populateNewTabs();

document.addEventListener('DOMContentLoaded', () => { fetch('/reset_simulation', { method: 'POST' }).then(() => { routeSegments.forEach(seg => map.removeLayer(seg)); routeSegments = []; currentSegment = null; lastRouteLatLng = null; window.isTeleporting = true; }); });
