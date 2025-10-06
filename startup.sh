#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Ensure media directory exists and has proper structure
echo "Setting up media directory..."
mkdir -p media/sponsors
mkdir -p media/committee
mkdir -p media/attractions
mkdir -p media/slider
mkdir -p media/hero/slides
mkdir -p media/site/logos
mkdir -p media/speakers
mkdir -p media/blog/images
mkdir -p media/awards/winners
mkdir -p media/university/gallery

# Set proper permissions for media directory
chmod -R 755 media/ || true

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate --noinput

# Check media files (optional - helps debug)
python manage.py check_media || true

# Start Gunicorn
gunicorn iccca_website.wsgi:application --bind 0.0.0.0:$PORT