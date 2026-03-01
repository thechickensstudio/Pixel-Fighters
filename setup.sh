#!/bin/bash

# Setup script for Smash Fighter game

echo "Setting up Smash Fighter..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment and install dependencies
echo "Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Setup complete!"
echo ""
echo "To run the game:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Run the game: python main.py"
echo "  3. When done, deactivate: deactivate"
echo ""
