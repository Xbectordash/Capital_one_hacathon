class AppConfig {
  // Environment-based URLs - can be overridden via dart-define or .env
  static const String backendUrl = String.fromEnvironment(
    'BACKEND_URL',
    defaultValue: 'https://capital-one-hacathon-1.onrender.com',
  );
  
  static const String aiServiceUrl = String.fromEnvironment(
    'AI_SERVICE_URL', 
    defaultValue: 'https://capital-one-hacathon-1.onrender.com',  // Same as backend
  );
  
  // App settings
  static const String defaultLanguage = String.fromEnvironment(
    'DEFAULT_LANGUAGE',
    defaultValue: 'hi',
  );
  
  static const String defaultLocation = String.fromEnvironment(
    'DEFAULT_LOCATION',
    defaultValue: 'भारत',
  );
  
  // Feature flags
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
  
  // Connection settings
  static const int connectionTimeout = int.fromEnvironment(
    'CONNECTION_TIMEOUT',
    defaultValue: 45, // seconds
  );
  
  static const int requestTimeout = int.fromEnvironment(
    'REQUEST_TIMEOUT', 
    defaultValue: 90, // seconds
  );
  
  // Debug mode
  static const bool isDebugMode = bool.fromEnvironment(
    'DEBUG_MODE',
    defaultValue: false,
  );
  
  // API endpoints
  static String get chatEndpoint => '$backendUrl/api/chat';
  static String get healthEndpoint => '$backendUrl/health';
  static String get aiHealthEndpoint => '$aiServiceUrl/health';
  static String get socketUrl => backendUrl;
  
  // WebSocket URL with proper protocol conversion
  static String get webSocketUrl => backendUrl.replaceFirst('https://', 'wss://').replaceFirst('http://', 'ws://');
  
  // Direct AI WebSocket URL (if needed)
  static String get aiWebSocketUrl => aiServiceUrl.replaceFirst('https://', 'wss://').replaceFirst('http://', 'ws://');
  
  // Get current configuration as map
  static Map<String, dynamic> toMap() {
    return {
      'backendUrl': backendUrl,
      'aiServiceUrl': aiServiceUrl,
      'webSocketUrl': webSocketUrl,
      'aiWebSocketUrl': aiWebSocketUrl,
      'defaultLanguage': defaultLanguage,
      'defaultLocation': defaultLocation,
      'enableWebSocket': enableWebSocket,
      'enableLocation': enableLocation,
      'enableFileUpload': enableFileUpload,
      'connectionTimeout': connectionTimeout,
      'requestTimeout': requestTimeout,
      'isDebugMode': isDebugMode,
    };
  }
  
  // Print configuration for debugging
  static void printConfig() {
    if (isDebugMode) {
      print('=== FarmMate App Configuration ===');
      print('Backend URL: $backendUrl');
      print('AI Service URL: $aiServiceUrl');
      print('WebSocket URL: $webSocketUrl');
      print('AI WebSocket URL: $aiWebSocketUrl');
      print('Default Language: $defaultLanguage');
      print('Default Location: $defaultLocation');
      print('WebSocket Enabled: $enableWebSocket');
      print('Location Enabled: $enableLocation');
      print('File Upload Enabled: $enableFileUpload');
      print('Connection Timeout: ${connectionTimeout}s');
      print('Request Timeout: ${requestTimeout}s');
      print('Debug Mode: $isDebugMode');
      print('================================');
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
