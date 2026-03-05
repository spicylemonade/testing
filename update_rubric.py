import json
import sys
from datetime import datetime

def update_rubric(item_id, status, notes=None, error=None):
    with open('research_rubric.json', 'r') as f:
        data = json.load(f)
    
    for phase in data['phases']:
        for item in phase['items']:
            if item['id'] == item_id:
                item['status'] = status
                if notes:
                    item['notes'] = notes
                if error:
                    item['error'] = error
                break
    
    # update summary
    summary = {"total_items": 0, "completed": 0, "in_progress": 0, "failed": 0, "pending": 0}
    for phase in data['phases']:
        for item in phase['items']:
            summary["total_items"] += 1
            summary[item['status']] += 1
            
    data['summary'] = summary
    
    if data['agent_status'][data['current_agent']]['status'] != 'in_progress':
        data['agent_status'][data['current_agent']]['status'] = 'in_progress'

    data['updated_at'] = datetime.utcnow().isoformat() + "Z"
    
    with open('research_rubric.json', 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    item_id = sys.argv[1]
    status = sys.argv[2]
    notes = sys.argv[3] if len(sys.argv) > 3 else None
    error = sys.argv[4] if len(sys.argv) > 4 else None
    update_rubric(item_id, status, notes, error)
