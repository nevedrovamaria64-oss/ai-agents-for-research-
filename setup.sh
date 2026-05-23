#!/bin/bash
# Installation script for Linux/macOS (optional)

echo ""
echo "======================================"
echo "  NEWS AGENT - Setup for Linux/macOS"
echo "======================================"
echo ""

# Check Python
echo "[1] Checking Python..."
python3 --version || (echo "Error: Python3 not found" && exit 1)

# Install pip
echo "[2] Upgrading pip..."
python3 -m pip install --upgrade pip

# Install requirements
echo "[3] Installing dependencies..."
python3 -m pip install -r requirements.txt

# Create directories
echo "[4] Creating directories..."
mkdir -p data logs news_output

echo ""
echo "======================================"
echo "  Installation Complete!"
echo "======================================"
echo ""
echo "Next: python3 main.py"
echo ""
