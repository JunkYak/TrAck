#!/bin/bash
set -e

echo "Starting trAck deployment sequence..."

echo "Running Alembic migrations..."
python -m alembic upgrade head

echo "Seeding global food catalog..."
python scripts/seed_global_foods.py

echo "Booting FastAPI Application..."
# Azure App Service sets the PORT environment variable natively.
# We default to 8000 if not provided.
PORT=${PORT:-8000}

# Start uvicorn. Note: For a high-concurrency production environment, 
# you should eventually install gunicorn and replace this line with:
# gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
