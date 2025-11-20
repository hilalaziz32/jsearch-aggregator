#!/bin/bash

# Job Search Application Rebuild Script
# This script rebuilds the containers and restarts them with the latest build

set -e  # Exit on any error

echo "🔨 Rebuilding Job Search Application..."

# Build the containers
echo "📦 Building containers..."
docker compose build

# Stop and remove existing containers
echo "🛑 Stopping and removing existing containers..."
docker compose down

# Start containers in detached mode
echo "🚀 Starting containers with latest build..."
docker compose up -d

# Check if services are running
echo "🔍 Checking service status..."
docker compose ps

echo "✅ Rebuild complete! Application is running on http://localhost:5555"
echo "📝 Logs: docker compose logs -f"
echo "🛑 Stop: docker compose down"
