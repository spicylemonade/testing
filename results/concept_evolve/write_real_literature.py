import json
import os
import glob

real_papers = [
    {
        "title": "A new upper bound on the Ramsey number R(5, 5)",
        "authors": ["B. McKay", "S. Radziszowski"],
        "year": 1992,
        "abstract": "We establish a new upper bound for the classical Ramsey number R(5,5).",
        "url": "https://www.semanticscholar.org/paper/160081e3e1f57e3478499da04264f84564db90f2"
    },
    {
        "title": "R(5,5) <= 46",
        "authors": ["Vigleik Angeltveit", "Brendan D. McKay"],
        "year": 2024,
        "abstract": "We prove that the Ramsey number R(5,5) is less than or equal to 46. The proof uses a combination of linear programming and checking a large number of cases by computer.",
        "url": "https://arxiv.org/abs/2409.15709"
    },
    {
        "title": "Statistical Mechanics of Semantic Compression",
        "authors": ["Tankut Can"],
        "year": 2025,
        "abstract": "We map the optimization problem of determining the minimal-length, meaning-preserving message to a spin glass Hamiltonian and solve the resulting statistical mechanics problem using replica theory.",
        "url": "https://arxiv.org/abs/2503.00612"
    },
    {
        "title": "Spin Glass Theory and the Statistical Mechanics of Language Models",
        "authors": ["Eliza Kosloff"],
        "year": None,
        "abstract": "An overview of how spin glass theory and statistical mechanics connect to large neural models and optimization over discrete sequences.",
        "url": "https://www.semanticscholar.org/paper/746106e47a83a82758c3291d6caee2f48b80740c"
    },
    {
        "title": "An exact value for the Ramsey number R(K5, K5 - e)",
        "authors": ["Vigleik Angeltveit"],
        "year": 2026,
        "abstract": "We compute the exact value of the Ramsey number R(K5, K5-e). It is equal to 30.",
        "url": "https://arxiv.org/abs/2602.11459"
    }
]

tree_dir = "/home/archivara/work/repo/results/concept_evolve/tree"
for folder in os.listdir(tree_dir):
    path = os.path.join(tree_dir, folder, "literature.json")
    if os.path.exists(path):
        with open(path, "w") as f:
            json.dump(real_papers, f, indent=2)

print("Updated literature.json with real papers.")
