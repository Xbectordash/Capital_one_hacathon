# 🎯 Flutter App URLs Configuration Guide

## कौन सा URL कब use होगा?

Flutter app **automatically detect** करती है कि कौन से URLs use करने हैं:

### 🔧 Development Mode (Debug Build):
```powershell
flutter run
# या 
flutter build apk --debug
```
**URLs Used:**
- Backend: `http://10.0.2.2:5000` (localhost for emulator)
- AI Service: `http://10.0.2.2:8000` (localhost for emulator)

### 🚀 Production Mode (Release Build):
```powershell
flutter build apk --release --dart-define=DEBUG_MODE=false
# या
flutter build apk --dart-define=DEBUG_MODE=false
```
**URLs Used:**
- Backend: `https://farmmate-backend.onrender.com` (deployed service)
- AI Service: `https://farmmate-ai-server.onrender.com` (deployed service)

## 📱 Current App Configuration

आपकी app में **smart switching** है:

```dart
// app_config.dart में
static bool get isProduction => !const bool.fromEnvironment('DEBUG_MODE', defaultValue: true);

static String get backendUrl {
  if (isProduction) {
    return ProductionConfig.backendUrl; // Deployed URLs
  }
  return 'http://10.0.2.2:5000'; // Localhost
}
```

## 🎯 Build Commands और URLs

### 1. Local Development (Localhost URLs):
```powershell
# Debug build - localhost use करेगा
flutter build apk --debug

# Regular run - localhost use करेगा  
flutter run
```
**Result**: App localhost services (10.0.2.2:5000) से connect करेगी

### 2. Production Build (Deployed URLs):
```powershell
# Production build - deployed services use करेगा
flutter build apk --release --dart-define=DEBUG_MODE=false

# या manual URL specify करें
flutter build apk --release --dart-define=DEBUG_MODE=false --dart-define=BACKEND_URL=https://your-backend.com
```
**Result**: App deployed services से connect करेगी

### 3. Custom URLs (अगर आपके अलग URLs हैं):
```powershell
flutter build apk --release \
  --dart-define=DEBUG_MODE=false \
  --dart-define=BACKEND_URL=https://your-custom-backend.com \
  --dart-define=AI_SERVICE_URL=https://your-custom-ai.com
```

## 🔍 कैसे Check करें कि कौन से URLs use हो रहे हैं?

### App के अंदर check करें:
1. App open करें
2. Settings screen जाएं  
3. "Service Status" या "Deployment Status" देखें
4. Current URLs दिखाई देंगे

### Code में check करें:
```dart
// main.dart में यह print होगा:
AppConfig.printConfig(); // URLs print करेगा
```

## 🚀 आपके लिए Ready Commands

### Local Testing के लिए:
```powershell
# Local services के साथ test करने के लिए
flutter build apk --debug
adb install build\app\outputs\flutter-apk\app-debug.apk
```

### Production APK के लिए:
```powershell
# Deployed services के साथ production APK
flutter build apk --release --dart-define=DEBUG_MODE=false
adb install build\app\outputs\flutter-apk\app-release.apk
```

## 📊 URL Comparison Table

| Build Type | DEBUG_MODE | Backend URL | AI Service URL | Use Case |
|------------|------------|-------------|----------------|----------|
| **Debug** | true | `http://10.0.2.2:5000` | `http://10.0.2.2:8000` | Local development |
| **Release** | true | `http://10.0.2.2:5000` | `http://10.0.2.2:8000` | Local testing |
| **Release** | false | `https://farmmate-backend.onrender.com` | `https://farmmate-ai-server.onrender.com` | **Production** |

## 🎯 आपका सवाल का जवाब:

> **"अगर मैं flutter build apk करूंगा तो hosted services वाला app बनेगा ना?"**

**Answer**: यह depend करता है कि आप कौन सा command use करते हैं:

### ❌ Localhost URLs (Local services):
```powershell
flutter build apk --debug
flutter build apk --release  # Without DEBUG_MODE=false
```

### ✅ Hosted/Deployed URLs (Production services):
```powershell
flutter build apk --release --dart-define=DEBUG_MODE=false
```

## 💡 Recommendation

Production APK के लिए हमेशा यह command use करें:
```powershell
flutter build apk --release --dart-define=DEBUG_MODE=false
```

या आसान तरीके से:
```powershell
.\build_production.ps1  # यह automatically सही flags use करेगा
```

## 🧪 Test करने के लिए:

1. **Local services के साथ test**: `flutter build apk --debug`
2. **Deployed services के साथ test**: `flutter build apk --release --dart-define=DEBUG_MODE=false`

App के Settings में जाकर देख सकते हैं कि कौन से URLs use हो रहे हैं! 🎯
