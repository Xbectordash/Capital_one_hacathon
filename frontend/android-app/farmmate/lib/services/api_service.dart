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
      
      print('🌐 === HTTP API CALL START ===');
      print('📍 API Endpoint: ${AppConfig.chatEndpoint}');
      print('👤 User ID: ${_currentUserId ?? 'anonymous'}');
      print('💬 Message: $message');
      print('🗣️ Language: $language');
      print('🌍 Location: $location');
      print('📁 Files: ${files?.length ?? 0}');
      
      var request = http.MultipartRequest('POST', uri);
      
      // Add text fields
      request.fields['user_id'] = _currentUserId ?? 'anonymous';
      request.fields['message'] = message;
      request.fields['language'] = language;
      request.fields['location'] = location;
      
      print('📋 Request Fields: ${request.fields}');
      
      // Add files if any
      if (files != null) {
        for (var file in files) {
          var multipartFile = await http.MultipartFile.fromPath(
            'files',
            file.path,
          );
          request.files.add(multipartFile);
          print('📄 Added file: ${file.path}');
        }
      }
      
      _logger.d('Sending message: $message');
      print('⏰ Request timeout: ${AppConfig.requestTimeout} seconds');
      
      final response = await request.send().timeout(
        Duration(seconds: AppConfig.requestTimeout),
      );
      final responseData = await response.stream.bytesToString();
      
      print('📨 Response Status Code: ${response.statusCode}');
      print('📄 Raw Response Data:');
      print(responseData);
      
      if (response.statusCode == 200) {
        final jsonData = json.decode(responseData);
        print('✅ JSON Parsed Successfully:');
        print(jsonData);
        _logger.i('Message sent successfully');
        print('🌐 === HTTP API CALL END (SUCCESS) ===');
        return jsonData;
      } else {
        print('❌ HTTP Error: ${response.statusCode}');
        print('❌ Response body: $responseData');
        _logger.e('Failed to send message: ${response.statusCode}');
        print('🌐 === HTTP API CALL END (ERROR) ===');
        return null;
      }
    } catch (e) {
      print('💥 Exception in HTTP call: $e');
      _logger.e('Error sending message: $e');
      print('🌐 === HTTP API CALL END (EXCEPTION) ===');
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
        print('🤖 === AI RESPONSE RECEIVED VIA WEBSOCKET ===');
        print('📨 Raw response data:');
        print(data);
        _logger.i('Received AI response');
        if (data is Map<String, dynamic>) {
          print('✅ Data is Map<String, dynamic>, calling onResponse');
          onResponse(data);
        } else {
          print('⚠️ Data is not Map<String, dynamic>, type: ${data.runtimeType}');
          print('🔄 Attempting to convert...');
          try {
            if (data is String) {
              final jsonData = json.decode(data);
              if (jsonData is Map<String, dynamic>) {
                print('✅ Successfully converted string to Map');
                onResponse(jsonData);
              } else {
                print('❌ Converted data is not Map<String, dynamic>');
                onResponse({'response': data.toString()});
              }
            } else {
              print('🔄 Converting to string format');
              onResponse({'response': data.toString()});
            }
          } catch (e) {
            print('❌ Error converting response: $e');
            onResponse({'response': data.toString()});
          }
        }
        print('🤖 === AI RESPONSE PROCESSING END ===');
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
    print('🔌 === WEBSOCKET MESSAGE START ===');
    print('📶 Socket connected: ${_socket?.connected}');
    
    if (_socket?.connected == true) {
      final data = {
        'query': message,
        'userId': _currentUserId,
        'language': language,
        'location': location,
        if (fileUrls != null) 'files': fileUrls,
      };
      
      print('📤 Sending data via WebSocket:');
      print(data);
      
      _socket!.emit('user_query', data);
      print('✅ Message emitted successfully');
      _logger.d('🐛 Message sent via WebSocket: $message');
      _logger.d('🐛 📍 Location sent: $location');
      _logger.d('🐛 🗣️ Language sent: $language');
    } else {
      print('❌ Socket not connected! Connection status: ${_socket?.connected}');
      _logger.e('Socket not connected');
    }
    print('🔌 === WEBSOCKET MESSAGE END ===');
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
