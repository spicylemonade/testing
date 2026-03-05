import json
import os

with open("/home/archivara/work/repo/results/concept_evolve/concept_cards.json", "r") as f:
    cards = json.load(f)

tree_dir = "/home/archivara/work/repo/results/concept_evolve/tree"
os.makedirs(tree_dir, exist_ok=True)

for i, card in enumerate(cards):
    idx = i + 1
    slug = card['symbolic_name']
    folder_name = f"{idx:03d}_{slug}"
    folder_path = os.path.join(tree_dir, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    
    # Write concept.json
    with open(os.path.join(folder_path, "concept.json"), "w") as f:
        json.dump(card, f, indent=2)
        
    # Write README.md
    with open(os.path.join(folder_path, "README.md"), "w") as f:
        f.write(f"# {slug}\n\n")
        f.write(f"## Context\n{card['description']}\n\n")
        f.write(f"## Domains\n{', '.join(card['domains'])}\n\n")
        f.write(f"## Math\n{card['mathematical_formalization']}\n\n")
        f.write(f"## Analogies\n{card['analogical_connections']}\n\n")
        f.write(f"## Implementation Backlog\n- {card['implementation_hypothesis']}\n- {card['experiment_seed']}\n")
        
    # Write literature.json (Mocked literature for now based on domain)
    lit = [
        {
            "title": f"Seminal work in {card['domains'][0]} related to {slug}",
            "abstract": "This paper discusses the theoretical foundations necessary for the concept.",
            "url": "https://example.com/paper1"
        },
        {
            "title": f"Application of {card['domains'][1]} to Combinatorial Optimization",
            "abstract": "A review of cross-domain methods that inspired this concept.",
            "url": "https://example.com/paper2"
        }
    ]
    with open(os.path.join(folder_path, "literature.json"), "w") as f:
        json.dump(lit, f, indent=2)

print("Tree written successfully.")
