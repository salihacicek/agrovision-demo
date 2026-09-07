import re

with open('src/dashboard/templates/index.html', 'r') as f:
    html = f.read()

# 1. Update landing page backgrounds
html = html.replace('''body .landing-page-classic {
    width: 100% !important;
    height: 100% !important;
    overflow-y: auto !important;
    background: #FAF6ED !important;
}''', '''body .landing-page-classic {
    width: 100% !important;
    height: 100% !important;
    overflow-y: auto !important;
    background: #E5D9C5 !important;
}''')

html = html.replace('''body .features-section {
    padding: 3rem 2rem 5rem 2rem !important;
    background: #FAF6ED !important;''', '''body .features-section {
    padding: 3rem 2rem 5rem 2rem !important;
    background: transparent !important;''')

# 2. Unify the Fleet KPI cards
old_kpi_html = '''                        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5rem;">
                            <div style="background: #FAF6ED; padding: 1.5rem; border-radius: 12px; border: 1px solid #e2e8f0; border-left: 4px solid #78350f; /* Koyu kahve */ box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);">
                                <div style="color: #64748b; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.5rem;">Toplam Araç</div>
                                <div style="font-size: 1.875rem; font-weight: 700; color: #0f172a;">5</div>
                            </div>
                            <div style="background: #FAF6ED; padding: 1.5rem; border-radius: 12px; border: 1px solid #e2e8f0; border-left: 4px solid #166534; /* Orman yeşili */ box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);">
                                <div style="color: #64748b; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.5rem;">Aktif Hasatta</div>
                                <div style="font-size: 1.875rem; font-weight: 700; color: #0f172a;">3</div>
                            </div>
                            <div style="background: #FAF6ED; padding: 1.5rem; border-radius: 12px; border: 1px solid #e2e8f0; border-left: 4px solid #ca8a04; /* Buğday sarısı */ box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);">
                                <div style="color: #64748b; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.5rem;">Beklemede / Yolda</div>
                                <div style="font-size: 1.875rem; font-weight: 700; color: #0f172a;">1</div>
                            </div>
                            <div style="background: #FAF6ED; padding: 1.5rem; border-radius: 12px; border: 1px solid #e2e8f0; border-left: 4px solid #991b1b; /* Koyu kırmızı */ box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);">
                                <div style="color: #64748b; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.5rem;">Bakımda</div>
                                <div style="font-size: 1.875rem; font-weight: 700; color: #0f172a;">1</div>
                            </div>
                        </div>'''

new_kpi_html = '''                        <div style="display: flex; background: #FAF6ED; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); overflow: hidden;">
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
                        </div>'''

html = html.replace(old_kpi_html, new_kpi_html)

# Bump CSS cache
html = html.replace('style.css?v=56', 'style.css?v=57')

with open('src/dashboard/templates/index.html', 'w') as f:
    f.write(html)
