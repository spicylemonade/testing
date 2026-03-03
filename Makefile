# GCD Algorithm Research — Build System
# Requires: GCC 12+ with C++20 support, x86-64 with BMI2 (TZCNT, SHRX)

CXX = g++
CXXFLAGS = -O3 -march=native -std=c++20 -Wall -Wextra
LDFLAGS =

# Output directories
BUILDDIR = build
RESULTSDIR = results

.PHONY: all clean test benchmark full_benchmark raw_benchmark figures analysis help

all: test benchmark full_benchmark raw_benchmark

help:
	@echo "GCD Algorithm Research — Available Targets"
	@echo ""
	@echo "  make all              Build all executables"
	@echo "  make test             Build and run correctness tests"
	@echo "  make benchmark        Build initial benchmark"
	@echo "  make full_benchmark   Build and run full comparative benchmark (CSV output)"
	@echo "  make raw_benchmark    Build and run raw per-trial benchmark (for statistics)"
	@echo "  make figures          Generate publication-quality figures (requires Python)"
	@echo "  make analysis         Run statistical analysis (requires Python)"
	@echo "  make reproduce        Run full reproduction pipeline (test + bench + stats + figs)"
	@echo "  make clean            Remove build artifacts"
	@echo ""
	@echo "Prerequisites:"
	@echo "  - GCC 12+ with C++20 support"
	@echo "  - x86-64 CPU with BMI2 (for TZCNT/SHRX)"
	@echo "  - Python 3 with matplotlib, seaborn, scipy, pandas, numpy (for figures/stats)"

$(BUILDDIR):
	mkdir -p $(BUILDDIR)

# === Correctness Tests ===
$(BUILDDIR)/test_correctness: src/baselines/test_correctness.cpp src/baselines/gcd_baselines.h | $(BUILDDIR)
	$(CXX) $(CXXFLAGS) -o $@ $<

$(BUILDDIR)/test_novel: src/novel/test_novel.cpp src/novel/*.h src/baselines/gcd_baselines.h | $(BUILDDIR)
	$(CXX) $(CXXFLAGS) -o $@ $<

test: $(BUILDDIR)/test_correctness $(BUILDDIR)/test_novel
	@echo "=== Running baseline correctness tests ==="
	$(BUILDDIR)/test_correctness
	@echo ""
	@echo "=== Running novel algorithm tests ==="
	@echo "(Note: branchless_fixed, branchless_loop, and divstep_v2 are expected to fail — they are documented negative results)"
	-$(BUILDDIR)/test_novel
	@echo ""
	@echo "Baseline tests passed. Novel algorithm results reported above."

# === Benchmarks ===
$(BUILDDIR)/benchmark: src/bench/benchmark.cpp src/baselines/gcd_baselines.h | $(BUILDDIR)
	$(CXX) $(CXXFLAGS) -o $@ $<

$(BUILDDIR)/full_benchmark: src/bench/full_benchmark.cpp src/baselines/gcd_baselines.h src/novel/*.h | $(BUILDDIR)
	$(CXX) $(CXXFLAGS) -o $@ $<

$(BUILDDIR)/raw_benchmark: src/bench/raw_benchmark.cpp src/baselines/gcd_baselines.h src/novel/*.h | $(BUILDDIR)
	$(CXX) $(CXXFLAGS) -o $@ $<

benchmark: $(BUILDDIR)/benchmark

full_benchmark: $(BUILDDIR)/full_benchmark
	@mkdir -p $(RESULTSDIR)/phase4
	$(BUILDDIR)/full_benchmark > $(RESULTSDIR)/phase4/full_benchmarks.csv
	@echo "Results written to $(RESULTSDIR)/phase4/full_benchmarks.csv"

raw_benchmark: $(BUILDDIR)/raw_benchmark
	@mkdir -p $(RESULTSDIR)/phase4
	$(BUILDDIR)/raw_benchmark > $(RESULTSDIR)/phase4/raw_trials.csv
	@echo "Raw trial data written to $(RESULTSDIR)/phase4/raw_trials.csv"

# === Analysis & Figures (Python) ===
analysis: $(RESULTSDIR)/phase4/raw_trials.csv
	python3 scripts/statistical_analysis.py
	@echo "Statistical analysis written to $(RESULTSDIR)/phase4/statistical_analysis.md"

figures: $(RESULTSDIR)/phase4/full_benchmarks.csv $(RESULTSDIR)/phase4/raw_trials.csv
	python3 scripts/generate_figures.py
	@echo "Figures written to figures/"

# === Full Reproduction Pipeline ===
reproduce: test full_benchmark raw_benchmark analysis figures
	@echo ""
	@echo "=== Full reproduction complete ==="
	@echo "Results: $(RESULTSDIR)/phase4/"
	@echo "Figures: figures/"

# === Assembly Analysis ===
$(BUILDDIR)/asm_analysis: src/baselines/asm_analysis.cpp src/baselines/gcd_baselines.h | $(BUILDDIR)
	$(CXX) $(CXXFLAGS) -S -o $(BUILDDIR)/asm_analysis.s $<
	$(CXX) $(CXXFLAGS) -o $@ $<

# === Cross-Platform Builds ===
$(BUILDDIR)/bench_skylake: src/bench/full_benchmark.cpp src/baselines/gcd_baselines.h src/novel/*.h | $(BUILDDIR)
	$(CXX) -O3 -march=skylake -std=c++20 -o $@ $<

$(BUILDDIR)/bench_zen2: src/bench/full_benchmark.cpp src/baselines/gcd_baselines.h src/novel/*.h | $(BUILDDIR)
	$(CXX) -O3 -march=znver2 -std=c++20 -o $@ $<

cross_platform: $(BUILDDIR)/bench_skylake $(BUILDDIR)/bench_zen2
	@mkdir -p $(RESULTSDIR)/phase4
	$(BUILDDIR)/bench_skylake > $(RESULTSDIR)/phase4/benchmarks_skylake.csv
	$(BUILDDIR)/bench_zen2 > $(RESULTSDIR)/phase4/benchmarks_zen2.csv
	@echo "Cross-platform results written to $(RESULTSDIR)/phase4/"

clean:
	rm -rf $(BUILDDIR)
	rm -f bench_skylake bench_zen2 raw_benchmark
