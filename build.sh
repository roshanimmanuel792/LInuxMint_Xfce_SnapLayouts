#!/bin/bash
# xfce-snap-layouts Build and Install Script

set -e

echo "=========================================="
echo "xfce-snap-layouts - Build & Install"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_step() {
    echo -e "${BLUE}>>> $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    print_error "This script only works on Linux"
    exit 1
fi

# Step 1: Install system dependencies
print_step "Installing system dependencies..."

if command -v apt-get &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y \
        python3 python3-dev python3-pip \
        xdotool wmctrl x11-utils \
        libgtk-3-0 libgtk-3-dev \
        gobject-introspection libgirepository1.0-dev
    print_success "System dependencies installed"
else
    print_error "apt-get not found. Please install the required packages manually."
    exit 1
fi

# Step 2: Create virtual environment
print_step "Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_success "Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate

# Step 3: Install Python dependencies
print_step "Installing Python dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
print_success "Python dependencies installed"

# Step 4: Install package in development mode
print_step "Installing package in development mode..."
pip install -e .
print_success "Package installed"

# Step 5: Run validation
print_step "Running validation checks..."
if python3 validate_build.py; then
    print_success "Validation passed!"
else
    print_error "Validation failed. Please check the output above."
    exit 1
fi

echo ""
print_success "Build completed successfully!"
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the application: xfce-snap-layouts &"
echo "3. Trigger the overlay: Press Super+Z"
echo ""
