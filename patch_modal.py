import re

with open('src/dashboard/templates/index.html', 'r') as f:
    content = f.read()

modal_html = """
    <!-- Report Details Modal -->
    <div id="report-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 9999; align-items: center; justify-content: center;">
        <div style="background: white; border-radius: 12px; width: 600px; max-width: 90%; box-shadow: 0 10px 25px rgba(0,0,0,0.2); overflow: hidden; display: flex; flex-direction: column;">
            
            <!-- Modal Header -->
            <div style="background: #1e293b; color: white; padding: 1.5rem; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3 style="margin: 0; font-size: 1.25rem;">Agrovision AI - Parsel Durum Raporu</h3>
                    <div style="font-size: 0.85rem; color: #94a3b8; margin-top: 5px;" id="modal-report-date"></div>
                </div>
                <button onclick="closeReportModal()" style="background: none; border: none; color: white; font-size: 1.25rem; cursor: pointer;"><i class="fa-solid fa-xmark"></i></button>
            </div>
            
            <!-- Modal Body -->
            <div style="padding: 1.5rem; overflow-y: auto; max-height: 70vh;">
                
                <h4 style="margin: 0 0 10px 0; color: #0f172a; border-bottom: 2px solid #f1f5f9; padding-bottom: 5px;">Parsel & ÇKS Bilgileri</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.5rem;">
                    <div><span style="color: #64748b; font-size: 0.85rem;">Malik:</span><br><b id="modal-report-owner" style="color: #1e293b;">-</b></div>
                    <div><span style="color: #64748b; font-size: 0.85rem;">Ada/Parsel:</span><br><b id="modal-report-parcel" style="color: #1e293b;">-</b></div>
                    <div><span style="color: #64748b; font-size: 0.85rem;">Kayıtlı Ürün:</span><br><b id="modal-report-crop" style="color: #1e293b;">-</b></div>
                </div>

                <h4 style="margin: 0 0 10px 0; color: #0f172a; border-bottom: 2px solid #f1f5f9; padding-bottom: 5px;">Hasat Sonuçları</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; margin-bottom: 1.5rem;">
                    <div style="background: #f8fafc; padding: 10px; border-radius: 8px;">
                        <span style="color: #64748b; font-size: 0.8rem;">Toplam Alan</span><br>
                        <b id="modal-report-total" style="color: #3b82f6; font-size: 1.1rem;">-</b>
                    </div>
                    <div style="background: #f8fafc; padding: 10px; border-radius: 8px;">
                        <span style="color: #64748b; font-size: 0.8rem;">Biçilen Alan</span><br>
                        <b id="modal-report-harvested" style="color: #10b981; font-size: 1.1rem;">-</b>
                    </div>
                    <div style="background: #f8fafc; padding: 10px; border-radius: 8px;">
                        <span style="color: #64748b; font-size: 0.8rem;">Tamamlanma</span><br>
                        <b id="modal-report-pct" style="color: #f59e0b; font-size: 1.1rem;">-</b>
                    </div>
                </div>

                <h4 style="margin: 0 0 10px 0; color: #0f172a; border-bottom: 2px solid #f1f5f9; padding-bottom: 5px;">Telemetri Özet</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                    <div><span style="color: #64748b; font-size: 0.85rem;">Tahmini Verim:</span><br><b id="modal-report-yield" style="color: #1e293b;">-</b></div>
                    <div><span style="color: #64748b; font-size: 0.85rem;">Ortalama Hız:</span><br><b id="modal-report-speed" style="color: #1e293b;">-</b></div>
                    <div><span style="color: #64748b; font-size: 0.85rem;">Ortalama Ürün Nemi:</span><br><b id="modal-report-moisture" style="color: #1e293b;">-</b></div>
                    <div><span style="color: #64748b; font-size: 0.85rem;">Hava Sıcaklığı:</span><br><b id="modal-report-temp" style="color: #1e293b;">-</b></div>
                </div>
            </div>
            
            <!-- Modal Footer -->
            <div style="background: #f8fafc; padding: 1rem 1.5rem; border-top: 1px solid #e2e8f0; display: flex; justify-content: flex-end; gap: 10px;">
                <button onclick="closeReportModal()" class="btn btn-secondary">Kapat</button>
                <button id="modal-pdf-btn" class="btn btn-primary"><i class="fa-solid fa-download"></i> PDF İndir</button>
            </div>
        </div>
    </div>
</body>"""

content = content.replace("</body>", modal_html)

with open('src/dashboard/templates/index.html', 'w') as f:
    f.write(content)
