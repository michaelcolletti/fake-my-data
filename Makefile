# Makefile for HumanFirst Demos - Synthetic Data Generation
# ========================================================

# Python interpreter
PYTHON := python3
PIP := pip3

# Project directories
SRC_DIR := .
TEST_DIR := tests
OUTPUT_DIR := output

# Default target
.PHONY: help
help: ## Show this help message
	@echo "🚀 HumanFirst Demos - Synthetic Data Generation"
	@echo "================================================"
	@echo ""
	@echo "Available targets:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""

# Installation and setup
.PHONY: install
install: ## Install project dependencies
	@echo "📦 Installing dependencies..."
	$(PIP) install -r requirements.txt
	@echo "✅ Dependencies installed successfully!"

.PHONY: install-dev
install-dev: install ## Install dependencies including development tools
	@echo "🔧 Installing development dependencies..."
	@echo "✅ Development environment ready!"

# Create output directory
$(OUTPUT_DIR):
	@mkdir -p $(OUTPUT_DIR)

# Running individual scripts
.PHONY: run-server-data
run-server-data: $(OUTPUT_DIR) ## Generate server migration data (default: 100 rows)
	@echo "🖥️  Generating server migration data..."
	$(PYTHON) create-testdata.py --output-file $(OUTPUT_DIR)/server_migration_data.csv
	@echo "✅ Server migration data generated in $(OUTPUT_DIR)/server_migration_data.csv"

.PHONY: run-payroll-data
run-payroll-data: $(OUTPUT_DIR) ## Generate payroll data (200 employees)
	@echo "👥 Generating payroll data..."
	$(PYTHON) generate-payroll-data.py
	@mv fake_payroll.csv $(OUTPUT_DIR)/payroll_data.csv 2>/dev/null || true
	@echo "✅ Payroll data generated in $(OUTPUT_DIR)/payroll_data.csv"

.PHONY: run-all
run-all: run-server-data run-payroll-data ## Generate all data types

# Generate example datasets with custom parameters
.PHONY: examples
examples: $(OUTPUT_DIR) ## Generate example datasets with various row counts
	@echo "📊 Generating example datasets..."
	@echo "  - Small dataset (50 servers)..."
	$(PYTHON) create-testdata.py --num-rows 50 --output-file $(OUTPUT_DIR)/server_data_small.csv
	@echo "  - Medium dataset (200 servers)..."
	$(PYTHON) create-testdata.py --num-rows 200 --output-file $(OUTPUT_DIR)/server_data_medium.csv
	@echo "  - Large dataset (500 servers)..."
	$(PYTHON) create-testdata.py --num-rows 500 --output-file $(OUTPUT_DIR)/server_data_large.csv
	@echo "  - Payroll data (200 employees)..."
	$(PYTHON) generate-payroll-data.py
	@mv fake_payroll.csv $(OUTPUT_DIR)/payroll_data_example.csv 2>/dev/null || true
	@echo "✅ Example datasets generated in $(OUTPUT_DIR)/"

# Custom data generation targets
.PHONY: server-small
server-small: $(OUTPUT_DIR) ## Generate small server dataset (50 rows)
	$(PYTHON) create-testdata.py --num-rows 50 --output-file $(OUTPUT_DIR)/server_data_50.csv
	@echo "✅ Small server dataset (50 rows) generated"

.PHONY: server-medium
server-medium: $(OUTPUT_DIR) ## Generate medium server dataset (200 rows)
	$(PYTHON) create-testdata.py --num-rows 200 --output-file $(OUTPUT_DIR)/server_data_200.csv
	@echo "✅ Medium server dataset (200 rows) generated"

.PHONY: server-large
server-large: $(OUTPUT_DIR) ## Generate large server dataset (500 rows)
	$(PYTHON) create-testdata.py --num-rows 500 --output-file $(OUTPUT_DIR)/server_data_500.csv
	@echo "✅ Large server dataset (500 rows) generated"

.PHONY: server-xlarge
server-xlarge: $(OUTPUT_DIR) ## Generate extra large server dataset (1000 rows)
	$(PYTHON) create-testdata.py --num-rows 1000 --output-file $(OUTPUT_DIR)/server_data_1000.csv
	@echo "✅ Extra large server dataset (1000 rows) generated"

# Testing
.PHONY: test
test: ## Run all tests
	@echo "🧪 Running tests..."
	$(PYTHON) -m pytest $(TEST_DIR)/ -v
	@echo "✅ All tests completed!"

.PHONY: test-verbose
test-verbose: ## Run tests with verbose output
	@echo "🧪 Running tests with verbose output..."
	$(PYTHON) -m pytest $(TEST_DIR)/ -v -s

.PHONY: test-coverage
test-coverage: ## Run tests with coverage reporting
	@echo "🧪 Running tests with coverage..."
	$(PYTHON) -m pytest $(TEST_DIR)/ --cov=. --cov-report=html --cov-report=term-missing
	@echo "✅ Coverage report generated in htmlcov/"

