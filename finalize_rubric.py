import json
import sys
from datetime import datetime

with open('research_rubric.json', 'r') as f:
    data = json.load(f)

data['agent_status'][data['current_agent']]['status'] = 'completed'
data['agent_status'][data['current_agent']]['completed_at'] = datetime.utcnow().isoformat() + "Z"
data['updated_at'] = datetime.utcnow().isoformat() + "Z"

with open('research_rubric.json', 'w') as f:
    json.dump(data, f, indent=2)
