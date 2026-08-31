import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime

class PDFReportGenerator:
    """Otenelabs formatında PDF raporları oluşturan sınıf."""
    
    def __init__(self, output_dir: str = "exports"):
        # app.py'daki export_dir ile tutarlı olsun diye exports yapıyorum
        self.output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../exports"))
        os.makedirs(self.output_dir, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()

    def _create_custom_styles(self):
        """Otenelabs özel stillerini tanımlar."""
        self.styles.add(ParagraphStyle(
            name='OtEneTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=colors.black,
            alignment=0, # Sol
            spaceAfter=5
        ))
        
        self.styles.add(ParagraphStyle(
            name='OtEneSub',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.gray,
            spaceAfter=25
        ))

        self.styles.add(ParagraphStyle(
            name='OtEneHeading',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=colors.black,
            spaceBefore=15,
            spaceAfter=10,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='OtEneNormal',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.black,
            spaceAfter=6,
            leading=16
        ))
        
        self.styles.add(ParagraphStyle(
            name='OtEneFooter',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.gray,
            spaceBefore=40
        ))

    def generate_report(self, session_data: dict, output_filename: str = None) -> str:
        """JSON veya dictionary verilerinden PDF raporu üretir."""
        if output_filename is None:
            output_filename = f"OtEneLabs_Rapor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
        filepath = os.path.join(self.output_dir, output_filename)
        doc = SimpleDocTemplate(filepath, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
        
        elements = []
        
        # Format the numbers
        area_m2 = session_data.get('harvested_area_m2', 0.0)
        area_donum = area_m2 / 1000.0
        
        timestamp = session_data.get('timestamp', datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
        try:
            # Try to format timestamp if it's ISO
            dt = datetime.fromisoformat(timestamp)
            timestamp_str = dt.strftime('%d.%m.%Y %H:%M:%S')
        except:
            timestamp_str = timestamp
            
        # Başlık
        elements.append(Paragraph("Agrovision AI - Parsel Durum Raporu", self.styles['OtEneTitle']))
        elements.append(Paragraph(f"Olusturulma Tarihi: {timestamp_str}", self.styles['OtEneSub']))
        
        # Parsel Bilgileri
        elements.append(Paragraph("Parsel Bilgileri", self.styles['OtEneHeading']))
        elements.append(Paragraph(f"Parsel No: {session_data.get('parsel_no', '51-113-25-2')}", self.styles['OtEneNormal']))
        elements.append(Paragraph(f"Ada / Parsel: {session_data.get('ada_parsel', '25/2')}", self.styles['OtEneNormal']))
        elements.append(Paragraph(f"Alan: {area_m2:,.0f} m2 ({area_donum:.1f} donum)".replace(',', '.'), self.styles['OtEneNormal']))
        elements.append(Paragraph(f"Malik: {session_data.get('owner', 'Mehmet Yilmaz')}", self.styles['OtEneNormal']))
        lat = session_data.get('gps', {}).get('lat', 37.968)
        lon = session_data.get('gps', {}).get('lon', 34.673)
        elements.append(Paragraph(f"Konum: Koordinat ({lat:.3f}, {lon:.3f})", self.styles['OtEneNormal']))
        
        # CKS Kayit Bilgileri
        elements.append(Paragraph("CKS Kayit Bilgileri", self.styles['OtEneHeading']))
        elements.append(Paragraph(f"Kayitli Urun: {session_data.get('declared_crop', 'Bilinmiyor').title()}", self.styles['OtEneNormal']))
        elements.append(Paragraph(f"Hasat Tarihi: {session_data.get('harvest_date', datetime.now().strftime('%Y-%m-%d'))}", self.styles['OtEneNormal']))
        elements.append(Paragraph(f"Ciftci: {session_data.get('owner', 'Mehmet Yilmaz')}", self.styles['OtEneNormal']))
        
        # Telemetri & Hasat Sonuclari
        elements.append(Paragraph("Telemetri & Hasat Sonuclari", self.styles['OtEneHeading']))
        elements.append(Paragraph(f"Ortalama Hiz: {session_data.get('avg_speed', 6.5)} km/s", self.styles['OtEneNormal']))
        elements.append(Paragraph(f"Tahmini Verim: {session_data.get('estimated_yield', 450)} kg/dekar", self.styles['OtEneNormal']))
        elements.append(Paragraph(f"Ortalama Urun Nemi: %{session_data.get('avg_moisture', 12.5)}", self.styles['OtEneNormal']))
        elements.append(Paragraph(f"Hava Sicakligi: {session_data.get('avg_temp', 32)} C", self.styles['OtEneNormal']))
        
        # Status styling
        status = session_data.get('cks_audit_status', 'Bilinmiyor').upper()
        if 'UYGUN' in status and 'UYUMSUZ' not in status:
            status_text = "UYGUN"
        elif 'UYUMSUZ' in status:
            status_text = "UYUMSUZ"
        else:
            status_text = status
            
        elements.append(Paragraph(f"Durum: {status_text}", self.styles['OtEneNormal']))
        elements.append(Paragraph("Son Kontrol: Guncel", self.styles['OtEneNormal']))
        
        # Footer
        elements.append(Paragraph("Bu rapor Agrovision AI Parsel Takip Sistemi tarafindan otomatik olarak olusturulmustur.", self.styles['OtEneFooter']))
        
        # Build PDF
        doc.build(elements)
        return filepath
