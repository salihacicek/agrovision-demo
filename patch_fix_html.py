import re

with open('src/dashboard/templates/index.html', 'r') as f:
    html = f.read()

# I will find the Araç Yönetimi tab and completely replace it
start_marker = '<!-- ARAÇ YÖNETİMİ SEKMESİ -->'
end_marker = '<!-- ÇKS SEKMESİ -->'
start_idx = html.find(start_marker)
end_idx = html.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_filo_tab = """            <!-- ARAÇ YÖNETİMİ SEKMESİ -->
            <div id="tab-filo" class="tab-pane">
                <div style="padding: 1.5rem; max-width: 1400px; margin: 0 auto;">
                    
                    <div style="margin-bottom: 2rem;">
                        <h2 style="color: #1e293b; margin-top: -1rem; margin-bottom: 1rem; font-size: 1.5rem;">Araç Yönetim Merkezi</h2>
                        
                        <!-- BİRLEŞTİRİLMİŞ FİLO BLOĞU -->
                        <div style="background: #FAF6ED; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); overflow: hidden; display: flex; flex-direction: column;">
                            
                            <!-- KPI Bar -->
                            <div style="display: flex; border-bottom: 1px solid #e2e8f0; background: transparent;">
                                <div style="flex: 1; padding: 1.5rem; border-right: 1px solid #e2e8f0; border-bottom: 4px solid #78350f;">
                                    <div style="color: #64748b; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.5rem;">Toplam Araç</div>
                                    <div style="font-size: 1.875rem; font-weight: 700; color: #0f172a;">5</div>
                                </div>
                                <div style="flex: 1; padding: 1.5rem; border-right: 1px solid #e2e8f0; border-bottom: 4px solid #166534;">
                                    <div style="color: #64748b; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.5rem;">Aktif Hasatta</div>
                                    <div style="font-size: 1.875rem; font-weight: 700; color: #0f172a;">3</div>
                                </div>
                                <div style="flex: 1; padding: 1.5rem; border-right: 1px solid #e2e8f0; border-bottom: 4px solid #ca8a04;">
                                    <div style="color: #64748b; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.5rem;">Beklemede / Yolda</div>
                                    <div style="font-size: 1.875rem; font-weight: 700; color: #0f172a;">1</div>
                                </div>
                                <div style="flex: 1; padding: 1.5rem; border-bottom: 4px solid #991b1b;">
                                    <div style="color: #64748b; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.5rem;">Bakımda</div>
                                    <div style="font-size: 1.875rem; font-weight: 700; color: #0f172a;">1</div>
                                </div>
                            </div>
                            
                            <!-- Harita ve Liste -->
                            <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 0; height: 60vh; background: transparent;">
                                
                                <!-- Harita -->
                                <div style="background: transparent; border-right: 1px solid #e2e8f0; position: relative;">
                                    <div style="position: absolute; top: 0; left: 0; right: 0; background: rgba(250, 246, 237, 0.9); padding: 1rem; z-index: 1000; border-bottom: 1px solid #e2e8f0; font-weight: 600; color: #1e293b; display: flex; align-items: center; gap: 10px;">
                                        <i class="fa-solid fa-map-location-dot" style="color: #3b82f6;"></i> Canlı Araç Konumları
                                    </div>
                                    <div id="fleet-map" style="width: 100%; height: 100%; min-height: 500px;"></div>
                                </div>
                                
                                <!-- Araç Listesi -->
                                <div style="background: transparent; display: flex; flex-direction: column;">
                                    <div style="background: transparent; padding: 1.25rem; border-bottom: 1px solid #e2e8f0; font-weight: 600; color: #1e293b; display: flex; justify-content: space-between; align-items: center;">
                                        <span><i class="fa-solid fa-tractor" style="color: #10b981; margin-right: 8px;"></i> Araç Listesi</span>
                                        <span style="font-size: 0.75rem; background: #e2e8f0; padding: 3px 8px; border-radius: 12px; color: #475569;">Oto-Yenileme: Açık</span>
                                    </div>
                                    <div id="fleet-list" style="overflow-y: auto; flex: 1; padding: 1rem;">
                                        <!-- JS ile doldurulacak -->
                                    </div>
                                </div>
                                
                            </div>
                        </div> <!-- BİRLEŞTİRİLMİŞ FİLO BLOĞU KAPANIŞI -->
                    </div>
                </div>
            </div>

            """
    
    html = html[:start_idx] + new_filo_tab + html[end_idx:]

with open('src/dashboard/templates/index.html', 'w') as f:
    f.write(html)
