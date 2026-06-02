#!/usr/bin/env bash

set -euo pipefail

echo "Starting Docker Compose stack..."
docker compose -f app/docker-compose.yml up --build -d

echo "Services started."
echo "Open: http://localhost:8080"
echo "Health endpoint: http://localhost:8080/health"
