# FarmMate Android App - Deployed Services Integration

## 🎯 Overview

The FarmMate Android app is now configured to work with **deployed services** rather than localhost. This guide explains how the app connects to production services and how to deploy them.

## 🏗️ Architecture with Deployed Services

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Android App   │────│  Express Backend │────│  Python AI      │
│  (Mobile/APK)   │    │  (Render/Heroku) │    │  (Render/Heroku)│
└─────────────────┘    └──────────────────┘    └─────────────────┘
        │                       │                       │
        │                       │                       │
    HTTP/WebSocket         WebSocket/HTTP          LangChain/AI
        │                       │                       │
        └───────────────────────┴───────────────────────┘
            Production URLs (HTTPS/WSS)
```

## 📱 App Configuration

The app automatically detects the environment and uses appropriate URLs:

### Development Mode (Debug)
- Backend: `http://10.0.2.2:5000` (Android emulator)
- AI Service: `http://10.0.2.2:8000` (Android emulator)
- WebSocket: `ws://10.0.2.2:5000`

### Production Mode (Release)
- Backend: `https://farmmate-backend.onrender.com`
- AI Service: `https://farmmate-ai-server.onrender.com`
- WebSocket: `wss://farmmate-backend.onrender.com`

## 🚀 Deployment Steps

### Step 1: Deploy Backend Services

Deploy in this order:

#### 1. Python AI Server (Core)
```bash
# Deploy to Render.com
Name: farmmate-ai-server
URL: https://farmmate-ai-server.onrender.com
Repository: agent-python folder
Dockerfile: agent-python/Dockerfile
```

Environment Variables:
```
PYTHONDONTWRITEBYTECODE=1
PYTHONUNBUFFERED=1
NODE_ENV=production
PORT=8000
GEMINI_API_KEY=your_actual_key
WEATHER_API=your_actual_key
LANGSMITH_API_KEY=your_actual_key
AGMARKNET_API_KEY=your_actual_key
```

#### 2. Express Backend (Gateway)
```bash
# Deploy to Render.com
Name: farmmate-backend
URL: https://farmmate-backend.onrender.com
Repository: backend folder
Dockerfile: backend/Dockerfile
```

Environment Variables:
```
NODE_ENV=production
PORT=5000
PYTHON_SERVER_URL=wss://farmmate-ai-server.onrender.com
```

### Step 2: Update Android App URLs

If you deploy to different URLs, update `lib/config/production_config.dart`:

```dart
// Update these with your actual deployment URLs
static const String backendUrl = 'https://your-backend.onrender.com';
static const String aiServiceUrl = 'https://your-ai-service.onrender.com';
```

### Step 3: Build Production APK

```bash
# Navigate to android app directory
cd frontend/android-app/farmmate

# Get dependencies
flutter pub get

# Build production APK
flutter build apk --dart-define=DEBUG_MODE=false

# Or build app bundle for Play Store
flutter build appbundle --dart-define=DEBUG_MODE=false
```

The APK will be generated at:
`build/app/outputs/flutter-apk/app-release.apk`

## 🔧 Service Status Monitoring

The app includes built-in service monitoring:

### 1. Settings Screen
- Go to Settings → View deployment status
- Real-time health checks for all services
- Shows current URLs and connection status

### 2. API Service
- Automatic health checks on app start
- Retry logic for failed connections
- WebSocket reconnection handling

### 3. Configuration Validation
- Environment detection (dev/prod)
- URL validation
- Service availability checks

## 🌐 Supported Deployment Platforms

### Primary (Recommended)
- **Render.com** - Easy Docker deployment
- **Heroku** - Git-based deployment
- **Railway** - Modern deployment platform

### Alternative
- **Vercel** - Frontend hosting
- **Netlify** - Static hosting
- **DigitalOcean** - VPS hosting
- **AWS** - Comprehensive cloud

## 📋 Pre-Deployment Checklist

### Backend Services
- [ ] Python AI server deployed and accessible
- [ ] Express backend deployed and accessible
- [ ] Environment variables configured
- [ ] API keys set up securely
- [ ] Health endpoints responding
- [ ] WebSocket connections working

### Android App
- [ ] Production URLs updated in config
- [ ] Debug mode disabled for production
- [ ] Permissions configured (location, internet)
- [ ] App tested with deployed services
- [ ] APK signed for distribution

## 🛠️ Testing Deployed Services

### 1. Service Health Checks
```bash
# Test Python AI server
curl https://farmmate-ai-server.onrender.com/health

# Test Express backend
curl https://farmmate-backend.onrender.com/health

# Test WebSocket (using wscat)
wscat -c wss://farmmate-backend.onrender.com/socket.io/?transport=websocket
```

### 2. Android App Testing
1. Build production APK
2. Install on physical device or emulator
3. Check Settings → Service Status
4. Test chat functionality
5. Verify location services
6. Test file uploads

### 3. Performance Testing
- Cold start times (Render services sleep after 15 min)
- Response times for chat
- WebSocket connection stability
- File upload speeds

## 🔍 Troubleshooting

### Common Issues

#### 1. Service Not Responding
```
Problem: 404 or timeout errors
Solution: 
- Check if service is deployed correctly
- Verify environment variables
- Check Render logs for errors
```

#### 2. WebSocket Connection Failed
```
Problem: WebSocket not connecting
Solution:
- Ensure URLs use wss:// for HTTPS sites
- Check CORS settings in backend
- Verify socket.io configuration
```

#### 3. Android Network Issues
```
Problem: App can't connect to services
Solution:
- Check internet permissions in AndroidManifest.xml
- Verify URLs in production_config.dart
- Test with mobile data and WiFi
```

#### 4. Cold Start Delays
```
Problem: First request takes long time
Solution:
- Use Render paid plans to avoid sleeping
- Implement keep-alive pings
- Show loading states in app
```

### Debug Commands

```bash
# Check Android app logs
flutter logs

# Check specific service logs
adb logcat | grep -i farmmate

# Test network connectivity
adb shell ping farmmate-backend.onrender.com

# Check WebSocket from browser
# Visit deployed backend URL + /test-page
```

## 📊 Service URLs Summary

| Service | Development | Production |
|---------|-------------|------------|
| Express Backend | http://10.0.2.2:5000 | https://farmmate-backend.onrender.com |
| Python AI | http://10.0.2.2:8000 | https://farmmate-ai-server.onrender.com |
| WebSocket | ws://10.0.2.2:5000 | wss://farmmate-backend.onrender.com |
| Health Check | http://10.0.2.2:5000/health | https://farmmate-backend.onrender.com/health |

## 🔗 Next Steps

1. **Deploy Services**: Follow the deployment guide to get services online
2. **Update URLs**: Modify production_config.dart with your actual URLs
3. **Build APK**: Create production APK with deployment URLs
4. **Test**: Verify all functionality with deployed services
5. **Distribute**: Share APK or publish to app stores

## 💡 Production Tips

1. **Use Paid Plans**: Free Render plans sleep after 15 minutes
2. **Monitor Logs**: Set up log monitoring for deployed services
3. **Health Checks**: Implement robust health checking
4. **Error Handling**: Handle network failures gracefully
5. **Caching**: Implement offline capabilities for better UX

## 🎉 Success Criteria

Your deployment is successful when:
- ✅ All health checks pass
- ✅ Android app connects to deployed services
- ✅ Chat functionality works end-to-end
- ✅ WebSocket real-time communication works
- ✅ Location services integrate properly
- ✅ File uploads work correctly

Ready to deploy your FarmMate services! 🚀
