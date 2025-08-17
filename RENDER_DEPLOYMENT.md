# FarmMate Render Deployment Guide

## Overview
This guide explains how to deploy FarmMate components on Render.com.

## Option 1: Deploy Python AI Server (Recommended Start)

### Manual Deployment via Render Dashboard

1. **Create New Web Service**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Web Service"
   - Connect your GitHub repository: `Xbectordash/Capital_one_hacathon`

2. **Configuration Settings**
   ```
   Name: farmmate-ai-server
   Branch: main (or agent-python)
   Root Directory: agent-python
   Environment: Production
   Language: Docker
   Region: Oregon (US West)
   Instance Type: Starter ($7/month) or Free
   ```

3. **Docker Settings**
   ```
   Dockerfile Path: agent-python/Dockerfile
   Docker Build Context Directory: agent-python
   Health Check Path: /health
   ```

4. **Environment Variables**
   Add these in the Render dashboard:
   ```
   PYTHONDONTWRITEBYTECODE=1
   PYTHONUNBUFFERED=1
   NODE_ENV=production
   PORT=8000
   GEMINI_API_KEY=your_actual_gemini_key
   WEATHER_API=your_actual_weather_key
   LANGSMITH_TRACING=true
   LANGSMITH_ENDPOINT=https://api.smith.langchain.com
   LANGSMITH_API_KEY=your_actual_langsmith_key
   AGMARKNET_API_KEY=your_actual_agmarknet_key
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Your service will be available at: `https://farmmate-ai-server.onrender.com`

### Testing Your Deployment

Once deployed, test these endpoints:
- Health Check: `https://farmmate-ai-server.onrender.com/health`
- API Docs: `https://farmmate-ai-server.onrender.com/docs`
- Test Page: `https://farmmate-ai-server.onrender.com/test-page`
- WebSocket: `wss://farmmate-ai-server.onrender.com/ws/{user_id}`

## Option 2: Deploy Full Stack (Multiple Services)

If you want to deploy the complete application, you'll need to create separate services:

### 1. Python AI Server (Backend Core)
- Follow Option 1 above

### 2. Express Backend (API Gateway)
```
Name: farmmate-backend
Root Directory: backend
Dockerfile Path: backend/Dockerfile
Environment Variables:
  - NODE_ENV=production
  - PORT=5000
  - PYTHON_SERVER_URL=wss://farmmate-ai-server.onrender.com
```

### 3. React Frontend (Web App)
```
Name: farmmate-frontend
Root Directory: frontend/web/agricultural-chat-app
Build Command: npm install && npm run build
Publish Directory: build
Environment Variables:
  - REACT_APP_BACKEND_URL=https://farmmate-backend.onrender.com
  - REACT_APP_SOCKET_URL=https://farmmate-backend.onrender.com
```

## Deployment using render.yaml (Alternative)

1. Use the provided `render.yaml` file in the repository root
2. Connect your repository to Render
3. Render will automatically detect and deploy based on the configuration

## Important Notes

### Free Tier Limitations
- Free instances spin down after 15 minutes of inactivity
- Cold starts can take 1-2 minutes
- No persistent storage
- Consider Starter plan ($7/month) for better performance

### Security
- Never commit API keys to the repository
- Add sensitive environment variables through Render dashboard
- Use Secret Files for private keys or certificates

### Monitoring
- Use Render's built-in logs and metrics
- Set up health checks for automatic restart
- Monitor resource usage to optimize instance type

## Troubleshooting

### Common Issues
1. **Build Failures**: Check Dockerfile paths and dependencies
2. **Health Check Failures**: Ensure `/health` endpoint is working
3. **Environment Variables**: Verify all required keys are set
4. **Port Issues**: Make sure your app listens on `0.0.0.0:$PORT`

### Logs Access
- View logs in Render dashboard
- Use SSH access (paid plans only) for debugging

## Production Optimizations

1. **Enable Auto-Deploy**: Automatic deployments on Git push
2. **Build Filters**: Only deploy when relevant files change
3. **Instance Scaling**: Use horizontal scaling for high traffic
4. **CDN**: Enable CDN for static assets
5. **Database**: Use Render PostgreSQL for persistent data

## Cost Estimation

- **Free Plan**: $0/month (limited resources, sleeps)
- **Starter Plan**: $7/month per service (basic production)
- **Standard Plan**: $25/month per service (recommended for production)

For full stack deployment (3 services on Starter): ~$21/month

## Next Steps

1. Start with Python AI Server deployment
2. Test the API endpoints
3. Deploy Express Backend if needed
4. Deploy React Frontend for complete web app
5. Set up monitoring and alerting
6. Configure custom domain (optional)
