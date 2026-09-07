import re

with open('src/reporting/pdf_report.py', 'r') as f:
    code = f.read()

sanitize_func = """
def sanitize_turkish(text: str) -> str:
    if not isinstance(text, str):
        return str(text)
    replacements = {
        'ı': 'i', 'I': 'I',
        'İ': 'I', 'i': 'i',
        'ş': 's', 'Ş': 'S',
        'ğ': 'g', 'Ğ': 'G',
        'ü': 'u', 'Ü': 'U',
        'ö': 'o', 'Ö': 'O',
        'ç': 'c', 'Ç': 'C'
    }
    for s, r in replacements.items():
        text = text.replace(s, r)
    return text

class PDFReportGenerator:"""

code = code.replace("class PDFReportGenerator:", sanitize_func)

# We need to sanitize the dynamic fields:
# session_data.get('owner', '-')
# session_data.get('declared_crop', 'Bilinmiyor').title()
# session_data.get('parsel_no', '-')
# session_data.get('ada_parsel', '-')
# We can just sanitize the result of .get() or override session_data values at the beginning.

override_block = """
        # Sanitize all string values in session_data to avoid ReportLab font rendering issues with Turkish chars
        for key in session_data:
            if isinstance(session_data[key], str):
                session_data[key] = sanitize_turkish(session_data[key])
                
        # Format the numbers"""

code = code.replace("# Format the numbers", override_block)

with open('src/reporting/pdf_report.py', 'w') as f:
    f.write(code)
