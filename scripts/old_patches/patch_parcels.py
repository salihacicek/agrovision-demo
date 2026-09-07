import json

with open('src/dashboard/static/assets/data/parseller.json', 'r') as f:
    data = json.load(f)

# The mapIds in farmersDb are:
# Osman: P1789, P1826, P1959, P1986
# Mehmet: P2017, P2044, P2074, P2093

# Update features
for feature in data.get('features', []):
    props = feature['properties']
    pid = props.get('parsel_id')
    
    if pid == 'P1789':
        props['malik_adi'] = 'Osman Cingitaş'
        props['urun_tipi'] = 'Ayçiçeği'
        props['alan_donum'] = 25.0
        props['ada_no'] = 25
        props['parsel_no'] = 1
    elif pid == 'P1826':
        props['malik_adi'] = 'Osman Cingitaş'
        props['urun_tipi'] = 'Mısır'
        props['alan_donum'] = 25.0
        props['ada_no'] = 25
        props['parsel_no'] = 2
    elif pid == 'P1959':
        props['malik_adi'] = 'Osman Cingitaş'
        props['urun_tipi'] = 'Mısır'
        props['alan_donum'] = 25.0
        props['ada_no'] = 25
        props['parsel_no'] = 3
    elif pid == 'P1986':
        props['malik_adi'] = 'Osman Cingitaş'
        props['urun_tipi'] = 'Mısır'
        props['alan_donum'] = 25.0
        props['ada_no'] = 25
        props['parsel_no'] = 4
    elif pid == 'P2017':
        props['malik_adi'] = 'Mehmet Yıldız'
        props['urun_tipi'] = 'Mısır'
        props['alan_donum'] = 60.0
        props['ada_no'] = 5
        props['parsel_no'] = 1
    elif pid == 'P2044':
        props['malik_adi'] = 'Mehmet Yıldız'
        props['urun_tipi'] = 'Arpa'
        props['alan_donum'] = 12.5
        props['ada_no'] = 5
        props['parsel_no'] = 2
    elif pid == 'P2074':
        props['malik_adi'] = 'Mehmet Yıldız'
        props['urun_tipi'] = 'Buğday'
        props['alan_donum'] = 15.0
        props['ada_no'] = 5
        props['parsel_no'] = 3
    elif pid == 'P2093':
        props['malik_adi'] = 'Mehmet Yıldız'
        props['urun_tipi'] = 'Mısır'
        props['alan_donum'] = 18.0
        props['ada_no'] = 5
        props['parsel_no'] = 4

with open('src/dashboard/static/assets/data/parseller.json', 'w') as f:
    json.dump(data, f, indent=4)

