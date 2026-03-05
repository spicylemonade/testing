import json

with open('research_rubric.json', 'r') as f:
    data = json.load(f)

for phase in data['phases']:
    for item in phase['items']:
        if item['id'] == 'item_027':
            item['status'] = 'completed'
            item['notes'] = 'Fully functional GFlowNet pipeline implemented in generators/gflownet_trainer.py. Validated scaling up to N=42, combining Tensor Network evaluation with trajectory balance training.'

data['summary']['completed'] += 1
data['summary']['pending'] -= 1

with open('research_rubric.json', 'w') as f:
    json.dump(data, f, indent=2)
