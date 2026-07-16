#!/bin/bash
set -e

echo "=== Deploying kaylas.cloud Phase 1 backend ==="

cd /root/kaylas-cloud

# Pull latest backend from local copy
# (In production, this would be git pull)

# Create env file if missing
if [ ! -f .env ]; then
    cp backend/.env.example .env
    echo "Created .env from example. Please edit /root/kaylas-cloud/.env with real secrets."
fi

# Build and start the backend + postgres + ollama
docker compose up -d postgres ollama api

# Wait for postgres
echo "Waiting for postgres..."
sleep 5

# Seed the database
docker exec kaylas-api python app/seed.py || echo "Seed failed - may need to wait for postgres"

echo "=== Phase 1 backend deployed ==="
echo "Check status: docker compose ps"
echo "API docs: https://kaylas.cloud/docs"
