import re

with open('src/dashboard/templates/index.html', 'r') as f:
    html = f.read()

# Replace the dark taupe background with darker cream
html = html.replace('background: #4a4036 !important; /* Soft earthy dark taupe */', 'background: #E5D9C5 !important; /* Darker premium cream/beige */')

# Bump CSS cache
html = html.replace('style.css?v=55', 'style.css?v=56')

with open('src/dashboard/templates/index.html', 'w') as f:
    f.write(html)
