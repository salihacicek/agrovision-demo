import re

with open('src/reporting/pdf_report.py', 'r') as f:
    content = f.read()

old_block = """        # Format the numbers
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
        elements.append(Paragraph(f"Hava Sicakligi: {session_data.get('avg_temp', 32)} C", self.styles['OtEneNormal']))"""

new_block = """        # Format the numbers
        total_area_m2 = float(session_data.get('total_area_m2', 0.0))
        total_area_donum = total_area_m2 / 1000.0
        
        harvested_area_m2 = float(session_data.get('harvested_area_m2', 0.0))
        harvested_area_donum = harvested_area_m2 / 1000.0
        
        completion_pct = float(session_data.get('completion_pct', 0.0))
        
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
        elements.append(Paragraph(f"Parsel No: {session_data.get('parsel_no', '-')}", self.styles['OtEneNormal']))
        elements.append(Paragraph(f"Ada / Parsel: {session_data.get('ada_parsel', '-')}", self.styles['OtEneNormal']))
        elements.append(Paragraph(f"Toplam Alan: {total_area_m2:,.0f} m2 ({total_area_donum:.1f} donum)".replace(',', '.'), self.styles['OtEneNormal']))
        elements.append(Paragraph(f"Malik: {session_data.get('owner', '-')}", self.styles['OtEneNormal']))
        lat = session_data.get('gps', {}).get('lat', 37.968)
        lon = session_data.get('gps', {}).get('lon', 34.673)
        elements.append(Paragraph(f"Konum: Koordinat ({lat:.3f}, {lon:.3f})", self.styles['OtEneNormal']))
        
        # CKS Kayit Bilgileri
        elements.append(Paragraph("CKS Kayit Bilgileri", self.styles['OtEneHeading']))
        elements.append(Paragraph(f"Kayitli Urun: {session_data.get('declared_crop', 'Bilinmiyor').title()}", self.styles['OtEneNormal']))
        elements.append(Paragraph(f"Hasat Tarihi: {session_data.get('harvest_date', datetime.now().strftime('%Y-%m-%d'))}", self.styles['OtEneNormal']))
        elements.append(Paragraph(f"Ciftci: {session_data.get('owner', '-')}", self.styles['OtEneNormal']))
        
        # Telemetri & Hasat Sonuclari
        elements.append(Paragraph("Telemetri & Hasat Sonuclari", self.styles['OtEneHeading']))
        elements.append(Paragraph(f"Bicilen Alan: {harvested_area_m2:,.0f} m2 ({harvested_area_donum:.1f} donum)", self.styles['OtEneNormal']))
        elements.append(Paragraph(f"Tamamlanma Orani: %{completion_pct:.1f}", self.styles['OtEneNormal']))
        elements.append(Paragraph(f"Ortalama Hiz: {session_data.get('avg_speed', 0.0)} km/s", self.styles['OtEneNormal']))
        elements.append(Paragraph(f"Tahmini Verim: {session_data.get('estimated_yield', 0.0):.0f} kg/dekar", self.styles['OtEneNormal']))
        elements.append(Paragraph(f"Ortalama Urun Nemi: %{session_data.get('avg_moisture', 0.0)}", self.styles['OtEneNormal']))
        elements.append(Paragraph(f"Hava Sicakligi: {session_data.get('avg_temp', 0.0)} C", self.styles['OtEneNormal']))"""

content = content.replace(old_block, new_block)

with open('src/reporting/pdf_report.py', 'w') as f:
    f.write(content)
