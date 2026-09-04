import re

with open('src/dashboard/templates/index.html', 'r') as f:
    content = f.read()

start_marker = '<tbody id="reports-tbody">'
end_marker = '</tbody>'
idx_start = content.find(start_marker)
idx_end = content.find(end_marker, idx_start)

new_tbody = '<tbody id="reports-tbody">\n                                <!-- JS ile dolar -->\n                            '
content = content[:idx_start] + new_tbody + content[idx_end:]

with open('src/dashboard/templates/index.html', 'w') as f:
    f.write(content)
