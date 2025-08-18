import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:logger/logger.dart';
import 'package:socket_io_client/socket_io_client.dart' as IO;
import '../config/app_config.dart';

class ApiService {
  static final Logger _logger = Logger();
  static IO.Socket? _socket;
  static String? _currentUserId;
  
  /// Initialize the API service
  static void initialize({String? userId}) {
    _currentUserId = userId ?? 'farmer_${DateTime.now().millisecondsSinceEpoch}';
    _logger.i('API Service initialized for user: $_currentUserId');
    
    // Print configuration in debug mode
    AppConfig.printConfig();
    
    // Validate configuration
    AppConfig.validateConfig();
  }
  
  /// Send message via HTTP API
  static Future<Map<String, dynamic>?> sendMessage({
    required String message,
    required String language,
    required String location,
    List<File>? files,
  }) async {
    try {
      final uri = Uri.parse(AppConfig.chatEndpoint);
      
      var request = http.MultipartRequest('POST', uri);
      
      // Add text fields
      request.fields['user_id'] = _currentUserId ?? 'anonymous';
      request.fields['message'] = message;
      request.fields['language'] = language;
      request.fields['location'] = location;
      
      // Add files if any
      if (files != null) {
        for (var file in files) {
          var multipartFile = await http.MultipartFile.fromPath(
            'files',
            file.path,
          );
          request.files.add(multipartFile);
        }
      }
      
      _logger.d('Sending message: $message');
      
      final response = await request.send().timeout(
        Duration(seconds: AppConfig.requestTimeout),
      );
      final responseData = await response.stream.bytesToString();
      
      if (response.statusCode == 200) {
        final jsonData = json.decode(responseData);
        _logger.i('Message sent successfully');
        return jsonData;
      } else {
        _logger.e('Failed to send message: ${response.statusCode}');
        return null;
      }
    } catch (e) {
      _logger.e('Error sending message: $e');
      return null;
    }
  }
  
  /// Initialize WebSocket connection
  static void initializeSocket({
    required Function(Map<String, dynamic>) onResponse,
    required Function(String) onError,
    required Function() onConnect,
    required Function() onDisconnect,
  }) {
    try {
      // Use the proper WebSocket URL based on environment
      final socketUrl = AppConfig.webSocketUrl;
      
      _socket = IO.io(socketUrl, <String, dynamic>{
        'transports': ['websocket'],
        'autoConnect': false,
        'timeout': AppConfig.connectionTimeout * 1000,
        'forceNew': true,
        'reconnection': true,
        'reconnectionAttempts': 5,
        'reconnectionDelay': 2000,
      });
      
      _logger.i('Initializing WebSocket connection to: $socketUrl');
      
      _socket!.onConnect((_) {
        _logger.i('Connected to WebSocket at: $socketUrl');
        onConnect();
        
        // Join user room
        if (_currentUserId != null) {
          _socket!.emit('join_room', {'user_id': _currentUserId});
        }
      });
      
      _socket!.onDisconnect((_) {
        _logger.w('Disconnected from WebSocket');
        onDisconnect();
      });
      
      _socket!.on('ai_response', (data) {
        _logger.i('Received AI response');
        if (data is Map<String, dynamic>) {
          onResponse(data);
        }
      });
      
      _socket!.on('error', (error) {
        _logger.e('WebSocket error: $error');
        onError(error.toString());
      });
      
      _socket!.on('connect_error', (error) {
        _logger.e('WebSocket connection error: $error');
        onError('Connection failed: $error');
      });
      
      _socket!.connect();
    } catch (e) {
      _logger.e('Error initializing socket: $e');
      onError(e.toString());
    }
  }
  
  /// Send message via WebSocket
  static void sendMessageViaSocket({
    required String message,
    required String language,
    required String location,
    List<String>? fileUrls,
  }) {
    if (_socket?.connected == true) {
      final data = {
        'query': message,
        'userId': _currentUserId,
        'language': language,
        'location': location,
        if (fileUrls != null) 'files': fileUrls,
      };
      
      _socket!.emit('user_query', data);
      _logger.d('🐛 Message sent via WebSocket: $message');
      _logger.d('🐛 📍 Location sent: $location');
      _logger.d('🐛 🗣️ Language sent: $language');
    } else {
      _logger.e('Socket not connected');
    }
  }
  
  /// Disconnect WebSocket
  static void disconnectSocket() {
    _socket?.disconnect();
    _socket = null;
    _logger.i('WebSocket disconnected');
  }
  
  /// Check backend health
  static Future<bool> checkBackendHealth() async {
    try {
      final response = await http.get(
        Uri.parse(AppConfig.healthEndpoint),
        headers: {'Content-Type': 'application/json'},
      ).timeout(Duration(seconds: AppConfig.connectionTimeout));
      
      return response.statusCode == 200;
    } catch (e) {
      _logger.e('Backend health check failed: $e');
      return false;
    }
  }
  
  /// Check AI service health
  static Future<bool> checkAIServiceHealth() async {
    try {
      final response = await http.get(
        Uri.parse(AppConfig.aiHealthEndpoint),
        headers: {'Content-Type': 'application/json'},
      ).timeout(Duration(seconds: AppConfig.connectionTimeout));
      
      return response.statusCode == 200;
    } catch (e) {
      _logger.e('AI service health check failed: $e');
      return false;
    }
  }
  
  /// Get service status
  static Future<Map<String, bool>> getServiceStatus() async {
    final backendStatus = await checkBackendHealth();
    final aiServiceStatus = await checkAIServiceHealth();
    
    return {
      'backend': backendStatus,
      'ai_service': aiServiceStatus,
    };
  }
}
