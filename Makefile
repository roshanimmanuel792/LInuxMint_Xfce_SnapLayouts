.PHONY: help build install dev-install test lint clean

help:
	@echo "xfce-snap-layouts - Build targets:"
	@echo "  make dev-install   - Install in development mode"
	@echo "  make build         - Build distribution packages"
	@echo "  make install       - Install system-wide"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Run linters"
	@echo "  make clean         - Clean build artifacts"
	@echo "  make run           - Run the application"

dev-install:
	python3 -m pip install -e .
	python3 -m pip install -r requirements.txt

build: clean
	python3 setup.py sdist bdist_wheel

install: build
	sudo python3 -m pip install dist/xfce-snap-layouts-1.0.0-py3-none-any.whl

test:
	python3 -m pytest tests/ -v --tb=short

lint:
	python3 -m pylint xfce_snap_layouts/ --disable=missing-docstring

clean:
	rm -rf build/ dist/ *.egg-info __pycache__ .pytest_cache .coverage htmlcov

run: dev-install
	xfce-snap-layouts

.PHONY: help build install dev-install test lint clean run
