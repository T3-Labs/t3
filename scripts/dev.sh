#!/usr/bin/env bash
# Development helper script

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Help message
show_help() {
    cat << EOF
T3 CLI Development Helper

Usage: $0 <command>

Commands:
    setup       Initial project setup (install dependencies)
    test        Run tests with pytest
    coverage    Run tests with coverage report
    lint        Run Ruff linter
    format      Format code with Ruff
    check       Run all checks (format, lint, test)
    install     Install CLI in editable mode
    build       Build distribution packages
    clean       Remove build artifacts and cache
    help        Show this help message

Examples:
    $0 setup        # First time setup
    $0 check        # Before committing
    $0 build        # Create distribution packages
EOF
}

# Setup
setup() {
    print_info "Installing dependencies..."
    uv sync
    print_success "Dependencies installed"
    
    print_info "Installing CLI in editable mode..."
    uv pip install -e .
    print_success "CLI installed"
    
    print_info "Verifying installation..."
    t3 --version
    print_success "Setup complete!"
}

# Run tests
run_tests() {
    print_info "Running tests..."
    uv run pytest tests/ -v
    print_success "Tests passed!"
}

# Run tests with coverage
run_coverage() {
    print_info "Running tests with coverage..."
    uv run pytest tests/ --cov=t3 --cov-report=term-missing --cov-report=html
    print_success "Coverage report generated in htmlcov/"
}

# Lint
run_lint() {
    print_info "Running Ruff linter..."
    uv run ruff check t3/ tests/
    print_success "Linting passed!"
}

# Format
run_format() {
    print_info "Formatting code with Ruff..."
    uv run ruff format t3/ tests/
    uv run ruff check --fix t3/ tests/
    print_success "Code formatted!"
}

# Check all
check_all() {
    print_info "Running all checks..."
    echo ""
    
    print_info "1/3 - Formatting check"
    uv run ruff format --check t3/ tests/
    print_success "Format check passed"
    echo ""
    
    print_info "2/3 - Linting"
    uv run ruff check t3/ tests/
    print_success "Linting passed"
    echo ""
    
    print_info "3/3 - Tests"
    uv run pytest tests/ -v
    print_success "Tests passed"
    echo ""
    
    print_success "All checks passed! ✨"
}

# Install CLI
install_cli() {
    print_info "Installing CLI in editable mode..."
    uv pip install -e .
    print_success "CLI installed"
    
    print_info "Verifying installation..."
    t3 --version
    t3 --help
}

# Build
build_package() {
    print_info "Building distribution packages..."
    uv build
    print_success "Packages built in dist/"
    
    print_info "Validating package..."
    uv run twine check dist/*
    print_success "Package validation passed!"
}

# Clean
clean_artifacts() {
    print_info "Removing build artifacts..."
    rm -rf build/ dist/ *.egg-info .pytest_cache/ .coverage htmlcov/
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    print_success "Clean complete!"
}

# Main
case "${1:-help}" in
    setup)
        setup
        ;;
    test)
        run_tests
        ;;
    coverage)
        run_coverage
        ;;
    lint)
        run_lint
        ;;
    format)
        run_format
        ;;
    check)
        check_all
        ;;
    install)
        install_cli
        ;;
    build)
        build_package
        ;;
    clean)
        clean_artifacts
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