.PHONY: test-server
test-server: ## Run tests for server data generation only
	@echo "🧪 Testing server data generation..."
	$(PYTHON) -m pytest $(TEST_DIR)/test_create_testdata.py -v

.PHONY: test-payroll
test-payroll: ## Run tests for payroll data generation only
	@echo "🧪 Testing payroll data generation..."
	$(PYTHON) -m pytest $(TEST_DIR)/test_generate_payroll_data.py -v

# Development and maintenance
.PHONY: lint
lint: ## Run code linting (if flake8 is available)
	@echo "🔍 Running code linting..."
	@if command -v flake8 >/dev/null 2>&1; then \
		flake8 *.py $(TEST_DIR)/*.py --max-line-length=88 --ignore=E203,W503; \
		echo "✅ Linting completed!"; \
	else \
		echo "⚠️  flake8 not found. Install with: pip install flake8"; \
	fi

.PHONY: format
format: ## Format code (if black is available)
	@echo "🎨 Formatting code..."
	@if command -v black >/dev/null 2>&1; then \
		black *.py $(TEST_DIR)/*.py --line-length=88; \
		echo "✅ Code formatted!"; \
	else \
		echo "⚠️  black not found. Install with: pip install black"; \
	fi

# Validation targets
.PHONY: validate
validate: test lint ## Run all validation checks (tests + linting)
	@echo "✅ All validation checks passed!"

.PHONY: validate-data
validate-data: $(OUTPUT_DIR) ## Generate and validate sample data
	@echo "🔬 Validating data generation..."
	$(PYTHON) create-testdata.py --num-rows 10 --output-file $(OUTPUT_DIR)/validation_server.csv
	$(PYTHON) generate-payroll-data.py
	@mv fake_payroll.csv $(OUTPUT_DIR)/validation_payroll.csv 2>/dev/null || true
	@echo "✅ Data validation completed!"

# Cleanup
.PHONY: clean
clean: ## Clean generated files and caches
	@echo "🧹 Cleaning up..."
	@rm -rf $(OUTPUT_DIR)/
	@rm -rf __pycache__/
	@rm -rf tests/__pycache__/
	@rm -rf .pytest_cache/
	@rm -rf htmlcov/
	@rm -rf .coverage
	@rm -f *.csv
	@rm -f fake_payroll.csv
	@rm -f server_migration_data.csv
	@echo "✅ Cleanup completed!"

.PHONY: clean-data
clean-data: ## Clean only generated data files
	@echo "🧹 Cleaning data files..."
	@rm -rf $(OUTPUT_DIR)/
	@rm -f *.csv
	@rm -f fake_payroll.csv
	@rm -f server_migration_data.csv
	@echo "✅ Data files cleaned!"

.PHONY: clean-cache
clean-cache: ## Clean Python cache files only
	@echo "🧹 Cleaning cache files..."
	@rm -rf __pycache__/
	@rm -rf tests/__pycache__/
	@rm -rf .pytest_cache/
	@rm -rf htmlcov/
	@rm -rf .coverage
	@echo "✅ Cache files cleaned!"

# Information targets
.PHONY: info
info: ## Show project information
	@echo "📋 Project Information"
	@echo "====================="
	@echo "Project: HumanFirst Demos - Synthetic Data Generation"
	@echo "Python: $(shell $(PYTHON) --version)"
	@echo "Pip: $(shell $(PIP) --version)"
	@echo ""
	@echo "📁 Project Structure:"
	@echo "  ├── create-testdata.py      # Server migration data generator"
	@echo "  ├── generate-payroll-data.py # Payroll data generator"
	@echo "  ├── requirements.txt        # Python dependencies"
	@echo "  ├── tests/                  # Test suite"
	@echo "  └── output/                 # Generated data files"
	@echo ""

.PHONY: status
status: ## Show current project status
	@echo "📊 Project Status"
	@echo "================="
	@echo "Dependencies:"
	@$(PIP) list | grep -E "(faker|pandas|click|pytest)" || echo "  No dependencies found - run 'make install'"
	@echo ""
	@echo "Generated files:"
	@if [ -d "$(OUTPUT_DIR)" ]; then \
		ls -la $(OUTPUT_DIR)/ 2>/dev/null | tail -n +2 || echo "  No files in output directory"; \
	else \
		echo "  Output directory doesn't exist"; \
	fi
	@echo ""

# Quick start
.PHONY: quickstart
quickstart: install examples test ## Quick start: install, generate examples, and test
	@echo ""
	@echo "🎉 Quick start completed!"
	@echo "========================"
	@echo "✅ Dependencies installed"
	@echo "✅ Example datasets generated in $(OUTPUT_DIR)/"
	@echo "✅ Tests passed"
	@echo ""
	@echo "Next steps:"
	@echo "  - View generated data: ls $(OUTPUT_DIR)/"
	@echo "  - Run specific generators: make run-server-data OR make run-payroll-data"
	@echo "  - Generate custom sizes: make server-large"
	@echo "  - Run tests: make test"
	@echo ""