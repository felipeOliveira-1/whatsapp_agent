#!/bin/bash

# Script to start gunicorn with the correct port from environment
PORT=${PORT:-5000}
echo "Starting gunicorn on port $PORT"
exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 4 --threads 2 --worker-class gthread --timeout 300 --access-logfile - --log-level info