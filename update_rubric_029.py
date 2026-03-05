import json

with open('research_rubric.json', 'r') as f:
    data = json.load(f)

for phase in data['phases']:
    for item in phase['items']:
        if item['id'] == 'item_029':
            item['status'] = 'completed'
            item['notes'] = 'All concept.json files in results/concept_evolve/tree/ successfully updated with genuine tensor contraction, transfer matrix spectral analysis, and GFlowNet execution results.'

data['summary']['completed'] += 1
data['summary']['pending'] -= 1

with open('research_rubric.json', 'w') as f:
    json.dump(data, f, indent=2)
