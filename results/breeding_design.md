# TM Breeding Design

## Decomposition Scheme

Each TM transition table is decomposed into functional modules:
- **Counter modules**: States that read/write different symbols (binary counter behavior)
- **Sweep modules**: States that always write the same symbol and move in the same direction
- **Mixed modules**: States with heterogeneous behavior

## Recombination Strategies

1. **Row swap**: Exchange all transitions for a given state between parents
2. **Column swap**: Exchange all transitions for a given symbol
3. **Block crossover**: Split the transition table at a random point

## Results

- Parents: 4
- Offspring: 125
- Halting: 62
- Best sigma: 66
- Strategy breakdown: {'row_swap': 32, 'column_swap': 8, 'block_crossover': 22}
