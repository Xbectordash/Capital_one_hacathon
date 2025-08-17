# 📱 Flutter App Integration Guide - FarmMate AI

Complete guide to integrate your Flutter app with FarmMate AI backend services.

## 🚀 Quick Overview

**Backend Services:**
- **Production API**: `https://farmmate-backend.onrender.com`
- **AI Service**: `https://farmmate-ai.onrender.com` 
- **WebSocket**: `wss://farmmate-backend.onrender.com/socket.io/`

## 📋 Prerequisites

```yaml
dependencies:
  flutter: 
    sdk: flutter
  http: ^1.1.0                    # HTTP requests
  socket_io_client: ^2.0.3       # WebSocket connection
  provider: ^6.1.1               # State management
  shared_preferences: ^2.2.2     # Local storage
```

## 🔧 Step 1: Add Dependencies

Add to your `pubspec.yaml`:

```yaml
dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.2
  
  # Network & API
  http: ^1.1.0
  socket_io_client: ^2.0.3
  dio: ^5.3.2                    # Alternative HTTP client
  
  # State Management
  provider: ^6.1.1
  riverpod: ^2.4.9               # Alternative state management
  
  # Storage
  shared_preferences: ^2.2.2
  
  # UI Enhancements
  flutter_markdown: ^0.6.18     # For formatted responses
  loading_animation_widget: ^1.2.0
  
  # Permissions
  permission_handler: ^11.0.1
  
dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^2.0.0
```

## 🌐 Step 2: API Service Setup

Create `lib/services/api_service.dart`:

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = 'https://farmmate-backend.onrender.com';
  static const String aiBaseUrl = 'https://farmmate-ai.onrender.com';
  
  // HTTP Headers
  static Map<String, String> get headers => {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  };

  // Health Check
  static Future<bool> checkHealth() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/health'),
        headers: headers,
      ).timeout(Duration(seconds: 10));
      
      return response.statusCode == 200;
    } catch (e) {
      print('Health check failed: $e');
      return false;
    }
  }

  // Send Agricultural Query (HTTP)
  static Future<Map<String, dynamic>?> sendQuery({
    required String query,
    required String userId,
    String language = 'hi',
    String location = 'India',
  }) async {
    try {
      final body = {
        'user_id': userId,
        'raw_query': query,
        'language': language,
        'location': location,
      };

      final response = await http.post(
        Uri.parse('$aiBaseUrl/chat'),
        headers: headers,
        body: jsonEncode(body),
      ).timeout(Duration(seconds: 30));

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        print('Query failed: ${response.statusCode}');
        return null;
      }
    } catch (e) {
      print('Query error: $e');
      return null;
    }
  }

  // Get Comprehensive Advice
  static Future<Map<String, dynamic>?> getComprehensiveAdvice({
    required String query,
    required String userId,
    String language = 'hi',
    String location = 'India',
  }) async {
    try {
      final body = {
        'user_id': userId,
        'raw_query': query,
        'language': language,
        'location': location,
      };

      final response = await http.post(
        Uri.parse('$aiBaseUrl/chat/comprehensive'),
        headers: headers,
        body: jsonEncode(body),
      ).timeout(Duration(seconds: 45));

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
      return null;
    } catch (e) {
      print('Comprehensive query error: $e');
      return null;
    }
  }
}
```

## 🔌 Step 3: WebSocket Service

Create `lib/services/websocket_service.dart`:

```dart
import 'dart:convert';
import 'package:socket_io_client/socket_io_client.dart' as IO;
import 'package:flutter/foundation.dart';

class WebSocketService extends ChangeNotifier {
  IO.Socket? _socket;
  bool _isConnected = false;
  String _status = 'Disconnected';
  String? _lastResponse;
  bool _isLoading = false;

  // Getters
  bool get isConnected => _isConnected;
  String get status => _status;
  String? get lastResponse => _lastResponse;
  bool get isLoading => _isLoading;

