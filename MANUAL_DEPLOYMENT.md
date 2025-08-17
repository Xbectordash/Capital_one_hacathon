# 🚀 Manual Deployment Guide (Recommended)

## Step-by-Step Manual Deployment

Since render.yaml automatic detection might not work, here's the manual approach:

### Step 1: Deploy Python AI Server First

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New"** → **"Web Service"**
3. Connect repository: `Xbectordash/Capital_one_hacathon`
4. Configure as follows:

```
Name: farmmate-ai-server
Branch: main (or agent-python)
Root Directory: agent-python
Environment: Production
Language: Docker
Region: Oregon (US West)
Instance Type: Starter ($7/month) or Free

Docker Settings:
- Dockerfile Path: agent-python/Dockerfile
- Docker Build Context: agent-python
- Health Check Path: /health
```

5. Add Environment Variables:
```
PYTHONDONTWRITEBYTECODE=1
PYTHONUNBUFFERED=1
NODE_ENV=production
PORT=8000
GEMINI_API_KEY=your_actual_key
WEATHER_API=your_actual_key
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your_actual_key
AGMARKNET_API_KEY=your_actual_key
```

6. Click **"Create Web Service"**
7. Wait for deployment (5-10 minutes)
8. Note the URL: `https://farmmate-ai-server.onrender.com`

### Step 2: Deploy Express Backend Second

1. Click **"New"** → **"Web Service"** again
2. Same repository: `Xbectordash/Capital_one_hacathon`
3. Configure as follows:

```
Name: farmmate-backend
Branch: main (or agent-python)
Root Directory: backend
Environment: Production
Language: Docker
Region: Oregon (US West)
Instance Type: Starter ($7/month) or Free

Docker Settings:
- Dockerfile Path: backend/Dockerfile
- Docker Build Context: backend
- Health Check Path: /health
```

4. Add Environment Variables:
```
NODE_ENV=production
PORT=5000
PYTHON_SERVER_URL=wss://farmmate-ai-server.onrender.com
FRONTEND_URL=https://farmmate-frontend.onrender.com
```

5. Click **"Create Web Service"**
6. Wait for deployment
7. Note the URL: `https://farmmate-backend.onrender.com`

### Step 3: Deploy React Frontend Last (Optional)

1. Click **"New"** → **"Static Site"**
2. Same repository: `Xbectordash/Capital_one_hacathon`
3. Configure as follows:

```
Name: farmmate-frontend
Branch: main (or agent-python)
Root Directory: frontend/web/agricultural-chat-app
Build Command: npm install && npm run build
Publish Directory: build
```

4. Add Environment Variables:
```
REACT_APP_BACKEND_URL=https://farmmate-backend.onrender.com
REACT_APP_SOCKET_URL=https://farmmate-backend.onrender.com
```

## ✅ Testing After Deployment

### Test Python Server:
```bash
curl https://farmmate-ai-server.onrender.com/health
curl https://farmmate-ai-server.onrender.com/docs
```

### Test Express Backend:
```bash
curl https://farmmate-backend.onrender.com/health
```

### Test Socket Connection:
Open browser console and run:
```javascript
const socket = io('https://farmmate-backend.onrender.com');
socket.on('connect', () => console.log('Connected!'));
socket.emit('user_query', {query: 'Hello', language: 'en'});
socket.on('ai_response', (data) => console.log('Response:', data));
```

## 🎯 Priority Order

For your hackathon, I recommend:

1. **First**: Deploy Python AI Server only
2. **Test**: Make sure it works properly
3. **Second**: Deploy Express Backend if needed
4. **Last**: Deploy Frontend if time permits

## 💡 Quick Start (Minimal)

Just deploy the **Python AI Server** first. You can test it directly:
- API Docs: `https://farmmate-ai-server.onrender.com/docs`
- WebSocket: `wss://farmmate-ai-server.onrender.com/ws/test123`
- Test Page: `https://farmmate-ai-server.onrender.com/test-page`

This gives you a working AI backend that can be accessed directly!
