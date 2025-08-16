# 🐳 FarmMate Docker Commands

## Quick Start
```bash
# 1. Check Docker is running
docker version

# 2. Build and start all services
docker-compose up -d --build

# 3. Check status
docker-compose ps
```

## Individual Commands

### Build Services
```bash
# Build all services
docker-compose build

# Build specific service
docker-compose build agent-python
docker-compose build backend
docker-compose build frontend-web
```

### Start/Stop Services
```bash
# Start all services (detached mode)
docker-compose up -d

# Start with logs visible
docker-compose up

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Monitoring
```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs

# View logs for specific service
docker-compose logs agent-python
docker-compose logs backend
docker-compose logs frontend-web

# Follow logs in real-time
docker-compose logs -f
```

### Development
```bash
# Rebuild and restart
docker-compose down && docker-compose up -d --build

# Restart specific service
docker-compose restart agent-python

# Execute command in running container
docker-compose exec agent-python bash
docker-compose exec backend sh
```

## Service URLs (when running)
- 🐍 Python AI Server: http://localhost:8000
- 🚀 Express Backend: http://localhost:5000  
- ⚛️ React Frontend: http://localhost:3000
- 📊 ChromaDB: http://localhost:8001

## Troubleshooting
```bash
# Remove all containers and images
docker-compose down --rmi all

# Clean up Docker system
docker system prune -a

# Check Docker disk usage
docker system df
```
