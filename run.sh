#!/bin/bash

# Quick run script for Smash Fighter game

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found!"
    echo "Please run setup.sh first: bash setup.sh"
    exit 1
fi

# Activate virtual environment and run game
source venv/bin/activate
python main.py
deactivate