  // Connect to WebSocket
  Future<void> connect(String userId) async {
    try {
      _socket = IO.io('https://farmmate-backend.onrender.com', 
        IO.OptionBuilder()
          .setTransports(['websocket'])
          .enableAutoConnect()
          .setQuery({'userId': userId})
          .build()
      );

      _socket!.onConnect((_) {
        _isConnected = true;
        _status = 'Connected';
        notifyListeners();
        print('🔌 Connected to FarmMate AI');
      });

      _socket!.onDisconnect((_) {
        _isConnected = false;
        _status = 'Disconnected';
        _isLoading = false;
        notifyListeners();
        print('🔌 Disconnected from FarmMate AI');
      });

      // Listen for AI status updates
      _socket!.on('ai_status', (data) {
        _status = data['message'] ?? 'Processing...';
        _isLoading = true;
        notifyListeners();
        print('📡 Status: $_status');
      });

      // Listen for AI responses
      _socket!.on('ai_response', (data) {
        _lastResponse = data['message'];
        _isLoading = false;
        _status = 'Response received';
        notifyListeners();
        print('🤖 Response received');
      });

      // Listen for errors
      _socket!.on('error', (data) {
        _status = 'Error: ${data['message']}';
        _isLoading = false;
        notifyListeners();
        print('❌ Error: ${data['message']}');
      });

      _socket!.connect();
    } catch (e) {
      _status = 'Connection failed: $e';
      notifyListeners();
      print('❌ Connection error: $e');
    }
  }

  // Send query via WebSocket
  void sendQuery({
    required String query,
    String language = 'hi',
    String location = 'India',
  }) {
    if (_socket != null && _isConnected) {
      _isLoading = true;
      _status = 'Sending query...';
      _lastResponse = null;
      notifyListeners();

      final data = {
        'query': query,
        'language': language,
        'location': location,
      };

      _socket!.emit('user_query', data);
      print('📤 Query sent: $query');
    } else {
      _status = 'Not connected';
      notifyListeners();
    }
  }

  // Disconnect
  void disconnect() {
    _socket?.disconnect();
    _socket?.dispose();
    _socket = null;
    _isConnected = false;
    _status = 'Disconnected';
    _isLoading = false;
    notifyListeners();
  }

  @override
  void dispose() {
    disconnect();
    super.dispose();
  }
}
```

## 🎨 Step 4: UI Components

Create `lib/screens/farm_chat_screen.dart`:

```dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:loading_animation_widget/loading_animation_widget.dart';
import '../services/websocket_service.dart';

class FarmChatScreen extends StatefulWidget {
  @override
  _FarmChatScreenState createState() => _FarmChatScreenState();
}

class _FarmChatScreenState extends State<FarmChatScreen> {
  final TextEditingController _messageController = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  List<ChatMessage> _messages = [];

  @override
  void initState() {
    super.initState();
    _connectToService();
  }

  void _connectToService() {
    final webSocketService = Provider.of<WebSocketService>(context, listen: false);
    webSocketService.connect('flutter_user_${DateTime.now().millisecondsSinceEpoch}');
  }

  void _sendMessage() {
    if (_messageController.text.trim().isEmpty) return;

    final message = _messageController.text.trim();
    
    // Add user message to chat
    setState(() {
      _messages.add(ChatMessage(
        text: message,
        isUser: true,
        timestamp: DateTime.now(),
      ));
    });

    // Send to AI
    final webSocketService = Provider.of<WebSocketService>(context, listen: false);
    webSocketService.sendQuery(query: message);

    _messageController.clear();
    _scrollToBottom();
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('🌾 FarmMate AI'),
        backgroundColor: Colors.green[700],
        elevation: 0,
      ),
      body: Column(
        children: [
          // Status Bar
          Consumer<WebSocketService>(
            builder: (context, service, child) {
              return Container(
                width: double.infinity,
                padding: EdgeInsets.all(8),
                color: service.isConnected ? Colors.green[100] : Colors.red[100],
                child: Row(
                  children: [
                    Icon(
                      service.isConnected ? Icons.circle : Icons.circle_outlined,
                      color: service.isConnected ? Colors.green : Colors.red,
                      size: 12,
                    ),
                    SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        service.status,
                        style: TextStyle(fontSize: 12),
                      ),
                    ),
                    if (service.isLoading)
                      LoadingAnimationWidget.staggeredDotsWave(
                        color: Colors.green,
                        size: 20,
                      ),
                  ],
                ),
              );
            },
          ),

