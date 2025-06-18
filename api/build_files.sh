#!/bin/bash
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Creating static directory..."
mkdir -p static/css static/js

echo "Creating placeholder static files..."
touch static/css/main.css
touch static/js/main.js

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Ensuring staticfiles directory exists..."
mkdir -p staticfiles
touch staticfiles/.keep

echo "Build completed successfully!"
ls -la staticfiles/
