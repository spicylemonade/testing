.PHONY: all install test benchmarks figures clean

all: install test benchmarks figures
	@echo "Full pipeline complete. See REPORT.md for results."

install:
	pip install -r requirements.txt

test:
	python -m pytest tests/ -v

benchmarks: results/synthetic_results.csv results/realworld_results.csv results/scalability_results.csv results/comparison.csv

results/synthetic_results.csv:
	python src/run_synthetic_benchmarks.py

results/realworld_results.csv:
	python src/run_realworld_benchmarks.py

results/scalability_results.csv:
	python src/run_scalability.py

results/comparison.csv: results/synthetic_results.csv results/realworld_results.csv
	python src/generate_comparison.py

figures: results/synthetic_results.csv results/realworld_results.csv results/scalability_results.csv
	python src/plot_results.py

clean:
	rm -rf results/*.csv figures/*.png figures/*.pdf __pycache__ .pytest_cache
	find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
