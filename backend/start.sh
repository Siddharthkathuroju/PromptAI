#!/bin/bash

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | xargs)
fi

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver 0.0.0.0:8000
