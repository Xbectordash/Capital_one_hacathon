# FarmMate Flutter App

This is the FarmMate Flutter application for the Capital One Hackathon project.

## Setup & Build (Docker)

1. Build the Docker image:
   ```sh
   docker build -t farmmate-web -f ../dockerfile .
   ```
2. Run the container:
   ```sh
   docker run -p 8080:80 farmmate-web
   ```
3. Access the app at [http://localhost:8080](http://localhost:8080)

## Development
- Main entry point: `lib/main.dart`
- To build locally, use:
  ```sh
  flutter build web
  ```
- The web build output is in `build/web/`

## License
MIT
# 📱 FarmMate Android App

AI-powered farming assistant mobile application built with Flutter, integrated with FarmMate backend services for intelligent agricultural guidance.

## 🌟 Features

### 🤖 **AI-Powered Chat**
- Real-time chat with agricultural AI assistant
- Multi-language support (Hindi, English, Punjabi, Gujarati, Marathi)
- File upload support (images, documents)
- Voice-to-text input with speech recognition

### 📍 **Location Integration**
- Automatic location detection using device GPS
- Manual location setting with address search
- Location-based farming advice and recommendations
- Persistent location storage for convenience

### 🔌 **Backend Connectivity**
- RESTful API integration with Express.js backend
- Real-time WebSocket communication
- Health monitoring of backend services
- Automatic fallback between connection methods

### 🎨 **Modern UI/UX**
- Material Design with custom glass-morphism effects
- Responsive design for all screen sizes
- Dark/Light theme adaptation
- Smooth animations and transitions

---

## 🚀 Quick Start

### 📋 Prerequisites

**Required:**
- **Flutter SDK** 3.8.1+
- **Dart SDK** 3.8.1+
- **Android Studio** or **VS Code** with Flutter extensions
- **Android SDK** (API level 21+)
- **FarmMate Backend Services** running (Express.js + Python AI)

**Optional:**
- **Physical Android device** or **emulator**
- **VS Code Flutter extensions**

### 🔧 Installation

#### 1. **Clone Repository**
```bash
# Navigate to the Android app directory
cd frontend/android-app/farmmate
```

#### 2. **Install Dependencies**
```bash
# Get Flutter packages
flutter pub get

# For iOS (if needed)
cd ios && pod install && cd ..
```

#### 3. **Configure Environment**

Update `lib/config/app_config.dart` with your backend URLs:

```dart
// For Android Emulator
static const String backendUrl = 'http://10.0.2.2:5000';
static const String aiServiceUrl = 'http://10.0.2.2:8000';

// For Physical Device (replace with your computer's IP)
// static const String backendUrl = 'http://192.168.1.100:5000';
// static const String aiServiceUrl = 'http://192.168.1.100:8000';

// For Production
// static const String backendUrl = 'https://your-backend-url.com';
// static const String aiServiceUrl = 'https://your-ai-service-url.com';
```

#### 4. **Run the App**

```bash
# Check connected devices
flutter devices

# Run on connected device/emulator
flutter run

# Build for release
flutter build apk --release
```

---

## 📱 App Structure

```
📱 farmmate/
├── 📄 pubspec.yaml                     # Dependencies and config
├── 📄 README.md                        # This documentation
├── 📄 .env                            # Environment variables
│
├── 📁 lib/                            # Main application code
│   ├── main.dart                      # App entry point
│   ├── app.dart                       # App configuration
│   │
│   ├── 📁 config/                     # Configuration
│   │   └── app_config.dart            # API URLs and settings
│   │
│   ├── 📁 providers/                  # State management
│   │   └── chat_provider.dart         # Chat and location state
│   │
│   ├── 📁 services/                   # Backend integration
│   │   ├── api_service.dart           # HTTP/WebSocket API
│   │   └── location_service.dart      # GPS and geocoding
│   │
│   ├── 📁 features/                   # Feature modules
│   │   ├── 📁 home/                   # Home screen
│   │   ├── 📁 chat/                   # Chat functionality
│   │   │   ├── models/                # Chat data models
│   │   │   └── widgets/               # Chat UI components
│   │   └── 📁 settings/               # Settings screens
│   │       └── screens/               # Location & language settings
│   │
│   └── 📁 utils/                      # Utilities
│       ├── constants/                 # App constants
│       └── extensions/                # Helper extensions
│
├── 📁 android/                        # Android platform code
│   └── app/src/main/AndroidManifest.xml  # Permissions & config
│
├── 📁 ios/                           # iOS platform code
├── 📁 assets/                        # App assets
│   └── icons/                        # Custom icons
└── 📁 test/                         # Unit tests
```

---

## ⚙️ Configuration Options

### 🌐 **Backend URLs**

| Environment | Backend URL | AI Service URL |
|-------------|-------------|----------------|
| **Android Emulator** | `http://10.0.2.2:5000` | `http://10.0.2.2:8000` |
| **Physical Device** | `http://YOUR_IP:5000` | `http://YOUR_IP:8000` |
| **Production** | `https://your-backend.com` | `https://your-ai.com` |

### 🗣️ **Supported Languages**

| Code | Language | Native Name |
|------|----------|-------------|
| `hi` | Hindi | हिंदी |
| `en` | English | English |
| `pa` | Punjabi | ਪੰਜਾਬੀ |
| `gu` | Gujarati | ગુજરાતી |
| `mr` | Marathi | मराठी |

### 🔧 **App Settings**

- **WebSocket**: Real-time communication (can be toggled)
- **Location**: GPS-based location detection
- **File Upload**: Image and document sharing
- **Speech Recognition**: Voice input support

---

## 🔌 API Integration

### 📡 **HTTP API Example**
```dart
// Send message via HTTP
final response = await ApiService.sendMessage(
  message: 'बारिश के मौसम में कौन सी फसल लगाऊं?',
  language: 'hi',
  location: 'राजस्थान',
);
```

### 🌐 **WebSocket Example**
```dart
// Initialize WebSocket
ApiService.initializeSocket(
  onResponse: (data) => print('AI Response: ${data['response']}'),
  onError: (error) => print('Error: $error'),
  onConnect: () => print('Connected'),
  onDisconnect: () => print('Disconnected'),
);

// Send message via WebSocket
ApiService.sendMessageViaSocket(
  message: 'मेरी फसल में कीड़े लग गए हैं',
  language: 'hi',
  location: 'महाराष्ट्र',
);
```

### 📍 **Location Services**
```dart
// Get current location
Position? position = await LocationService.getCurrentPosition();

// Get address from coordinates
String? address = await LocationService.getAddressFromCoordinates(
  position.latitude, 
  position.longitude,
);

// Save location for future use
await LocationService.saveLocation(position, address);
```

---

## 🔐 Permissions

The app requires the following Android permissions:

```xml
<!-- Core functionality -->
<uses-permission android:name="android.permission.INTERNET"/>
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>

<!-- Location services -->
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION"/>

<!-- File access -->
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>

<!-- Voice input -->
<uses-permission android:name="android.permission.RECORD_AUDIO"/>
```

---

## 🧪 Testing

### 🔍 **Run Tests**
```bash
# Unit tests
flutter test

# Integration tests
flutter test integration_test/

# Widget tests
flutter test test/widget_test.dart
```

### 📱 **Manual Testing**
1. **Chat Functionality**: Send messages and verify AI responses
2. **Location Services**: Test GPS detection and manual location setting
3. **File Upload**: Upload images and documents
4. **Voice Input**: Test speech-to-text functionality
5. **Settings**: Test language and connection preferences

---

## 🚀 Deployment

### 📦 **Build Release APK**
```bash
# Build release APK
flutter build apk --release

# Build App Bundle (recommended for Play Store)
flutter build appbundle --release

# Install on device
flutter install --release
```

### 🏪 **Play Store Deployment**
1. Update `android/app/build.gradle` with version info
2. Generate signed APK/App Bundle
3. Upload to Google Play Console
4. Follow Play Store deployment guidelines

---

## 🛠️ Development

### 🔧 **Setup Development Environment**
```bash
# Check Flutter installation
flutter doctor

# Enable Flutter for VS Code
code --install-extension Dart-Code.flutter

# Hot reload during development
flutter run --hot-reload
```

### 📝 **Code Style**
- Follow **Flutter/Dart style guide**
- Use **meaningful variable names**
- Add **comments** for complex logic
- Implement **error handling**

---

## 🐛 Troubleshooting

### ❌ **Common Issues**

#### **"Connection Refused" Error**
```
Solution: Update backend URL in app_config.dart
- For emulator: Use 10.0.2.2 instead of localhost
- For device: Use computer's IP address
- Check if backend services are running
```

#### **Location Permission Denied**
```
Solution: Grant location permissions manually
- Go to Settings > Apps > FarmMate > Permissions
- Enable Location permission
- Restart the app
```

#### **WebSocket Connection Failed**
```
Solution: Check network connectivity
- Verify backend WebSocket server is running
- Try toggling WebSocket in app settings
- Use HTTP mode as fallback
```

#### **Build Errors**
```
Solution: Clean and rebuild
flutter clean
flutter pub get
flutter build apk
```

---

## 📚 Documentation

- **[Flutter Documentation](https://flutter.dev/docs)**
- **[Provider State Management](https://pub.dev/packages/provider)**
- **[Socket.IO Client](https://pub.dev/packages/socket_io_client)**
- **[Geolocator Plugin](https://pub.dev/packages/geolocator)**

---

## 🤝 Contributing

1. **Fork** the repository
2. **Create** feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** changes: `git commit -m 'Add amazing feature'`
4. **Push** to branch: `git push origin feature/amazing-feature`
5. **Submit** pull request

---

## 📄 License

This project is licensed under the **MIT License** - see the LICENSE file for details.

---

**📱 FarmMate Android App | Built with Flutter | Powered by AI 🌾**
