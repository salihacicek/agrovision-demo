import re

with open('src/dashboard/templates/index.html', 'r') as f:
    html = f.read()

# 1. CSS approach for Canlı İzleme (tracker-layout)
merge_css = """
/* TRACKER LAYOUT BÜTÜNLEŞTİRME (Canlı İzleme) */
body .tracker-layout {
    display: flex !important;
    flex-direction: column !important;
    gap: 0 !important;
    background: #FAF6ED !important;
    border-radius: 12px !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    overflow: hidden !important;
}
body .tracker-layout .map-section.card {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    border-radius: 0 !important;
    padding: 15px 15px 15px 15px !important;
    margin: 0 !important;
}
body .tracker-layout .telemetry-section {
    border-radius: 0 !important;
    border: none !important;
    border-top: 1px solid #e2e8f0 !important;
    box-shadow: none !important;
    margin-top: 0 !important;
}
"""

if "TRACKER LAYOUT BÜTÜNLEŞTİRME" not in html:
    html = html.replace("</style>", merge_css + "\n</style>")

# 2. HTML rewrite for Araç Yönetimi (tab-filo)
# Reduce top margin for title
html = html.replace('<h2 style="color: #1e293b; margin-bottom: 1.5rem; font-size: 1.5rem;">Araç Yönetim Merkezi</h2>',
                    '<h2 style="color: #1e293b; margin-top: -0.5rem; margin-bottom: 1rem; font-size: 1.5rem;">Araç Yönetim Merkezi</h2>')

# The KPI Bar container original:
kpi_container_start = '<div style="margin-bottom: 2rem;">'
# Actually, I'll just find the exact block and replace.
old_fleet_html = """                    <div style="margin-bottom: 2rem;">
                        <h2 style="color: #1e293b; margin-bottom: 1.5rem; font-size: 1.5rem;">Araç Yönetim Merkezi</h2>
                        
                        <div style="display: flex; background: #FAF6ED; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); overflow: hidden;">"""
new_fleet_html = """                    <div style="margin-bottom: 2rem;">
                        <h2 style="color: #1e293b; margin-top: -0.5rem; margin-bottom: 1rem; font-size: 1.5rem;">Araç Yönetim Merkezi</h2>
                        
                        <!-- BİRLEŞTİRİLMİŞ FİLO BLOĞU -->
                        <div style="background: #FAF6ED; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); overflow: hidden; display: flex; flex-direction: column;">
                            
                            <!-- KPI Bar (Artık iç border alt ve sağ çizgilerle ayrılıyor) -->
                            <div style="display: flex; border-bottom: 1px solid #e2e8f0; background: transparent;">"""
html = html.replace(old_fleet_html, new_fleet_html)

# We need to remove the closing div of the old KPI bar, and wrap the grid inside the new master container.
# Currently, it looks like:
#                             </div>
#                         </div>
#                     </div>
#                     
#                     <!-- Harita ve Liste Kapsayıcı -->
#                     <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 1.5rem; height: 60vh;">
#                         
#                         <!-- Harita -->
#                         <div style="background: #FAF6ED; border-radius: 12px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); position: relative;">

old_middle_html = """                            </div>
                        </div>
                    </div>
                    
                    <!-- Harita ve Liste Kapsayıcı -->
                    <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 1.5rem; height: 60vh;">
                        
                        <!-- Harita -->
                        <div style="background: #FAF6ED; border-radius: 12px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); position: relative;">"""

new_middle_html = """                            </div>
                            </div>
                            
                            <!-- Harita ve Liste Kapsayıcı (Gap kaldırıldı, iç border eklendi) -->
                            <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 0; height: 60vh; background: transparent;">
                                
                                <!-- Harita (Border ve shadow kaldırıldı, sağ tarafa border eklendi) -->
                                <div style="background: transparent; border-right: 1px solid #e2e8f0; position: relative;">"""
html = html.replace(old_middle_html, new_middle_html)

# Now we need to fix the List container
old_list_html = """                        <!-- Araç Listesi -->
                        <div style="background: #FAF6ED; border-radius: 12px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); display: flex; flex-direction: column;">
                            <div style="background: #FAF6ED; padding: 1.25rem; border-bottom: 1px solid #e2e8f0; font-weight: 600; color: #1e293b; display: flex; justify-content: space-between; align-items: center;">"""
new_list_html = """                        <!-- Araç Listesi (Border ve shadow kaldırıldı) -->
                        <div style="background: transparent; display: flex; flex-direction: column;">
                            <div style="background: transparent; padding: 1.25rem; border-bottom: 1px solid #e2e8f0; font-weight: 600; color: #1e293b; display: flex; justify-content: space-between; align-items: center;">"""
html = html.replace(old_list_html, new_list_html)

# And finally, close the master block after the List container
old_end_html = """                            <div id="fleet-list" style="overflow-y: auto; flex: 1; padding: 1rem;">
                                <!-- JS ile doldurulacak -->
                            </div>
                        </div>
                        
                    </div>
                </div>"""
new_end_html = """                            <div id="fleet-list" style="overflow-y: auto; flex: 1; padding: 1rem;">
                                <!-- JS ile doldurulacak -->
                            </div>
                        </div>
                        
                            </div> <!-- BİRLEŞTİRİLMİŞ FİLO BLOĞU KAPANIŞI -->
                    </div>
                </div>"""
html = html.replace(old_end_html, new_end_html)

# Bump CSS cache
html = html.replace('style.css?v=58', 'style.css?v=59')

with open('src/dashboard/templates/index.html', 'w') as f:
    f.write(html)
