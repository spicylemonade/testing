import json

with open('research_rubric.json', 'r') as f:
    data = json.load(f)

for phase in data['phases']:
    for item in phase['items']:
        if item['id'] == 'item_030':
            item['status'] = 'completed'
            item['notes'] = 'All figures in figures/ successfully recreated using Seaborn and Matplotlib in publication quality (PDF/PNG format), accurately visualizing the TRG tensor contraction, MPO spectral gap, and GFlowNet training.'

data['summary']['completed'] += 1
data['summary']['pending'] -= 1

with open('research_rubric.json', 'w') as f:
    json.dump(data, f, indent=2)
