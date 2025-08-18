# Express Backend Deployment Guide for Render

## 🚀 Quick Deployment Steps for Express Backend

### Prerequisites:
- ✅ Python AI Server already deployed at: `farmmate-ai-server.onrender.com`

### Render Dashboard Configuration:

#### 1. Basic Settings:
```
Name: farmmate-backend
Source: Xbectordash/Capital_one_hacathon
Branch: main (or agent-python)
Environment: Production
Language: Docker
Region: Oregon (US West)
```

#### 2. Docker Configuration:
```
Root Directory: backend
Dockerfile Path: backend/Dockerfile
Docker Build Context Directory: backend
Health Check Path: /health
```

#### 3. Instance Type:
- **Free**: For testing (will sleep after 15 min)
- **Starter ($7/month)**: Recommended for production

#### 4. Environment Variables (Critical!):
```
NODE_ENV=production
PORT=5000
PYTHON_SERVER_URL=wss://farmmate-ai-server.onrender.com
FRONTEND_URL=https://farmmate-frontend.onrender.com
```

### 🔗 Socket Connection Flow:

```
Browser/App (Frontend)
    ↓ Socket.IO Connection
Express Backend (Port 5000)
    ↓ WebSocket Connection  
Python AI Server (Port 8000)
```

### ✅ After Deployment:

Your Express backend will be available at:
- Main URL: `https://farmmate-backend.onrender.com`
- Health Check: `https://farmmate-backend.onrender.com/health`
- Socket.IO: `https://farmmate-backend.onrender.com/socket.io/`

### 🧪 Testing Socket Connection:

1. **Health Check**:
   ```bash
   curl https://farmmate-backend.onrender.com/health
   ```

2. **Socket.IO Connection**:
   Open browser console on any webpage and run:
   ```javascript
   const socket = io('https://farmmate-backend.onrender.com');
   socket.on('connect', () => console.log('Connected to Express Backend'));
   socket.emit('user_query', {query: 'Test message', language: 'en'});
   socket.on('ai_response', (data) => console.log('AI Response:', data));
   ```

### 🔧 Important Notes:

1. **WebSocket Protocol**: 
   - Local: `ws://localhost:8000`
   - Render: `wss://farmmate-ai-server.onrender.com` (note the 's' for secure)

2. **CORS Configuration**: 
   - Already configured for production URLs
   - Will accept connections from frontend deployed on Render

3. **Connection Retry**: 
   - Built-in retry logic for Python server connections
   - 10-second timeout for WebSocket connections

4. **Language Support**: 
   - Multi-language support (English, Hindi, Punjabi, etc.)
   - Auto-fallback to English for unsupported languages

### ⚠️ Troubleshooting:

1. **Connection Failures**:
   - Check PYTHON_SERVER_URL is correct
   - Verify Python server is running and healthy
   - Check Render logs for connection errors

2. **CORS Issues**:
   - Verify frontend URL in FRONTEND_URL env var
   - Check browser console for CORS errors

3. **WebSocket Issues**:
   - Ensure using `wss://` not `ws://` for Render
   - Check firewall/proxy settings

### 📊 Monitoring:

Check Express backend health:
- Monitor CPU/Memory usage in Render dashboard
- Watch connection counts in logs
- Set up alerts for health check failures

### 💰 Cost Optimization:

- **Free Tier**: Good for testing, sleeps after 15 min
- **Starter ($7/month)**: Recommended, always-on
- **Scaling**: Auto-scale based on traffic if needed
