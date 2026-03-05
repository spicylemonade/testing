import sys
import os
import networkx as nx
import numpy as np
from itertools import combinations

# Add the parent directory to the path so we can import generators
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generators.twisted_algebraic import TwistedAlgebraicGenerator

def count_k5_cliques(G):
    # Find all maximal cliques in the graph
    cliques = list(nx.find_cliques(G))
    # Collect all unique K5s
    k5_sets = set()
    for clique in cliques:
        if len(clique) >= 5:
            for k5 in combinations(sorted(clique), 5):
                k5_sets.add(k5)
    return len(k5_sets)

def max_clique_size(G):
    cliques = list(nx.find_cliques(G))
    if not cliques: return 0
    return max(len(c) for c in cliques)

def evaluate_candidate(A):
    G = nx.from_numpy_array(A)
    # Complement graph
    A_comp = 1 - A
    np.fill_diagonal(A_comp, 0)
    G_comp = nx.from_numpy_array(A_comp)

    max_clique = max_clique_size(G)
    max_clique_comp = max_clique_size(G_comp)
    
    k5_G = count_k5_cliques(G)
    k5_comp = count_k5_cliques(G_comp)

    density = nx.density(G)

    return {
        'max_clique_G': max_clique,
        'max_clique_comp': max_clique_comp,
        'k5_G': k5_G,
        'k5_comp': k5_comp,
        'density': density
    }

def main():
    generator = TwistedAlgebraicGenerator(N=43)
    
    best_candidate = None
    best_score = float('inf')
    best_twists = -1
    best_stats = None

    # Search for the best candidate by varying the number of twists
    # Using 100 twists is sufficient to find a good representative without taking too long
    for num_twists in range(100):
        A = generator.generate_candidate(num_twists=num_twists)
        stats = evaluate_candidate(A)
        
        # A good candidate should minimize the total number of K_5s in G and G_comp
        score = stats['k5_G'] + stats['k5_comp']
        
        if score < best_score:
            best_score = score
            best_candidate = A
            best_twists = num_twists
            best_stats = stats
            
        if num_twists % 10 == 0:
            print(f"Twists: {num_twists:3d} | Max Clique G: {stats['max_clique_G']} | Max Clique G_comp: {stats['max_clique_comp']} | K5s: {stats['k5_G']} + {stats['k5_comp']} = {score}")

    print("\nBest Candidate found:")
    print(f"Number of twists: {best_twists}")
    print(f"Max Clique G: {best_stats['max_clique_G']}")
    print(f"Max Clique G_comp: {best_stats['max_clique_comp']}")
    print(f"Total K5s: {best_score}")
    print(f"Density: {best_stats['density']:.4f}")

    # Write evaluation results
    with open('experiments/candidate_evaluation.md', 'w') as f:
        f.write("# Candidate Evaluation: Twisted Algebraic Generator (N=43)\n\n")
        f.write("## Overview\n")
        f.write("We evaluated the `TwistedAlgebraicGenerator(N=43)` to search for $K_5$-free configurations in both the graph and its complement, potentially serving as counterexamples to the Ramsey number $R(5,5) \\le 43$ bound.\n\n")
        
        f.write("## Methodology\n")
        f.write("The generator creates a base cyclotomic graph and applies structural 'twists' (edge flips along algebraic sub-orbits) to disrupt highly symmetric cliques. We iterated through different numbers of twists (from 0 to 99) to find the candidate that minimizes the total number of $K_5$ subgraphs in the graph ($G$) and its complement ($\\overline{G}$).\n\n")
        f.write("NetworkX was used to construct the graph from the adjacency matrix, compute the maximum clique size, and explicitly count the unique occurrences of $K_5$ cliques by generating combinations from the maximal cliques found by NetworkX.\n\n")
        
        f.write("## Results for the Best Candidate\n")
        f.write(f"- **Number of Twists:** {best_twists}\n")
        f.write(f"- **Max Clique Size in $G$:** {best_stats['max_clique_G']}\n")
        f.write(f"- **Max Clique Size in $\\overline{{G}}$:** {best_stats['max_clique_comp']}\n")
        f.write(f"- **Total $K_5$ Cliques in $G$:** {best_stats['k5_G']}\n")
        f.write(f"- **Total $K_5$ Cliques in $\\overline{{G}}$:** {best_stats['k5_comp']}\n")
        f.write(f"- **Total $K_5$ structures overall:** {best_score}\n")
        f.write(f"- **Graph Density:** {best_stats['density']:.4f}\n\n")
        
        f.write("## Analysis\n")
        if best_score == 0:
            f.write("The evaluated graph contains zero $K_5$ cliques in both $G$ and $\\overline{G}$, successfully finding a counterexample to $R(5,5) \\le 43$.\n")
        else:
            f.write("The evaluated graph is not $K_5$-free in both $G$ and $\\overline{G}$. ")
            f.write("Although the twisted algebraic construction disrupts many symmetric cliques, the structural density and the applied twists were insufficient to completely eliminate all $K_5$ subgraphs. ")
            f.write(f"The best configuration still contains {best_score} total $K_5$ structures. ")
            f.write("Thus, it does not stand as a valid $K_5$-free construction for $N=43$.\n\n")
            f.write("Further optimizations of the generator, such as modifying the base subgroup, the specific orbits twisted, or integrating a local search algorithm (like simulated annealing) to resolve the remaining $K_5$ cliques, are necessary to find a true counterexample (if one exists).\n")

if __name__ == '__main__':
    main()
