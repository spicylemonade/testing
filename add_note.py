import json

with open('research_rubric.json', 'r') as f:
    data = json.load(f)

data['agent_status']['writer']['notes'] = "Drafted publication-quality research_paper.tex, generated supporting figures using matplotlib, and successfully compiled to PDF with bibtex references without errors."

with open('research_rubric.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Added notes to research_rubric.json")
