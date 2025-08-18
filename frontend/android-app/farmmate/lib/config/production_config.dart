class ProductionConfig {
  // Production URLs for deployed services
  // Update these URLs when you deploy to Render or other cloud platforms
  
  // Render.com deployed URLs (update with your actual service names)
  static const String backendUrl = String.fromEnvironment(
    'BACKEND_URL',
    defaultValue: 'https://farmmate-backend.onrender.com',
  );
  
  static const String aiServiceUrl = String.fromEnvironment(
    'AI_SERVICE_URL', 
    defaultValue: 'https://farmmate-ai-server.onrender.com',
  );
  
  // Alternative cloud provider URLs (uncomment and update as needed)
  // static const String backendUrl = 'https://your-backend.herokuapp.com';
  // static const String aiServiceUrl = 'https://your-ai-service.herokuapp.com';
  // static const String backendUrl = 'https://your-backend.vercel.app';
  // static const String aiServiceUrl = 'https://your-ai-service.railway.app';
  
  // App settings
  static const String defaultLanguage = String.fromEnvironment(
    'DEFAULT_LANGUAGE',
    defaultValue: 'hi',
  );
  
  static const String defaultLocation = String.fromEnvironment(
    'DEFAULT_LOCATION',
    defaultValue: 'भारत',
  );
  
  // Feature flags for production
  static const bool enableWebSocket = bool.fromEnvironment(
    'ENABLE_WEBSOCKET',
    defaultValue: true,
  );
  
  static const bool enableLocation = bool.fromEnvironment(
    'ENABLE_LOCATION',
    defaultValue: true,
  );
  
  static const bool enableFileUpload = bool.fromEnvironment(
    'ENABLE_FILE_UPLOAD',
    defaultValue: true,
  );
  
  // Production connection settings (longer timeouts for deployed services)
  static const int connectionTimeout = 45; // seconds
  static const int requestTimeout = 90; // seconds
  
  // Production mode
  static const bool isDebugMode = bool.fromEnvironment(
    'DEBUG_MODE',
    defaultValue: false, // Disable debug in production
  );
  
  // API endpoints
  static String get chatEndpoint => '$backendUrl/api/chat';
  static String get healthEndpoint => '$backendUrl/health';
  static String get aiHealthEndpoint => '$aiServiceUrl/health';
  static String get socketUrl => backendUrl;
  
  // WebSocket URL with proper protocol
  static String get webSocketUrl {
    return backendUrl.replaceFirst('https://', 'wss://').replaceFirst('http://', 'ws://');
  }
  
  // Direct AI WebSocket URL (if needed)
  static String get aiWebSocketUrl {
    return aiServiceUrl.replaceFirst('https://', 'wss://').replaceFirst('http://', 'ws://');
  }
  
  // Get current configuration as map
  static Map<String, dynamic> toMap() {
    return {
      'backendUrl': backendUrl,
      'aiServiceUrl': aiServiceUrl,
      'defaultLanguage': defaultLanguage,
      'defaultLocation': defaultLocation,
      'enableWebSocket': enableWebSocket,
      'enableLocation': enableLocation,
      'enableFileUpload': enableFileUpload,
      'connectionTimeout': connectionTimeout,
      'requestTimeout': requestTimeout,
      'isDebugMode': isDebugMode,
      'webSocketUrl': webSocketUrl,
      'aiWebSocketUrl': aiWebSocketUrl,
    };
  }
  
  // Print configuration for debugging
  static void printConfig() {
    if (isDebugMode) {
      print('=== FarmMate Production Configuration ===');
      print('Backend URL: $backendUrl');
      print('AI Service URL: $aiServiceUrl');
      print('WebSocket URL: $webSocketUrl');
      print('AI WebSocket URL: $aiWebSocketUrl');
      print('Default Language: $defaultLanguage');
      print('Default Location: $defaultLocation');
      print('WebSocket Enabled: $enableWebSocket');
      print('Location Enabled: $enableLocation');
      print('File Upload Enabled: $enableFileUpload');
      print('Debug Mode: $isDebugMode');
      print('Connection Timeout: ${connectionTimeout}s');
      print('Request Timeout: ${requestTimeout}s');
      print('========================================');
    }
  }
  
  // Validate configuration
  static bool validateConfig() {
    bool isValid = true;
    
    if (!backendUrl.startsWith('http')) {
      print('❌ Invalid backend URL: $backendUrl');
      isValid = false;
    }
    
    if (!aiServiceUrl.startsWith('http')) {
      print('❌ Invalid AI service URL: $aiServiceUrl');
      isValid = false;
    }
    
    if (isValid) {
      print('✅ Configuration is valid');
    }
    
    return isValid;
  }
}
