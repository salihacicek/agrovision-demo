import re

with open('src/dashboard/app.py', 'r') as f:
    content = f.read()

# 1. Add ReportRequest
req_class = """class ReportRequest(BaseModel):
    avg_speed: float = 0.0

@app.post("/generate_report")
async def generate_report_endpoint(req: ReportRequest):"""

content = content.replace('@app.post("/generate_report")\nasync def generate_report_endpoint():', req_class)

# 2. Update avg_speed logic
old_speed = "'avg_speed': round(getattr(state, 'last_speed', 0.0), 1),"
new_speed = "'avg_speed': req.avg_speed if req.avg_speed > 0 else round(getattr(state, 'last_speed', 0.0), 1),"

content = content.replace(old_speed, new_speed)

with open('src/dashboard/app.py', 'w') as f:
    f.write(content)
