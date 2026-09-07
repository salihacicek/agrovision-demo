import re

with open('src/dashboard/templates/index.html', 'r') as f:
    content = f.read()

start_marker = "<!-- ÇKS SEKMESİ (BİRLEŞTİRİLMİŞ) -->"
end_marker = "<!-- GEÇMİŞ RAPORLAR SEKMESİ -->"

idx_start = content.find(start_marker)
idx_end = content.find(end_marker)

new_html = """<!-- ÇKS SEKMESİ (BİRLEŞTİRİLMİŞ) -->
            <div id="tab-cks" class="tab-pane">
                <div style="margin-bottom: 2rem;">
                    <h2 style="margin: 0; color: #1e293b; font-size: 1.5rem;">Kayıtlı Çiftçiler</h2>
                    <p style="color: #64748b; margin-top: 5px;">Sisteme kayıtlı çiftçileri ve onlara ait parselleri görüntüleyin.</p>
                </div>
                
                <div class="card" style="padding: 0; overflow: hidden; margin-bottom: 2rem;">
                    <table style="width: 100%; border-collapse: collapse;">
                        <thead>
                            <tr style="background-color: #f8fafc; border-bottom: 2px solid #e2e8f0;">
                                <th style="padding: 1rem 1.5rem; text-align: left; color: #475569; font-weight: 600;">Çiftçi Adı</th>
                                <th style="padding: 1rem 1.5rem; text-align: left; color: #475569; font-weight: 600;">TC / ÇKS No</th>
                                <th style="padding: 1rem 1.5rem; text-align: left; color: #475569; font-weight: 600;">Kayıtlı İl</th>
                                <th style="padding: 1rem 1.5rem; text-align: right; color: #475569; font-weight: 600;">İşlemler</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr style="border-bottom: 1px solid #e2e8f0; transition: background-color 0.2s;" onmouseover="this.style.backgroundColor='#f1f5f9'" onmouseout="this.style.backgroundColor='transparent'">
                                <td style="padding: 1rem 1.5rem; color: #1e293b; font-weight: 600;">Osman Cingitaş<br><span style="font-size: 0.8rem; color: #64748b; font-weight: 400;">4 Parsel Kaydı</span></td>
                                <td style="padding: 1rem 1.5rem; color: #334155;">12345678901<br><span style="font-size: 0.8rem; color: #64748b;">2025-0158</span></td>
                                <td style="padding: 1rem 1.5rem; color: #334155;">Niğde</td>
                                <td style="padding: 1rem 1.5rem; text-align: right;">
                                    <button class="btn btn-secondary" style="padding: 0.4rem 0.8rem; font-size: 0.85rem;" onclick="selectFarmer('osman')">
                                        <i class="fa-solid fa-folder-open"></i> Parselleri Gör
                                    </button>
                                </td>
                            </tr>
                            <tr style="border-bottom: 1px solid #e2e8f0; transition: background-color 0.2s;" onmouseover="this.style.backgroundColor='#f1f5f9'" onmouseout="this.style.backgroundColor='transparent'">
                                <td style="padding: 1rem 1.5rem; color: #1e293b; font-weight: 600;">Mehmet Yıldız<br><span style="font-size: 0.8rem; color: #64748b; font-weight: 400;">4 Parsel Kaydı</span></td>
                                <td style="padding: 1rem 1.5rem; color: #334155;">98765432109<br><span style="font-size: 0.8rem; color: #64748b;">2025-1105</span></td>
                                <td style="padding: 1rem 1.5rem; color: #334155;">Ankara</td>
                                <td style="padding: 1rem 1.5rem; text-align: right;">
                                    <button class="btn btn-secondary" style="padding: 0.4rem 0.8rem; font-size: 0.85rem;" onclick="selectFarmer('mehmet')">
                                        <i class="fa-solid fa-folder-open"></i> Parselleri Gör
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div id="parcels-container" style="display: none;">
                    <div style="margin-bottom: 1.5rem; display: flex; align-items: center; justify-content: space-between;">
                        <h3 style="margin: 0; color: #1e293b; font-size: 1.25rem;"><i class="fa-solid fa-layer-group" style="color: #64748b; margin-right: 10px;"></i> <span id="selected-farmer-title">Çiftçi</span> Parselleri</h3>
                        <button class="btn btn-primary" style="padding: 6px 12px; font-size: 0.85rem;"><i class="fa-solid fa-plus"></i> Yeni Parsel Ekle</button>
                    </div>
                    
                    <div class="card" style="padding: 0; overflow: hidden;">
                        <table style="width: 100%; border-collapse: collapse; text-align: left;">
                            <thead>
                                <tr style="background-color: #f8fafc; border-bottom: 2px solid #e2e8f0;">
                                    <th style="padding: 1rem 1.5rem; color: #475569; font-weight: 600;">Parsel No</th>
                                    <th style="padding: 1rem 1.5rem; color: #475569; font-weight: 600;">Ada/Parsel</th>
                                    <th style="padding: 1rem 1.5rem; color: #475569; font-weight: 600;">Alan (m²)</th>
                                    <th style="padding: 1rem 1.5rem; color: #475569; font-weight: 600;">Malik</th>
                                    <th style="padding: 1rem 1.5rem; color: #475569; font-weight: 600;">Kayıtlı Ürün</th>
                                    <th style="padding: 1rem 1.5rem; color: #475569; font-weight: 600;">ÇKS Tarihi</th>
                                    <th style="padding: 1rem 1.5rem; color: #475569; font-weight: 600; text-align: center;">İşlem</th>
                                </tr>
                            </thead>
                            <tbody id="cks-parcels-tbody">
                                <!-- JS ile dinamik dolar -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            """

content = content[:idx_start] + new_html + content[idx_end:]

with open('src/dashboard/templates/index.html', 'w') as f:
    f.write(content)
