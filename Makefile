.PHONY: help install dev-install test lint format build clean run-hello run-status

# Default target
help:
	@echo "T3 CLI Development Commands"
	@echo "=========================="
	@echo ""
	@echo "Setup Commands:"
	@echo "  install      Install dependencies with uv"
	@echo "  dev-install  Install in development mode"
	@echo ""
	@echo "Development Commands:"
	@echo "  test         Run tests with pytest"
	@echo "  lint         Run linting with ruff"
	@echo "  format       Format code with ruff"
	@echo "  build        Build package"
	@echo "  clean        Clean build artifacts"
	@echo ""
	@echo "CLI Commands:"
	@echo "  run-hello    Run hello command"
	@echo "  run-status   Run status command"
	@echo ""
	@echo "Example Usage:"
	@echo "  make install"
	@echo "  make test"
	@echo "  make run-hello"

# Setup commands
install:
	@echo "📦 Installing dependencies..."
	uv sync

dev-install: install
	@echo "🔧 Installing in development mode..."
	uv pip install -e .

# Development commands
test:
	@echo "🧪 Running tests..."
	pytest -v

test-cov:
	@echo "🧪 Running tests with coverage..."
	pytest --cov=t3 --cov-report=term-missing --cov-report=html

lint:
	@echo "🔍 Running linter..."
	ruff check .

lint-fix:
	@echo "🔧 Running linter with auto-fix..."
	ruff check . --fix

format:
	@echo "✨ Formatting code..."
	ruff format .

build:
	@echo "📦 Building package..."
	python -m build

clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/

# CLI test commands
run-hello:
	@echo "👋 Running hello command..."
	python -m t3.main hello --name "Developer"

run-status:
	@echo "📊 Running status command..."
	python -m t3.main status

run-version:
	@echo "📋 Showing version..."
	python -m t3.main --version

# Development workflow
check: lint test
	@echo "✅ All checks passed!"

dev: install lint format test
	@echo "🚀 Development environment ready!"

# Quick project initialization test
test-init:
	@echo "🧪 Testing project initialization..."
	@mkdir -p /tmp/t3-test
	@cd /tmp/t3-test && python -m t3.main init project --name "test-project" --template python --force
	@echo "✅ Test project created at /tmp/t3-test/test-project"