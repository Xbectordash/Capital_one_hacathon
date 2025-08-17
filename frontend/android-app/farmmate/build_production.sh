#!/bin/bash

# FarmMate Android App - Production Build Script
# This script builds the Android app for production deployment

set -e

echo "🚀 FarmMate Android Production Build Script"
echo "==========================================="

# Check if we're in the right directory
if [ ! -f "pubspec.yaml" ]; then
    echo "❌ Error: pubspec.yaml not found. Run this script from the farmmate flutter project root."
    exit 1
fi

# Check if Flutter is installed
if ! command -v flutter &> /dev/null; then
    echo "❌ Error: Flutter not found. Please install Flutter and add it to PATH."
    exit 1
fi

echo "📋 Pre-build Checklist"
echo "====================="
echo "✅ Make sure backend services are deployed"
echo "✅ Update URLs in lib/config/production_config.dart"
echo "✅ Test services are responding to health checks"
echo ""

read -p "Have you completed the checklist above? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Please complete the checklist before building for production."
    exit 1
fi

echo "🔍 Validating Flutter setup..."
flutter doctor --android-licenses

echo "📦 Getting dependencies..."
flutter pub get

echo "🔧 Running code generation..."
if [ -f "build_runner.yaml" ] || grep -q "build_runner" pubspec.yaml; then
    flutter packages pub run build_runner build --delete-conflicting-outputs
fi

echo "🧹 Cleaning previous builds..."
flutter clean
flutter pub get

echo "🔨 Building production APK..."
echo "Building with production configuration (DEBUG_MODE=false)..."

# Build APK for production
flutter build apk \
    --dart-define=DEBUG_MODE=false \
    --dart-define=BACKEND_URL=https://farmmate-backend.onrender.com \
    --dart-define=AI_SERVICE_URL=https://farmmate-ai-server.onrender.com \
    --target-platform android-arm,android-arm64,android-x64 \
    --split-per-abi

echo "📱 Building App Bundle for Play Store..."
flutter build appbundle \
    --dart-define=DEBUG_MODE=false \
    --dart-define=BACKEND_URL=https://farmmate-backend.onrender.com \
    --dart-define=AI_SERVICE_URL=https://farmmate-ai-server.onrender.com

echo "✅ Build completed successfully!"
echo ""
echo "📁 Build artifacts:"
echo "   APK (Universal): build/app/outputs/flutter-apk/app-release.apk"
echo "   APK (Split):     build/app/outputs/flutter-apk/app-*-release.apk"
echo "   App Bundle:      build/app/outputs/bundle/release/app-release.aab"
echo ""

# Check if ADB is available for installation
if command -v adb &> /dev/null; then
    echo "📲 Install options:"
    echo "   adb install build/app/outputs/flutter-apk/app-release.apk"
    echo ""
    
    read -p "Install APK on connected device now? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "📲 Installing APK..."
        adb install -r build/app/outputs/flutter-apk/app-release.apk
        echo "✅ Installation completed!"
        
        echo ""
        echo "🧪 Testing suggestions:"
        echo "   1. Open the app and check Settings > Service Status"
        echo "   2. Test chat functionality with deployed backend"
        echo "   3. Verify location services work"
        echo "   4. Test file upload functionality"
    fi
fi

echo ""
echo "🚀 Next steps:"
echo "   1. Test the APK thoroughly on devices"
echo "   2. Verify all services are working"
echo "   3. Share APK or upload App Bundle to Play Console"
echo ""
echo "🎉 Production build ready for deployment!"
