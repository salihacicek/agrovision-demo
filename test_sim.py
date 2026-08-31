import random
sim_state = {
    'lat': 39.7610,
    'lon': 32.4270,
    'direction': 'west',
    'row': 0
}

for i in range(100):
    speed_kmh = 6.0
    step_size = 0.000003 * (speed_kmh / 5.0)
    
    if sim_state['direction'] == 'east':
        sim_state['lon'] += step_size
        if sim_state['lon'] > 32.4270:
            sim_state['direction'] = 'south'
    elif sim_state['direction'] == 'west':
        sim_state['lon'] -= step_size
        if sim_state['lon'] < 32.4252:
            sim_state['direction'] = 'south'
    elif sim_state['direction'] == 'south':
        sim_state['lat'] -= 0.00006
        sim_state['row'] += 1
        if sim_state['row'] % 2 == 1:
            sim_state['direction'] = 'east'
        else:
            sim_state['direction'] = 'west'
            
    if sim_state['lat'] < 39.7600:
        sim_state['lat'] = 39.7610
        sim_state['lon'] = 32.4270
        sim_state['direction'] = 'west'
        sim_state['row'] = 0

    if i % 10 == 0 or sim_state['direction'] == 'south':
        print(f"Step {i}: lat={sim_state['lat']:.6f}, lon={sim_state['lon']:.6f}, dir={sim_state['direction']}, row={sim_state['row']}")
