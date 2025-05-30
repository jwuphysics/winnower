# The Winnower - Development and CI/CD commands

.PHONY: help install install-dev test test-unit test-integration test-smoke lint format clean

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install the package"
	@echo "  install-dev  - Install with development dependencies"
	@echo "  test         - Run all tests"
	@echo "  test-unit    - Run unit tests only"
	@echo "  test-integration - Run integration tests only"
	@echo "  test-smoke   - Run smoke tests only (good for CI health checks)"
	@echo "  lint         - Run code linting"
	@echo "  format       - Format code with black"
	@echo "  clean        - Clean build artifacts"

# Installation
install:
	uv pip install -e .

install-dev:
	uv pip install -e .[dev,test]

# Testing
test:
	pytest

test-unit:
	pytest tests/test_config.py tests/test_parsers.py tests/test_cli.py -v

test-integration:
	pytest tests/test_integration.py -v

test-smoke:
	pytest tests/test_smoke.py -v

# Code quality
lint:
	flake8 winnower/ tests/
	mypy winnower/

format:
	black winnower/ tests/

# Cleanup
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete