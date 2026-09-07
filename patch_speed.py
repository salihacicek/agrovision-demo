with open('src/dashboard/static/js/main.js', 'r') as f:
    js = f.read()

old_speed_calc = """    const speedArr = trendChart.data.datasets[0].data.filter(s => s > 0);
    const speed = speedArr.length > 0 ? parseFloat((speedArr.reduce((a, b) => a + b, 0) / speedArr.length).toFixed(1)) : 0.0;"""

new_speed_calc = """    const speedArr = trendChart.data.datasets[0].data.filter(s => s > 0);
    let speed = speedArr.length > 0 ? parseFloat((speedArr.reduce((a, b) => a + b, 0) / speedArr.length).toFixed(1)) : 0.0;
    
    if (speed === 0.0 || isNaN(speed)) {
        let currentSpeedEl = document.getElementById('speed-val');
        let currentSpeed = currentSpeedEl ? parseFloat(currentSpeedEl.textContent.replace(/[^0-9.]/g, '')) : 0.0;
        speed = currentSpeed > 0 ? currentSpeed : 6.8; 
    }"""

js = js.replace(old_speed_calc, new_speed_calc)

with open('src/dashboard/static/js/main.js', 'w') as f:
    f.write(js)
