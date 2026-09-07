with open('src/dashboard/templates/index.html', 'r') as f:
    html = f.read()
html = html.replace('>Niğde<', '>Ankara<')
with open('src/dashboard/templates/index.html', 'w') as f:
    f.write(html)

with open('src/dashboard/static/js/main.js', 'r') as f:
    js = f.read()
js = js.replace("51-113-25-", "06-113-25-")
js = js.replace("TR-51-", "TR-06-")
with open('src/dashboard/static/js/main.js', 'w') as f:
    f.write(js)
