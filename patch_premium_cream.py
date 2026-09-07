import re

with open('src/dashboard/templates/index.html', 'r') as f:
    html = f.read()

# 1. Fix the accidental global background I set to #292524
html = html.replace('background: #292524 !important; /* Koyu antrasit/kahve */ /* Çok uçuk toprak/krem rengi */', 'background: #FAF6ED !important; /* Premium elite cream */')
# There might be another instance from earlier patches:
html = html.replace('background: #f8fafc !important; /* Mesh gradienti iptal et */', 'background: #FAF6ED !important; /* Premium elite cream */')

# 2. Change all major white backgrounds to cream
html = html.replace('background: #ffffff !important;', 'background: #FAF6ED !important;')

# 3. For cards that have inline style="background: white;"
html = html.replace('background: white;', 'background: #FAF6ED;')

# 4. Make sure icon wrappers (which were #292524) are still dark!
# Wait, did I change #ffffff !important to #FAF6ED !important? Yes.
# Did I accidentally change the feature-card icon background?
# It was `background: #292524 !important; /* Koyu antrasit/kahve */` 
# I didn't replace that one because I targeted the specific line with "Çok uçuk toprak/krem rengi".
# Let's verify.

with open('src/dashboard/templates/index.html', 'w') as f:
    f.write(html)
