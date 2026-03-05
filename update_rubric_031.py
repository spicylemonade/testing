import json

with open('research_rubric.json', 'r') as f:
    data = json.load(f)

for phase in data['phases']:
    for item in phase['items']:
        if item['id'] == 'item_031':
            item['status'] = 'completed'
            item['notes'] = 'Successfully integrated novel findings, MPO transfer eigenvalues, and GFlowNet graphs into research_paper.tex. Compiled to PDF with added citations for TRG and GFlowNet.'

data['summary']['completed'] += 1
data['summary']['pending'] -= 1

with open('research_rubric.json', 'w') as f:
    json.dump(data, f, indent=2)
