# 🚀 FarmMate - Docker के बिना Build करें

## एक command में सब कुछ! 

```powershell
# Project root directory में जाएं और run करें:
.\build_local.ps1
```

यह script automatically सब कुछ build कर देगा! 

## 🎯 Quick Options

### 1. सब कुछ build करें (Complete Setup)
```powershell
.\build_local.ps1
# Choose option 1
```
**Result**: Python AI Service + Express Backend + Android APK सब ready!

### 2. Development mode में सब start करें  
```powershell
.\start_dev.ps1
```
**Result**: सभी services चालू हो जाएंगी और live testing कर सकते हैं!

### 3. केवल Android APK बनाएं
```powershell
cd frontend\android-app\farmmate
flutter build apk --debug
```

## 📱 Android App Test करें

### Emulator पर:
```powershell
flutter run
```

### Physical Device पर:
```powershell
# Build APK
flutter build apk --debug

# Install APK  
adb install build\app\outputs\flutter-apk\app-debug.apk
```

## 🌐 Service URLs (Local)

- **Python AI Service**: http://localhost:8000
- **Express Backend**: http://localhost:5000  
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🎉 बस इतना ही!

Docker के बिना building बहुत आसान है:
1. Run `.\build_local.ps1` 
2. सब कुछ automatically build हो जाएगा
3. APK ready मिल जाएगा!

**Total Time**: केवल 5-10 minutes! 🚀
