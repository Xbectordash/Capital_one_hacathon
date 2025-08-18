import 'dart:io';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:logger/logger.dart';
import 'package:file_picker/file_picker.dart';
import '../features/chat/models/chat_message.dart';
import '../services/api_service.dart';
import '../services/location_service.dart';
import '../utils/localization/app_localizations.dart';

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
    'ta': 'தமிழ்',
    'te': 'తెలుగు',
    'bn': 'বাংলা',
  };
  
  Map<String, String> get languages => _languages;
  
  /// Change selected language
  void changeLanguage(String languageCode) {
    if (_languages.containsKey(languageCode)) {
      _selectedLanguage = languageCode;
      _logger.i('Language changed to: $languageCode (${_languages[languageCode]})');
      notifyListeners();
    }
  }
  
  /// Get current language display name
  String get currentLanguageDisplay => _languages[_selectedLanguage] ?? 'हिंदी';
  
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
    
    print('🚀 === SENDING MESSAGE START ===');
    print('📝 User Message: $text');
    print('📁 Files Count: ${files?.length ?? 0}');
    print('🌍 Location: $_currentLocation');
    print('🗣️ Language: $_selectedLanguage');
    
    // Convert Files to PlatformFile objects
    List<PlatformFile>? platformFiles;
    if (files != null) {
      platformFiles = files.map((f) => PlatformFile(
        name: f.path.split('/').last,
        path: f.path,
        size: f.lengthSync(),
        bytes: null,
      )).toList();
      print('📂 Files: ${platformFiles.map((f) => f.name).join(', ')}');
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
    
    print('⏳ Loading state set to: $_isLoading');
    print('💬 User message added to chat');
    
    try {
      if (_useWebSocket && _isConnected) {
        print('🔌 Sending via WebSocket...');
        // Send via WebSocket
        ApiService.sendMessageViaSocket(
          message: text,
          language: _selectedLanguage,
          location: _currentLocation,
        );
      } else {
        print('📡 Sending via HTTP...');
        // Send via HTTP
        final response = await ApiService.sendMessage(
          message: text,
          language: _selectedLanguage,
          location: _currentLocation,
          files: files,
        );
        
        print('📨 HTTP Response received');
        if (response != null) {
          print('✅ Response is not null, processing...');
          _handleAIResponse(response);
        } else {
          print('❌ Response is null!');
          _addErrorMessage('Failed to get response from AI service');
        }
      }
    } catch (e) {
      print('❌ Exception occurred: $e');
      _logger.e('Error sending message: $e');
      _addErrorMessage('Error sending message: $e');
    } finally {
      if (!_useWebSocket || !_isConnected) {
        _isLoading = false;
        notifyListeners();
        print('⭕ Loading state set to: $_isLoading (finally block)');
      }
    }
    
    print('🚀 === SENDING MESSAGE END ===');
  }
  
  /// Handle AI response
  void _handleAIResponse(Map<String, dynamic> data) {
    try {
      // पूरा response terminal में print करते हैं
      _logger.i('🔥 Full AI Response received:');
      print('🔥 ==== COMPLETE AI RESPONSE START ====');
      print(data);
      print('🔥 ==== COMPLETE AI RESPONSE END ====');
      
      String responseText = '';
      
      // Extract response based on your API structure
      if (data.containsKey('final_advice')) {
        responseText += '🌾 सलाह: ${data['final_advice']}\n\n';
        print('🌾 Final Advice: ${data['final_advice']}');
      }
      
      if (data.containsKey('response')) {
        responseText += data['response'];
        print('📝 Response: ${data['response']}');
      }
      
      if (data.containsKey('summary_message')) {
        responseText += '\n\n📝 सारांश: ${data['summary_message']}';
        print('📋 Summary: ${data['summary_message']}');
      }
      
      // Check for other possible response keys
      if (data.containsKey('message')) {
        responseText += data['message'];
        print('💬 Message: ${data['message']}');
      }
      
      if (data.containsKey('answer')) {
        responseText += data['answer'];
        print('✅ Answer: ${data['answer']}');
      }
      
      if (data.containsKey('text')) {
        responseText += data['text'];
        print('📄 Text: ${data['text']}');
      }
      
      // If still empty, show full response but formatted
      if (responseText.isEmpty) {
        responseText = 'Response received:\n${_formatJsonResponse(data)}';
        print('⚠️ Using full response as text was empty');
      }
      
      final aiMessage = ChatMessage(
        text: responseText,
        sender: MessageSender.bot,
        timestamp: DateTime.now(),
      );
      
      _messages.add(aiMessage);
      _isLoading = false;
      notifyListeners();
      
      print('✅ AI response processed and added to chat');
      _logger.i('AI response received and added');
    } catch (e) {
      print('❌ Error processing AI response: $e');
      _logger.e('Error handling AI response: $e');
      _addErrorMessage('Error processing AI response: $e');
    }
  }
  
  /// Format JSON response for display
  String _formatJsonResponse(Map<String, dynamic> data) {
    try {
      const encoder = JsonEncoder.withIndent('  ');
      return encoder.convert(data);
    } catch (e) {
      return data.toString();
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
  
  /// Add error message with localization
  void _addErrorMessage(String error) {
    String localizedError = AppLocalizations.error(_selectedLanguage);
    final errorMessage = ChatMessage(
      text: '❌ $localizedError: ${_translateErrorMessage(error)}',
      sender: MessageSender.system,
      timestamp: DateTime.now(),
    );
    _messages.add(errorMessage);
    _isLoading = false;
    notifyListeners();
  }
  
  /// Translate error messages based on selected language
  String _translateErrorMessage(String error) {
    if (error.contains('Failed to get response')) {
      return AppLocalizations.translate('server_error', _selectedLanguage);
    } else if (error.contains('network') || error.contains('connection')) {
      return AppLocalizations.translate('network_error', _selectedLanguage);
    } else if (error.contains('timeout')) {
      return AppLocalizations.translate('timeout_error', _selectedLanguage);
    } else if (error.contains('processing')) {
      return AppLocalizations.translate('server_error', _selectedLanguage);
    } else {
      return AppLocalizations.translate('something_went_wrong', _selectedLanguage);
    }
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