          // Chat Messages
          Expanded(
            child: Consumer<WebSocketService>(
              builder: (context, service, child) {
                // Add AI response to messages if available
                if (service.lastResponse != null && 
                    (_messages.isEmpty || !_messages.last.text.contains(service.lastResponse!))) {
                  WidgetsBinding.instance.addPostFrameCallback((_) {
                    setState(() {
                      _messages.add(ChatMessage(
                        text: service.lastResponse!,
                        isUser: false,
                        timestamp: DateTime.now(),
                      ));
                    });
                    _scrollToBottom();
                  });
                }

                return ListView.builder(
                  controller: _scrollController,
                  padding: EdgeInsets.all(16),
                  itemCount: _messages.length,
                  itemBuilder: (context, index) {
                    final message = _messages[index];
                    return _buildMessageBubble(message);
                  },
                );
              },
            ),
          ),

          // Input Field
          Container(
            padding: EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.white,
              boxShadow: [
                BoxShadow(
                  offset: Offset(0, -2),
                  blurRadius: 4,
                  color: Colors.black.withOpacity(0.1),
                ),
              ],
            ),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _messageController,
                    decoration: InputDecoration(
                      hintText: 'अपना कृषि प्रश्न पूछें...',
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(24),
                      ),
                      contentPadding: EdgeInsets.symmetric(
                        horizontal: 16,
                        vertical: 12,
                      ),
                    ),
                    maxLines: null,
                    onSubmitted: (_) => _sendMessage(),
                  ),
                ),
                SizedBox(width: 8),
                Consumer<WebSocketService>(
                  builder: (context, service, child) {
                    return FloatingActionButton(
                      onPressed: service.isConnected && !service.isLoading 
                          ? _sendMessage 
                          : null,
                      child: Icon(Icons.send),
                      mini: true,
                      backgroundColor: service.isConnected 
                          ? Colors.green[700] 
                          : Colors.grey,
                    );
                  },
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMessageBubble(ChatMessage message) {
    return Padding(
      padding: EdgeInsets.symmetric(vertical: 4),
      child: Row(
        mainAxisAlignment: message.isUser 
            ? MainAxisAlignment.end 
            : MainAxisAlignment.start,
        children: [
          if (!message.isUser) ...[
            CircleAvatar(
              backgroundColor: Colors.green[700],
              child: Icon(Icons.agriculture, color: Colors.white),
              radius: 16,
            ),
            SizedBox(width: 8),
          ],
          Flexible(
            child: Container(
              padding: EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: message.isUser 
                    ? Colors.blue[600] 
                    : Colors.grey[200],
                borderRadius: BorderRadius.circular(16),
              ),
              child: message.isUser
                  ? Text(
                      message.text,
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 14,
                      ),
                    )
                  : MarkdownBody(
                      data: message.text,
                      styleSheet: MarkdownStyleSheet(
                        p: TextStyle(fontSize: 14),
                        code: TextStyle(
                          backgroundColor: Colors.grey[300],
                          fontSize: 12,
                        ),
                      ),
                    ),
            ),
          ),
          if (message.isUser) ...[
            SizedBox(width: 8),
            CircleAvatar(
              backgroundColor: Colors.blue[600],
              child: Icon(Icons.person, color: Colors.white),
              radius: 16,
            ),
          ],
        ],
      ),
    );
  }

  @override
  void dispose() {
    _messageController.dispose();
    _scrollController.dispose();
    super.dispose();
  }
}

class ChatMessage {
  final String text;
  final bool isUser;
  final DateTime timestamp;

