import json
import datetime

def update_rubric():
    with open('research_rubric.json', 'r') as f:
        data = json.load(f)
    
    # Check if phase 6 exists
    for phase in data['phases']:
        if phase['id'] == 'phase_6':
            print("Phase 6 already exists!")
            return
            
    new_items = [
        {
            "id": "item_026",
            "description": "Implement Authentic Tensor Network Contraction for Clique Constraints",
            "acceptance_criteria": "Code module that strictly maps the K_5 inclusion-exclusion conditions to a 2D tensor network, and implements an approximate contraction algorithm (e.g., TRG or DMRG analog) to evaluate the partition function of K_5-free graphs on N vertices without simple sieving.",
            "status": "pending",
            "error": None,
            "notes": None
        },
        {
            "id": "item_027",
            "description": "Develop GFlowNet Pipeline for Thermodynamic Flow Graph Generation",
            "acceptance_criteria": "A fully functional GFlowNet training module where the reward landscape is defined by the tensor network partition function, dynamically generating and sampling large graph candidates (N=42,43) through sequential thermodynamic state transitions.",
            "status": "pending",
            "error": None,
            "notes": None
        },
        {
            "id": "item_028",
            "description": "Extract Novel Graph Invariants from Tensor Spectra",
            "acceptance_criteria": "Analysis script computing the leading eigenvalues of the transfer matrix from the tensor contraction, producing a mathematical proof-of-concept that maps these spectral gaps to a genuinely new upper bound on the maximum density of K_5-free graphs.",
            "status": "pending",
            "error": None,
            "notes": None
        },
        {
            "id": "item_029",
            "description": "Populate Concept Trees with Genuine Experimental Data",
            "acceptance_criteria": "All concept.json files in results/concept_evolve/tree/ updated to include robust experimental_result fields containing actual numerical validation, convergence logs, and data from the new tensor network and GFlowNet executions, replacing prior boilerplate.",
            "status": "pending",
            "error": None,
            "notes": None
        },
        {
            "id": "item_030",
            "description": "Regenerate Professional Publication-Quality Visualizations",
            "acceptance_criteria": "All figures in figures/ recreated using professional libraries (e.g., Seaborn) demonstrating high-quality typography, clear color-blind-friendly palettes, and intricate, polished visualization of the tensor contraction flow and thermodynamic state spaces.",
            "status": "pending",
            "error": None,
            "notes": None
        },
        {
            "id": "item_031",
            "description": "Integrate Novel Findings into the Manuscript",
            "acceptance_criteria": "Update research_paper.tex and corresponding bibliography with the verified experimental data, concrete tensor contraction algorithms, and improved figures, ensuring all claims of cross-domain methodology are strictly backed by the newly executed non-trivial code.",
            "status": "pending",
            "error": None,
            "notes": None
        }
    ]
    
    new_phase = {
        "id": "phase_6",
        "name": "Novelty Deepening",
        "order": 6,
        "items": new_items
    }
    
    data['phases'].append(new_phase)
    
    # Update summary
    data['summary']['total_items'] += len(new_items)
    data['summary']['pending'] += len(new_items)
    data['updated_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    with open('research_rubric.json', 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    update_rubric()
