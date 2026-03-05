import json
from datetime import datetime, timezone

with open('research_rubric.json', 'r') as f:
    data = json.load(f)

now = datetime.now(timezone.utc).isoformat()
data['agent_status']['writer']['status'] = 'completed'
data['agent_status']['writer']['completed_at'] = now
data['current_agent'] = 'reviewer'
data['agent_status']['reviewer']['status'] = 'in_progress'
data['agent_status']['reviewer']['started_at'] = now

with open('research_rubric.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Updated research_rubric.json")
