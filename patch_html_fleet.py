import re

with open('src/dashboard/templates/index.html', 'r') as f:
    content = f.read()

# 1. Update the Navbar
navbar_old = """                <a href="#" class="nav-link" data-target="tab-arac-takip">Canlı İzleme & Telemetri</a>
                <a href="#" class="nav-link" data-target="tab-cks">ÇKS & Parsel Yönetimi</a>
                <a href="#" class="nav-link" data-target="tab-raporlar">Hasat Raporları</a>"""

navbar_new = """                <a href="#" class="nav-link" data-target="tab-arac-takip">Canlı İzleme & Telemetri</a>
                <a href="#" class="nav-link" data-target="tab-filo">Filo Yönetimi</a>
                <a href="#" class="nav-link" data-target="tab-cks">ÇKS & Parsel Yönetimi</a>
                <a href="#" class="nav-link" data-target="tab-raporlar">Hasat Raporları</a>"""

content = content.replace(navbar_old, navbar_new)

# 2. Insert the new tab pane before tab-cks
tab_marker = """            <!-- ÇKS VE PARSEL YÖNETİMİ SEKMESİ -->
            <div id="tab-cks" class="tab-pane">"""

fleet_tab_html = """            <!-- FİLO YÖNETİMİ SEKMESİ -->
            <div id="tab-filo" class="tab-pane">
                <div style="padding: 1.5rem; max-width: 1400px; margin: 0 auto;">
                    
                    <!-- Başlık ve KPI'lar -->
                    <div style="margin-bottom: 2rem;">
                        <h2 style="color: #1e293b; margin-bottom: 1.5rem; font-size: 1.5rem;">Filo Yönetim Merkezi</h2>
                        
                        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5rem;">
                            <div style="background: white; padding: 1.5rem; border-radius: 12px; border: 1px solid #e2e8f0; border-left: 4px solid #3b82f6; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);">
                                <div style="color: #64748b; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.5rem;">Toplam Araç</div>
                                <div style="font-size: 1.875rem; font-weight: 700; color: #0f172a;">5</div>
                            </div>
                            <div style="background: white; padding: 1.5rem; border-radius: 12px; border: 1px solid #e2e8f0; border-left: 4px solid #10b981; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);">
                                <div style="color: #64748b; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.5rem;">Aktif Hasatta</div>
                                <div style="font-size: 1.875rem; font-weight: 700; color: #0f172a;">3</div>
                            </div>
                            <div style="background: white; padding: 1.5rem; border-radius: 12px; border: 1px solid #e2e8f0; border-left: 4px solid #f59e0b; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);">
                                <div style="color: #64748b; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.5rem;">Beklemede / Yolda</div>
                                <div style="font-size: 1.875rem; font-weight: 700; color: #0f172a;">1</div>
                            </div>
                            <div style="background: white; padding: 1.5rem; border-radius: 12px; border: 1px solid #e2e8f0; border-left: 4px solid #ef4444; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);">
                                <div style="color: #64748b; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.5rem;">Bakımda</div>
                                <div style="font-size: 1.875rem; font-weight: 700; color: #0f172a;">1</div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Harita ve Liste Kapsayıcı -->
                    <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 1.5rem; height: 60vh;">
                        
                        <!-- Harita -->
                        <div style="background: white; border-radius: 12px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); position: relative;">
                            <div style="position: absolute; top: 0; left: 0; right: 0; background: rgba(255,255,255,0.9); padding: 1rem; z-index: 1000; border-bottom: 1px solid #e2e8f0; font-weight: 600; color: #1e293b; display: flex; align-items: center; gap: 10px;">
                                <i class="fa-solid fa-map-location-dot" style="color: #3b82f6;"></i> Canlı Filo Konumları
                            </div>
                            <div id="fleet-map" style="width: 100%; height: 100%;"></div>
                        </div>
                        
                        <!-- Araç Listesi -->
                        <div style="background: white; border-radius: 12px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); display: flex; flex-direction: column;">
                            <div style="background: #f8fafc; padding: 1.25rem; border-bottom: 1px solid #e2e8f0; font-weight: 600; color: #1e293b; display: flex; justify-content: space-between; align-items: center;">
                                <span><i class="fa-solid fa-tractor" style="color: #10b981; margin-right: 8px;"></i> Araç Listesi</span>
                                <span style="font-size: 0.75rem; background: #e2e8f0; padding: 3px 8px; border-radius: 12px; color: #475569;">Oto-Yenileme: Açık</span>
                            </div>
                            
                            <div id="fleet-list" style="overflow-y: auto; flex: 1; padding: 1rem;">
                                <!-- JS ile doldurulacak -->
                            </div>
                        </div>
                        
                    </div>
                </div>
            </div>

            <!-- ÇKS VE PARSEL YÖNETİMİ SEKMESİ -->
            <div id="tab-cks" class="tab-pane">"""

content = content.replace(tab_marker, fleet_tab_html)

# 3. Add CSS for the fleet list hover effect
style_marker = "</style>"
fleet_style = """
    .fleet-item {
        padding: 1rem;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        margin-bottom: 1rem;
        cursor: pointer;
        transition: all 0.2s;
        background: #fff;
    }
    .fleet-item:hover {
        border-color: #cbd5e1;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transform: translateY(-2px);
    }
    .fleet-status-badge {
        font-size: 0.7rem;
        padding: 3px 8px;
        border-radius: 12px;
        font-weight: 600;
    }
    .status-hasat { background: #dcfce7; color: #166534; }
    .status-yol { background: #fef3c7; color: #92400e; }
    .status-bakim { background: #fee2e2; color: #991b1b; }
    
    .fuel-bar-container {
        height: 6px;
        background: #e2e8f0;
        border-radius: 3px;
        margin-top: 5px;
        overflow: hidden;
    }
    .fuel-bar-fill {
        height: 100%;
        background: #3b82f6;
        border-radius: 3px;
    }
</style>
"""
content = content.replace(style_marker, fleet_style)

with open('src/dashboard/templates/index.html', 'w') as f:
    f.write(content)

