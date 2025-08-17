# 🚀 FarmMate App को Start करने के तरीके

## ⚡ **सबसे आसान - Enhanced Setup (Monitoring के साथ):**

```powershell
# Enhanced setup with monitoring dashboard
./scripts/start-farmmate-enhanced.ps1
```

**Access URLs:**
- 🌐 **Main App**: http://localhost:3000
- 🔍 **Monitoring Dashboard**: http://localhost:9000  
- 🤖 **AI API**: http://localhost:8000
- 📊 **Grafana**: http://localhost:3001

---

## 🐳 **Docker Enhanced Setup:**

```powershell
# Complete Docker setup with monitoring
docker-compose -f docker-compose.enhanced.yml up -d

# Check status
docker ps

# Stop all services
docker-compose -f docker-compose.enhanced.yml down
```

---

## 🏃‍♂️ **Quick Development Setup:**

```powershell
# Simple development setup
./scripts/start-farmmate.ps1
```

**Access URLs:**
- 🌐 **Frontend**: http://localhost:3000
- 🤖 **Backend**: http://localhost:5000
- 🧠 **AI Server**: http://localhost:8000

---

## 🔧 **Manual Start (Development):**

### 1. Start AI Server:
```powershell
cd agent-python
python src/start_server.py
# Runs on: http://localhost:8000
```

### 2. Start Express Backend:
```powershell
cd backend
npm start
# Runs on: http://localhost:5000
```

### 3. Start React Frontend:
```powershell
cd frontend/web/agricultural-chat-app
npm start
# Runs on: http://localhost:3000
```

---

## ⚙️ **Troubleshooting Commands:**

### Check what's running:
```powershell
# Check ports
netstat -ano | findstr "3000 5000 8000 9000"

# Check Docker containers
docker ps -a

# Check logs
docker logs farmmate-monitoring
docker logs farmmate-ai-server
```

### Stop everything:
```powershell
# Stop Docker
docker-compose down
docker-compose -f docker-compose.enhanced.yml down

# Kill processes on specific ports
taskkill /F /PID (Get-NetTCPConnection -LocalPort 3000).OwningProcess
taskkill /F /PID (Get-NetTCPConnection -LocalPort 5000).OwningProcess
taskkill /F /PID (Get-NetTCPConnection -LocalPort 8000).OwningProcess
```

---

## 🎯 **Recommended: Enhanced Setup**

**सबसे अच्छा तरीका है Enhanced setup जो monitoring भी देता है:**

```powershell
./scripts/start-farmmate-enhanced.ps1
```

फिर browser में जाएं:
- **http://localhost:3000** - Main App
- **http://localhost:9000** - Monitoring Dashboard

---

## 📱 **Quick Status Check:**

```powershell
# Check if services are running
curl http://localhost:8000/health     # AI Server
curl http://localhost:5000/api/health # Backend  
curl http://localhost:9000/health     # Monitoring
```

बस ये commands run करें और आपका app ready हो जाएगा! 🚀
