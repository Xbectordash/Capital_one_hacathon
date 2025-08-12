# 🌾 FarmMate - Docker Deployment Guide

## 🏗️ Three-Tier Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Web     │───▶│  Express.js     │───▶│   Python AI     │
│   Frontend      │    │   Gateway       │    │    Server       │
│   (Port 3000)   │    │  (Port 5000)    │    │  (Port 8000)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
     Socket.IO             Socket.IO ↔           WebSocket
     Client                WebSocket             FastAPI
                           Client
```

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed and running
- Ports 3000, 5000, 8000 available

### Option 1: PowerShell (Windows)
```powershell
.\start-farmmate.ps1
```

### Option 2: Bash (Linux/Mac/WSL)
```bash
chmod +x start-farmmate.sh
./start-farmmate.sh
```

### Option 3: Manual Docker Compose
```bash
# Build and start all services
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

## 🐳 Services Overview

| Service | Container Name | Port | Description |
|---------|---------------|------|-------------|
| **React Frontend** | `farmmate-react-frontend` | 3000 | Web UI with Socket.IO client |
| **Express Gateway** | `farmmate-express-gateway` | 5000 | API gateway with Socket.IO server |
| **Python AI Server** | `farmmate-ai-server` | 8000 | FastAPI + WebSocket AI processing |
| **ChromaDB** | `farmmate-chromadb` | 8001 | Vector database (optional) |

## 🔗 Service URLs

- **🌐 Frontend**: http://localhost:3000
- **🔗 Express API**: http://localhost:5000
- **🤖 Python AI**: http://localhost:8000
- **📚 API Docs**: http://localhost:8000/docs
- **💾 ChromaDB**: http://localhost:8001

## 🔄 Communication Flow

1. **User** → React Frontend (Socket.IO client)
2. **React** → Express Gateway (Socket.IO connection)
3. **Express** → Python AI Server (WebSocket client)
4. **Python AI** → Agricultural processing & response
5. **Response** flows back through the chain

## 🛠️ Development Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f farmmate-ai-server
docker-compose logs -f farmmate-express-gateway
docker-compose logs -f farmmate-react-frontend
```

### Restart Services
```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart farmmate-ai-server
```

### Rebuild Services
```bash
# Rebuild all
docker-compose up --build -d

# Rebuild specific service
docker-compose up --build -d farmmate-ai-server
```

### Health Checks
```bash
# Python AI Server
curl http://localhost:8000/health

# Express Gateway
curl http://localhost:5000/health

# React Frontend
curl http://localhost:3000
```

## 🔧 Environment Variables

### Python AI Server
- `PYTHONDONTWRITEBYTECODE=1`
- `PYTHONUNBUFFERED=1`
- `PORT=8000`

### Express Gateway
- `NODE_ENV=production`
- `PORT=5000`
- `PYTHON_SERVER_URL=ws://agent-python:8000`

### React Frontend
- `REACT_APP_BACKEND_URL=http://localhost:5000`
- `REACT_APP_SOCKET_URL=http://localhost:5000`

## 🐛 Troubleshooting

### Service Won't Start
```bash
# Check logs for errors
docker-compose logs [service-name]

# Restart problematic service
docker-compose restart [service-name]
```

### Port Conflicts
```bash
# Check what's using the ports
netstat -ano | findstr :3000
netstat -ano | findstr :5000
netstat -ano | findstr :8000
```

### Network Issues
```bash
# Recreate network
docker-compose down
docker network prune
docker-compose up --build -d
```

### Clean Reset
```bash
# Remove all containers and rebuild
docker-compose down --volumes --remove-orphans
docker system prune -f
docker-compose up --build -d
```

## 📊 Monitoring

### Container Status
```bash
docker-compose ps
```

### Resource Usage
```bash
docker stats
```

### Network Info
```bash
docker network ls
docker network inspect capital_one_hacathon_farmmate-network
```

## 🎯 Testing the Flow

1. **Start all services**: `docker-compose up --build -d`
2. **Open Frontend**: http://localhost:3000
3. **Test AI chat**: Send agricultural queries
4. **Check logs**: `docker-compose logs -f` 
5. **Verify responses**: Should see data flow through all three tiers

## 📱 Flutter Mobile App (Currently Disabled)

The Flutter mobile app build is commented out in `docker-compose.yml`. To enable:

1. Uncomment the `frontend-android` service
2. Run: `docker-compose up --build -d frontend-android`
3. APK will be built in the container

## 🔒 Security Notes

- All services run as non-root users
- Health checks monitor service availability  
- Network isolation between services
- Production-ready Dockerfile configurations

## 🚧 Future Enhancements

- [ ] Add Redis for session management
- [ ] Implement service mesh with Istio
- [ ] Add monitoring with Prometheus/Grafana
- [ ] SSL/TLS certificates for HTTPS
- [ ] Auto-scaling with Kubernetes
