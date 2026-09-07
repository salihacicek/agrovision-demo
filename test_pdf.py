from src.reporting.pdf_report import PDFReportGenerator
import traceback
try:
    gen = PDFReportGenerator()
    dummy_data = {
        "parsel_no": "P123",
        "ada_parsel": "A123",
        "owner": "Test",
        "declared_crop": "Mısır",
        "total_area_m2": 1000,
        "harvested_area_m2": 500,
        "completion_pct": 50.0,
        "estimated_yield": 800,
        "avg_speed": 5.5,
        "avg_temp": 32.0,
        "avg_moisture": 12.5,
        "lat": 38.0,
        "lon": 34.0
    }
    path = gen.generate_report(dummy_data)
    print("SUCCESS: PDF created at", path)
except Exception as e:
    print("FAILED:", str(e))
    traceback.print_exc()
