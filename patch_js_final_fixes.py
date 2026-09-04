import re

with open('src/dashboard/static/js/main.js', 'r') as f:
    content = f.read()

# 1. Update togglePlay
old_play = """function togglePlay() {
    fetch('/toggle_play', { method: 'POST' })"""
new_play = """function togglePlay() {
    if (!window.currentActiveParcelId) {
        alert("Lütfen önce listeden veya haritadan bir parsel seçip 'Bu Parselde Başla' işlemini yapın!");
        return;
    }
    fetch('/toggle_play', { method: 'POST' })"""
content = content.replace(old_play, new_play)

# 2. Update farmersDb to use real numbers for alan and fix city
old_osman = """    'osman': {
        name: 'Osman Cingitaş', tc: '12345678901', no: '2025-0158', city: 'Niğde',
        parcels: [
            { no: '51-113-25-1', ada: '25/1', alan: '25.000', malik: 'Osman Cingitaş', kayitli: 'Ayçiçeği', tarih: '20.07.2026', mapId: 'P1789' },
            { no: '51-113-25-2', ada: '25/2', alan: '25.000', malik: 'Osman Cingitaş', kayitli: 'Mısır', tarih: '20.07.2026', mapId: 'P1826' },
            { no: '51-113-25-3', ada: '25/3', alan: '25.000', malik: 'Osman Cingitaş', kayitli: 'Mısır', tarih: '20.07.2026', mapId: 'P1959' },
            { no: '51-113-25-4', ada: '25/4', alan: '25.000', malik: 'Osman Cingitaş', kayitli: 'Mısır', tarih: '20.07.2026', mapId: 'P1986' }
        ]
    },"""

new_osman = """    'osman': {
        name: 'Osman Cingitaş', tc: '12345678901', no: '2025-0158', city: 'Ankara',
        parcels: [
            { no: '51-113-25-1', ada: '25/1', alan: 25000, malik: 'Osman Cingitaş', kayitli: 'Ayçiçeği', tarih: '20.07.2026', mapId: 'P1789' },
            { no: '51-113-25-2', ada: '25/2', alan: 25000, malik: 'Osman Cingitaş', kayitli: 'Mısır', tarih: '20.07.2026', mapId: 'P1826' },
            { no: '51-113-25-3', ada: '25/3', alan: 25000, malik: 'Osman Cingitaş', kayitli: 'Mısır', tarih: '20.07.2026', mapId: 'P1959' },
            { no: '51-113-25-4', ada: '25/4', alan: 25000, malik: 'Osman Cingitaş', kayitli: 'Mısır', tarih: '20.07.2026', mapId: 'P1986' }
        ]
    },"""
content = content.replace(old_osman, new_osman)

old_mehmet = """    'mehmet': {
        name: 'Mehmet Yıldız', tc: '98765432109', no: '2025-1105', city: 'Ankara',
        parcels: [
            { no: '06-112-05-1', ada: '5/1', alan: '60.000', malik: 'Mehmet Yıldız', kayitli: 'Mısır', tarih: '01.09.2026', mapId: 'P2017' },
            { no: '06-112-05-2', ada: '5/2', alan: '12.500', malik: 'Mehmet Yıldız', kayitli: 'Arpa', tarih: '01.09.2026', mapId: 'P2044' },
            { no: '06-112-05-3', ada: '5/3', alan: '15.000', malik: 'Mehmet Yıldız', kayitli: 'Buğday', tarih: '01.09.2026', mapId: 'P2074' },
            { no: '06-112-05-4', ada: '5/4', alan: '18.000', malik: 'Mehmet Yıldız', kayitli: 'Mısır', tarih: '01.09.2026', mapId: 'P2093' }
        ]
    }"""

new_mehmet = """    'mehmet': {
        name: 'Mehmet Yıldız', tc: '98765432109', no: '2025-1105', city: 'Ankara',
        parcels: [
            { no: '06-112-05-1', ada: '5/1', alan: 60000, malik: 'Mehmet Yıldız', kayitli: 'Mısır', tarih: '01.09.2026', mapId: 'P2017' },
            { no: '06-112-05-2', ada: '5/2', alan: 12500, malik: 'Mehmet Yıldız', kayitli: 'Arpa', tarih: '01.09.2026', mapId: 'P2044' },
            { no: '06-112-05-3', ada: '5/3', alan: 15000, malik: 'Mehmet Yıldız', kayitli: 'Buğday', tarih: '01.09.2026', mapId: 'P2074' },
            { no: '06-112-05-4', ada: '5/4', alan: 18000, malik: 'Mehmet Yıldız', kayitli: 'Mısır', tarih: '01.09.2026', mapId: 'P2093' }
        ]
    }"""
content = content.replace(old_mehmet, new_mehmet)


with open('src/dashboard/static/js/main.js', 'w') as f:
    f.write(content)
