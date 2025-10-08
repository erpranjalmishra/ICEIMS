#!/bin/bash

# Exit on error
set -e

echo "Starting deployment script..."

# Install dependencies
echo "Installing Python dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Deployment script completed successfully!"
