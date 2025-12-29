#!/bin/bash

# ArtCam Pro Startup Script

echo "Setting up ArtCam Pro..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run the application
echo "Starting ArtCam Pro..."
./venv/bin/python3 main.py