import 'dart:io';
import 'package:flutter/material.dart';
import 'package:logger/logger.dart';
import 'package:file_picker/file_picker.dart';
import '../features/chat/models/chat_message.dart';
import '../services/api_service.dart';
import '../services/location_service.dart';

class ChatProvider extends ChangeNotifier {
  final Logger _logger = Logger();
  
  List<ChatMessage> _messages = [];
  bool _isLoading = false;
  bool _isConnected = false;
  String _currentLocation = '';
  String _selectedLanguage = 'hi'; // Default to Hindi
  bool _useWebSocket = true;
  
  // Getters
  List<ChatMessage> get messages => _messages;
  bool get isLoading => _isLoading;
  bool get isConnected => _isConnected;
  String get currentLocation => _currentLocation;
  String get selectedLanguage => _selectedLanguage;
  bool get useWebSocket => _useWebSocket;
  
  // Language options
  final Map<String, String> _languages = {
    'hi': 'हिंदी',
    'en': 'English',
    'pa': 'ਪੰਜਾਬੀ',
    'gu': 'ગુજરાતી',
    'mr': 'मराठी',
  };
  
  Map<String, String> get languages => _languages;
  
  ChatProvider() {
    _initializeServices();
  }
  
  /// Initialize services
  Future<void> _initializeServices() async {
    try {
      // Initialize API service
      ApiService.initialize();
      
      // Get location
      await _updateLocation();
      
      // Initialize WebSocket if enabled
      if (_useWebSocket) {
        _initializeWebSocket();
      }
      
      _logger.i('Chat provider initialized');
    } catch (e) {
      _logger.e('Error initializing chat provider: $e');
    }
  }
  
  /// Initialize WebSocket connection
  void _initializeWebSocket() {
    ApiService.initializeSocket(
      onResponse: (data) {
        _handleAIResponse(data);
      },
      onError: (error) {
        _logger.e('WebSocket error: $error');
        _addSystemMessage('Connection error: $error');
        _isConnected = false;
        notifyListeners();
      },
      onConnect: () {
        _isConnected = true;
        _addSystemMessage('Connected to FarmMate AI');
        notifyListeners();
      },
      onDisconnect: () {
        _isConnected = false;
        _addSystemMessage('Disconnected from server');
        notifyListeners();
      },
    );
  }
  
  /// Update current location
  Future<void> _updateLocation() async {
    try {
      String location = await LocationService.getLocationForQuery();
      _currentLocation = location;
      _logger.i('Location updated: $location');
      notifyListeners();
    } catch (e) {
      _logger.e('Error updating location: $e');
    }
  }
  
  /// Send message
  Future<void> sendMessage({
    required String text,
    List<File>? files,
  }) async {
    if (text.trim().isEmpty && (files == null || files.isEmpty)) {
      return;
    }
    
    // Convert Files to PlatformFile objects
    List<PlatformFile>? platformFiles;
    if (files != null) {
      platformFiles = files.map((f) => PlatformFile(
        name: f.path.split('/').last,
        path: f.path,
        size: f.lengthSync(),
        bytes: null,
      )).toList();
    }
    
    // Add user message
    final userMessage = ChatMessage(
      text: text,
      sender: MessageSender.user,
      files: platformFiles,
      timestamp: DateTime.now(),
    );
    
    _messages.add(userMessage);
    _isLoading = true;
    notifyListeners();
    
    try {
      if (_useWebSocket && _isConnected) {
        // Send via WebSocket
        ApiService.sendMessageViaSocket(
          message: text,
          language: _selectedLanguage,
          location: _currentLocation,
        );
      } else {
        // Send via HTTP
        final response = await ApiService.sendMessage(
          message: text,
          language: _selectedLanguage,
          location: _currentLocation,
          files: files,
        );
        
        if (response != null) {
          _handleAIResponse(response);
        } else {
          _addErrorMessage('Failed to get response from AI service');
        }
      }
    } catch (e) {
      _logger.e('Error sending message: $e');
      _addErrorMessage('Error sending message: $e');
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }
  
  /// Handle AI response
  void _handleAIResponse(Map<String, dynamic> data) {
    try {
      String responseText = '';
      
      // Extract response based on your API structure
      if (data.containsKey('final_advice')) {
        responseText += '🌾 सलाह: ${data['final_advice']}\n\n';
      }
      
      if (data.containsKey('response')) {
        responseText += data['response'];
      }
      
      if (data.containsKey('summary_message')) {
        responseText += '\n\n📝 सारांश: ${data['summary_message']}';
      }
      
      if (responseText.isEmpty) {
        responseText = data.toString(); // Fallback
      }
      
      final aiMessage = ChatMessage(
        text: responseText,
        sender: MessageSender.bot,
        timestamp: DateTime.now(),
      );
      
      _messages.add(aiMessage);
      _isLoading = false;
      notifyListeners();
      
      _logger.i('AI response received and added');
    } catch (e) {
      _logger.e('Error handling AI response: $e');
      _addErrorMessage('Error processing AI response');
    }
  }
  
  /// Add system message
  void _addSystemMessage(String message) {
    final systemMessage = ChatMessage(
      text: message,
      sender: MessageSender.system,
      timestamp: DateTime.now(),
    );
    _messages.add(systemMessage);
  }
  
  /// Add error message
  void _addErrorMessage(String error) {
    final errorMessage = ChatMessage(
      text: '❌ $error',
      sender: MessageSender.system,
      timestamp: DateTime.now(),
    );
    _messages.add(errorMessage);
    _isLoading = false;
    notifyListeners();
  }
  
  /// Set language
  void setLanguage(String languageCode) {
    if (_languages.containsKey(languageCode)) {
      _selectedLanguage = languageCode;
      _logger.i('Language changed to: ${_languages[languageCode]}');
      notifyListeners();
    }
  }
  
  /// Toggle WebSocket usage
  void toggleWebSocket() {
    _useWebSocket = !_useWebSocket;
    _logger.i('WebSocket usage toggled: $_useWebSocket');
    
    if (_useWebSocket) {
      _initializeWebSocket();
    } else {
      ApiService.disconnectSocket();
      _isConnected = false;
    }
    notifyListeners();
  }
  
  /// Refresh location
  Future<void> refreshLocation() async {
    await _updateLocation();
  }
  
  /// Set custom location
  Future<void> setCustomLocation(String address) async {
    try {
      final position = await LocationService.getCoordinatesFromAddress(address);
      if (position != null) {
        await LocationService.saveLocation(position, address);
        _currentLocation = address;
        _logger.i('Custom location set: $address');
        notifyListeners();
      }
    } catch (e) {
      _logger.e('Error setting custom location: $e');
    }
  }
  
  /// Clear chat history
  void clearChat() {
    _messages.clear();
    _addSystemMessage('Chat cleared');
    notifyListeners();
  }
  
  /// Check service status
  Future<Map<String, bool>> getServiceStatus() async {
    return await ApiService.getServiceStatus();
  }
  
  @override
  void dispose() {
    ApiService.disconnectSocket();
    super.dispose();
  }
}
