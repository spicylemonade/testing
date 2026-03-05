import json
import matplotlib.pyplot as plt
import os

os.makedirs('figures', exist_ok=True)

# Plot 1: Baseline metrics
with open('experiments/baseline_results.json', 'r') as f:
    baseline = json.load(f)

Ns = [v['N'] for v in baseline.values()]
thetas = [v['spectral_metrics']['theta_G_bound'] for v in baseline.values()]

plt.figure(figsize=(6, 4))
plt.plot(Ns, thetas, 'bo-', label='Lovasz theta bound')
plt.axhline(y=4.99, color='r', linestyle='--', label='Theoretical Viability Limit')
plt.xlabel('Graph Size N')
plt.ylabel('Spectral Bound')
plt.title('Baseline Lovasz theta for Paley Graphs')
plt.legend()
plt.grid(True)
plt.savefig('figures/baseline_spectral.png', dpi=300, bbox_inches='tight')
plt.close()

# Plot 2: Generator metrics
with open('experiments/generator_logs.json', 'r') as f:
    gen_logs = json.load(f)

Ns_gen = [42, 43, 44]
densities = [gen_logs[f'algebraic_N{n}']['density'] for n in Ns_gen]
max_bounds = [gen_logs[f'algebraic_N{n}']['max_spectral_bound'] for n in Ns_gen]

fig, ax1 = plt.subplots(figsize=(6, 4))

color = 'tab:blue'
ax1.set_xlabel('Graph Size N')
ax1.set_ylabel('Edge Density', color=color)
ax1.plot(Ns_gen, densities, 'bs-', label='Density')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Max Spectral Bound', color=color)
ax2.plot(Ns_gen, max_bounds, 'r^-', label='Spectral Bound')
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
plt.title('Twisted Algebraic Candidates Metrics')
plt.grid(True)
plt.savefig('figures/generator_metrics.png', dpi=300, bbox_inches='tight')
plt.close()

# Plot 3: Tensor counts
spins = [gen_logs[f'tensor_N{n}']['num_spins'] for n in Ns_gen]
tensors = [gen_logs[f'tensor_N{n}']['num_tensors'] for n in Ns_gen]

plt.figure(figsize=(6, 4))
plt.plot(Ns_gen, spins, 'go-', label='Physical Spins (Edges)')
plt.plot(Ns_gen, [t/1000 for t in tensors], 'ms-', label='Constraint Tensors (x 10^3)')
plt.xlabel('Graph Size N')
plt.ylabel('Count')
plt.yscale('log')
plt.title('Tensor Network Complexity Scaling')
plt.legend()
plt.grid(True)
plt.savefig('figures/tensor_complexity.png', dpi=300, bbox_inches='tight')
plt.close()
print("Figures generated.")
