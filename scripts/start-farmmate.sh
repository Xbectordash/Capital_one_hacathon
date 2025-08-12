#!/bin/bash
# FarmMate Three-Tier Architecture Startup Script

echo "🌾 Starting FarmMate Agricultural AI System..."
echo "========================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

echo "🔧 Building and starting all services..."

# Build and start all services
docker-compose up --build -d

echo "⏳ Waiting for services to start..."
sleep 10

# Check service health
echo "🔍 Checking service health..."

echo "📊 Python AI Server (port 8000):"
curl -f http://localhost:8000/health || echo "❌ AI Server not ready yet"

echo ""
echo "📊 Express Gateway (port 5000):"
curl -f http://localhost:5000/health || echo "❌ Gateway not ready yet"

echo ""
echo "📊 React Frontend (port 3000):"
curl -f http://localhost:3000 || echo "❌ Frontend not ready yet"

echo ""
echo "✅ Services starting up..."
echo "🌐 Frontend: http://localhost:3000"
echo "🔗 Express API: http://localhost:5000"  
echo "🤖 Python AI: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"

echo ""
echo "📋 To view logs:"
echo "docker-compose logs -f [service-name]"
echo ""
echo "🛑 To stop all services:"
echo "docker-compose down"