  ChatMessage({
    required this.text,
    required this.isUser,
    required this.timestamp,
  });
}
```

## 📱 Step 5: Main App Setup

Update your `lib/main.dart`:

```dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'services/websocket_service.dart';
import 'screens/farm_chat_screen.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => WebSocketService(),
      child: MaterialApp(
        title: 'FarmMate AI',
        theme: ThemeData(
          primarySwatch: Colors.green,
          fontFamily: 'Roboto',
        ),
        home: FarmChatScreen(),
        debugShowCheckedModeBanner: false,
      ),
    );
  }
}
```

## 🔒 Step 6: Permissions (Android)

Add to `android/app/src/main/AndroidManifest.xml`:

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
```

## 🌐 Step 7: Network Security (Android)

Create `android/app/src/main/res/xml/network_security_config.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="true">farmmate-backend.onrender.com</domain>
        <domain includeSubdomains="true">farmmate-ai.onrender.com</domain>
    </domain-config>
</network-security-config>
```

And add to AndroidManifest.xml:

```xml
<application
    android:networkSecurityConfig="@xml/network_security_config"
    ...>
```

## 🚀 Step 8: Testing

```dart
// Test HTTP API
final response = await ApiService.sendQuery(
  query: 'मेरी गेहूं की फसल में कीड़े लग गए हैं',
  userId: 'test_user_123',
  language: 'hi',
  location: 'राजस्थान',
);

print('Response: $response');
```

## 📊 Step 9: Advanced Features

### A. Add Offline Support
```dart
class OfflineService {
  static const String CACHE_KEY = 'farmmate_cache';
  
  static Future<void> saveResponse(String query, Map<String, dynamic> response) async {
    final prefs = await SharedPreferences.getInstance();
    final cache = prefs.getString(CACHE_KEY) ?? '{}';
    final cacheMap = jsonDecode(cache);
    cacheMap[query] = response;
    await prefs.setString(CACHE_KEY, jsonEncode(cacheMap));
  }
  
  static Future<Map<String, dynamic>?> getResponse(String query) async {
    final prefs = await SharedPreferences.getInstance();
    final cache = prefs.getString(CACHE_KEY) ?? '{}';
    final cacheMap = jsonDecode(cache);
    return cacheMap[query];
  }
}
```

### B. Add Voice Input
```dart
dependencies:
  speech_to_text: ^6.6.0
  
// Implementation
class VoiceInput extends StatefulWidget {
  @override
  _VoiceInputState createState() => _VoiceInputState();
}
```

## 🎯 Step 10: Sample Queries for Testing

```dart
final testQueries = [
  'मेरी गेहूं की फसल में कीड़े लग गए हैं, क्या करूं?',
  'बारिश के मौसम में कौन सी फसल लगाऊं?',
  'मिट्टी की जांच कैसे करूं?',
  'आज गेहूं का भाव क्या है?',
  'मेरे खेत की मिट्टी में नाइट्रोजन की कमी है',
];
```

## 🔧 Troubleshooting

**Common Issues:**

1. **Connection Timeout:**
   - Increase timeout duration
   - Check internet connectivity
   - Verify API endpoints

2. **WebSocket Disconnection:**
   - Implement auto-reconnect
   - Handle network state changes

3. **JSON Parsing Errors:**
   - Add try-catch blocks
   - Validate response format

## 📱 Complete Integration Checklist

- ✅ Add dependencies
- ✅ Setup API service
- ✅ Configure WebSocket
- ✅ Create UI components
- ✅ Handle permissions
- ✅ Test connectivity
- ✅ Add error handling
- ✅ Implement offline support

## 🎉 Ready to Go!

Your Flutter app is now ready to connect with FarmMate AI! 

**Production URLs:**
- Backend: `https://farmmate-backend.onrender.com`
- AI Service: `https://farmmate-ai.onrender.com`

**Test it with:** "मेरी फसल के लिए आज कौन सा काम करूं?"

Happy Farming! 🌾📱
