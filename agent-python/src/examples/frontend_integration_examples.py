"""
Frontend Integration Examples for Agricultural AI Assistant
Description: Examples showing how frontend should integrate with the WebSocket server
"""

# Example 1: Basic WebSocket connection and message sending
websocket_example_js = """
// Frontend JavaScript Example for WebSocket Integration

class AgriculturalChatClient {
    constructor(userId, serverUrl = 'ws://localhost:8000') {
        this.userId = userId;
        this.serverUrl = serverUrl;
        this.websocket = null;
        this.messageHandlers = {};
    }

    connect() {
        return new Promise((resolve, reject) => {
            try {
                this.websocket = new WebSocket(`${this.serverUrl}/ws/${this.userId}`);
                
                this.websocket.onopen = (event) => {
                    console.log('🔗 Connected to Agricultural AI Assistant');
                    resolve(true);
                };
                
                this.websocket.onmessage = (event) => {
                    try {
                        const data = JSON.parse(event.data);
                        this.handleMessage(data);
                    } catch (error) {
                        console.error('❌ Failed to parse message:', error);
                    }
                };
                
                this.websocket.onclose = (event) => {
                    console.log('🔌 Disconnected from server');
                };
                
                this.websocket.onerror = (error) => {
                    console.error('❌ WebSocket error:', error);
                    reject(error);
                };
                
            } catch (error) {
                reject(error);
            }
        });
    }

    sendQuery(query, language = 'hi', location = null, additionalContext = {}) {
        if (!this.websocket || this.websocket.readyState !== WebSocket.OPEN) {
            console.error('❌ WebSocket not connected');
            return false;
        }

        const message = {
            raw_query: query,
            language: language,
            location: location,
            additional_context: additionalContext
        };

        try {
            this.websocket.send(JSON.stringify(message));
            console.log('📤 Query sent:', query);
            return true;
        } catch (error) {
            console.error('❌ Failed to send message:', error);
            return false;
        }
    }

    handleMessage(data) {
        const messageType = data.type || 'unknown';
        
        switch (messageType) {
            case 'connection_established':
                console.log('✅ Connection established:', data.message);
                break;
                
            case 'message_received':
                console.log('📨 Message acknowledged:', data.message);
                break;
                
            case 'status_update':
                console.log('⏳ Processing status:', data.status, data.details?.stage);
                break;
                
            case 'agricultural_response':
                this.handleAgriculturalResponse(data);
                break;
                
            case 'error':
            case 'validation_error':
            case 'server_error':
                console.error('❌ Error:', data.message);
                break;
                
            default:
                console.log('📩 Unknown message type:', data);
        }
    }

    handleAgriculturalResponse(data) {
        console.log('🌾 Agricultural response received');
        
        if (data.success) {
            const responseData = data.data;
            
            // Display the response in your UI
            const response = {
                query: responseData.query,
                location: responseData.location,
                intents: responseData.detected_intents,
                advice: responseData.translated_response || responseData.final_advice,
                explanation: responseData.translated_explanation || responseData.explanation,
                processingTime: data.processing_time,
                timestamp: data.timestamp
            };
            
            // Call your UI update function
            this.updateChatUI(response);
            
        } else {
            console.error('❌ Query processing failed:', data.error);
            this.showError(data.error);
        }
    }

    updateChatUI(response) {
        // Implement your UI update logic here
        console.log('💡 Advice:', response.advice);
        console.log('📍 Location:', response.location);
        console.log('🎯 Intents:', response.intents.join(', '));
    }

    showError(error) {
        // Implement your error display logic here
        console.error('Error to display:', error);
    }

    disconnect() {
        if (this.websocket) {
            this.websocket.close();
        }
    }
}

// Usage Example
const chatClient = new AgriculturalChatClient('user123');

// Connect to server
chatClient.connect().then(() => {
    console.log('Ready to send queries!');
    
    // Send a query
    chatClient.sendQuery(
        'मिट्टी का विश्लेषण कैसे करें?',
        'hi',
        'Maharashtra',
        { crop_type: 'wheat', farm_size: '2 acres' }
    );
});
"""

# Example 2: React component integration
react_example = """
// React Component Example

import React, { useState, useEffect, useRef } from 'react';

const AgriculturalChat = ({ userId }) => {
    const [messages, setMessages] = useState([]);
    const [inputValue, setInputValue] = useState('');
    const [isConnected, setIsConnected] = useState(false);
    const [isProcessing, setIsProcessing] = useState(false);
    const wsRef = useRef(null);

    useEffect(() => {
        connectWebSocket();
        return () => {
            if (wsRef.current) {
                wsRef.current.close();
            }
        };
    }, [userId]);

    const connectWebSocket = () => {
        const ws = new WebSocket(`ws://localhost:8000/ws/${userId}`);
        
        ws.onopen = () => {
            setIsConnected(true);
            console.log('Connected to Agricultural AI Assistant');
        };
        
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            handleWebSocketMessage(data);
        };
        
        ws.onclose = () => {
            setIsConnected(false);
            console.log('Disconnected from server');
        };
        
        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            setIsConnected(false);
        };
        
        wsRef.current = ws;
    };

    const handleWebSocketMessage = (data) => {
        switch (data.type) {
            case 'connection_established':
                addMessage('system', data.message);
                break;
                
            case 'message_received':
                setIsProcessing(true);
                break;
                
            case 'status_update':
                // Update processing status
                break;
                
            case 'agricultural_response':
                setIsProcessing(false);
                if (data.success) {
                    const advice = data.data.translated_response || data.data.final_advice;
                    addMessage('assistant', advice);
                } else {
                    addMessage('error', `Error: ${data.error}`);
                }
                break;
                
            case 'error':
                setIsProcessing(false);
                addMessage('error', data.message);
                break;
        }
    };

    const addMessage = (type, content) => {
        const newMessage = {
            id: Date.now(),
            type: type,
            content: content,
            timestamp: new Date()
        };
        setMessages(prev => [...prev, newMessage]);
    };

    const sendMessage = () => {
        if (!inputValue.trim() || !isConnected || isProcessing) return;
        
        const message = {
            raw_query: inputValue,
            language: 'hi'
        };
        
        wsRef.current.send(JSON.stringify(message));
        addMessage('user', inputValue);
        setInputValue('');
    };

    return (
        <div className="agricultural-chat">
            <div className="chat-header">
                <h3>🌾 Agricultural AI Assistant</h3>
                <div className={`status ${isConnected ? 'connected' : 'disconnected'}`}>
                    {isConnected ? '🟢 Connected' : '🔴 Disconnected'}
                </div>
            </div>
            
            <div className="messages">
                {messages.map(message => (
                    <div key={message.id} className={`message ${message.type}`}>
                        <div className="content">{message.content}</div>
                        <div className="timestamp">
                            {message.timestamp.toLocaleTimeString()}
                        </div>
                    </div>
                ))}
                {isProcessing && (
                    <div className="message processing">
                        <div className="content">🔄 Processing your query...</div>
                    </div>
                )}
            </div>
            
            <div className="input-area">
                <input
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                    placeholder="अपना कृषि प्रश्न यहाँ लिखें..."
                    disabled={!isConnected || isProcessing}
                />
                <button 
                    onClick={sendMessage}
                    disabled={!isConnected || isProcessing || !inputValue.trim()}
                >
                    Send
                </button>
            </div>
        </div>
    );
};

export default AgriculturalChat;
"""

# Example 3: Message format examples
message_formats = {
    "frontend_to_server": {
        "basic_query": {
            "raw_query": "What is the weather forecast for next week?",
            "language": "hi"
        },
        "query_with_location": {
            "raw_query": "मिट्टी का विश्लेषण कैसे करें?",
            "language": "hi",
            "location": "Maharashtra"
        },
        "query_with_context": {
            "raw_query": "What government schemes are available for farmers?",
            "language": "en",
            "location": "Punjab",
            "additional_context": {
                "farm_size": "2 acres",
                "crop_type": "wheat",
                "farmer_type": "small"
            }
        }
    },
    
    "server_to_frontend": {
        "connection_established": {
            "type": "connection_established",
            "message": "आपका स्वागत है! कृषि सलाहकार सेवा में।",
            "user_id": "user123",
            "timestamp": "2025-08-12T16:30:00Z"
        },
        "message_received": {
            "type": "message_received",
            "message": "आपका प्रश्न प्राप्त हुआ है। कृपया प्रतीक्षा करें...",
            "query": "मिट्टी का विश्लेषण कैसे करें?",
            "timestamp": "2025-08-12T16:30:01Z"
        },
        "status_update": {
            "type": "status_update",
            "status": "processing",
            "timestamp": "2025-08-12T16:30:02Z",
            "details": {
                "stage": "analyzing_query"
            }
        },
        "agricultural_response": {
            "type": "agricultural_response",
            "message_id": "msg-123",
            "user_id": "user123",
            "query": "मिट्टी का विश्लेषण कैसे करें?",
            "success": True,
            "processing_time": 15.5,
            "timestamp": "2025-08-12T16:30:15Z",
            "data": {
                "query": "मिट्टी का विश्लेषण कैसे करें?",
                "location": "Maharashtra",
                "language": "hi",
                "detected_intents": ["soil"],
                "final_advice": "मिट्टी का विश्लेषण करने के लिए...",
                "translated_response": "मिट्टी की जांच के लिए नमूना लें...",
                "explanation": "मिट्टी की गुणवत्ता जानना जरूरी है..."
            }
        },
        "error": {
            "type": "error",
            "message": "अमान्य JSON डेटा। कृपया सही फॉर्मेट में भेजें।",
            "timestamp": "2025-08-12T16:30:00Z"
        }
    }
}

# Example 4: Flutter/Dart integration
flutter_example = """
// Flutter WebSocket Integration Example

import 'dart:convert';
import 'dart:io';
import 'package:web_socket_channel/web_socket_channel.dart';

class AgriculturalChatService {
  WebSocketChannel? _channel;
  final String userId;
  final String serverUrl;
  Function(Map<String, dynamic>)? onMessage;
  Function(bool)? onConnectionChange;

  AgriculturalChatService({
    required this.userId,
    this.serverUrl = 'ws://localhost:8000',
    this.onMessage,
    this.onConnectionChange,
  });

  Future<bool> connect() async {
    try {
      _channel = WebSocketChannel.connect(
        Uri.parse('$serverUrl/ws/$userId'),
      );

      _channel!.stream.listen(
        (message) {
          try {
            final data = jsonDecode(message);
            onMessage?.call(data);
          } catch (e) {
            print('Error parsing message: $e');
          }
        },
        onDone: () {
          onConnectionChange?.call(false);
        },
        onError: (error) {
          print('WebSocket error: $error');
          onConnectionChange?.call(false);
        },
      );

      onConnectionChange?.call(true);
      return true;
    } catch (e) {
      print('Connection failed: $e');
      return false;
    }
  }

  void sendQuery({
    required String query,
    String language = 'hi',
    String? location,
    Map<String, dynamic>? additionalContext,
  }) {
    if (_channel == null) return;

    final message = {
      'raw_query': query,
      'language': language,
      if (location != null) 'location': location,
      if (additionalContext != null) 'additional_context': additionalContext,
    };

    _channel!.sink.add(jsonEncode(message));
  }

  void disconnect() {
    _channel?.sink.close();
    _channel = null;
  }
}

// Usage in Flutter widget
class ChatScreen extends StatefulWidget {
  @override
  _ChatScreenState createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  late AgriculturalChatService _chatService;
  final TextEditingController _messageController = TextEditingController();
  final List<ChatMessage> _messages = [];
  bool _isConnected = false;
  bool _isProcessing = false;

  @override
  void initState() {
    super.initState();
    _chatService = AgriculturalChatService(
      userId: 'flutter-user-${DateTime.now().millisecondsSinceEpoch}',
      onMessage: _handleMessage,
      onConnectionChange: (connected) {
        setState(() {
          _isConnected = connected;
        });
      },
    );
    _connectToServer();
  }

  Future<void> _connectToServer() async {
    await _chatService.connect();
  }

  void _handleMessage(Map<String, dynamic> data) {
    setState(() {
      switch (data['type']) {
        case 'agricultural_response':
          _isProcessing = false;
          if (data['success'] == true) {
            final responseData = data['data'];
            final advice = responseData['translated_response'] ?? 
                          responseData['final_advice'] ?? 
                          'कोई सलाह उपलब्ध नहीं';
            _addMessage(ChatMessage(
              content: advice,
              isUser: false,
              timestamp: DateTime.now(),
            ));
          }
          break;
        case 'message_received':
          _isProcessing = true;
          break;
        case 'error':
          _isProcessing = false;
          _addMessage(ChatMessage(
            content: 'Error: ${data['message']}',
            isUser: false,
            timestamp: DateTime.now(),
            isError: true,
          ));
          break;
      }
    });
  }

  void _addMessage(ChatMessage message) {
    setState(() {
      _messages.add(message);
    });
  }

  void _sendMessage() {
    if (_messageController.text.trim().isEmpty || !_isConnected || _isProcessing) {
      return;
    }

    final message = _messageController.text.trim();
    _addMessage(ChatMessage(
      content: message,
      isUser: true,
      timestamp: DateTime.now(),
    ));

    _chatService.sendQuery(query: message);
    _messageController.clear();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('🌾 कृषि सहायक'),
        backgroundColor: Colors.green,
        actions: [
          Icon(_isConnected ? Icons.wifi : Icons.wifi_off),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final message = _messages[index];
                return ChatMessageWidget(message: message);
              },
            ),
          ),
          if (_isProcessing)
            Padding(
              padding: EdgeInsets.all(8.0),
              child: Row(
                children: [
                  CircularProgressIndicator(),
                  SizedBox(width: 8),
                  Text('प्रोसेसिंग हो रही है...'),
                ],
              ),
            ),
          Padding(
            padding: EdgeInsets.all(8.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _messageController,
                    decoration: InputDecoration(
                      hintText: 'अपना कृषि प्रश्न यहाँ लिखें...',
                      border: OutlineInputBorder(),
                    ),
                    onSubmitted: (_) => _sendMessage(),
                    enabled: _isConnected && !_isProcessing,
                  ),
                ),
                SizedBox(width: 8),
                IconButton(
                  icon: Icon(Icons.send),
                  onPressed: _sendMessage,
                  color: Colors.green,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _chatService.disconnect();
    _messageController.dispose();
    super.dispose();
  }
}

class ChatMessage {
  final String content;
  final bool isUser;
  final DateTime timestamp;
  final bool isError;

  ChatMessage({
    required this.content,
    required this.isUser,
    required this.timestamp,
    this.isError = false,
  });
}

class ChatMessageWidget extends StatelessWidget {
  final ChatMessage message;

  const ChatMessageWidget({Key? key, required this.message}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: EdgeInsets.symmetric(vertical: 4, horizontal: 8),
      child: Row(
        mainAxisAlignment: message.isUser 
            ? MainAxisAlignment.end 
            : MainAxisAlignment.start,
        children: [
          Container(
            constraints: BoxConstraints(
              maxWidth: MediaQuery.of(context).size.width * 0.8,
            ),
            padding: EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: message.isError 
                  ? Colors.red[100]
                  : message.isUser 
                      ? Colors.blue[100] 
                      : Colors.green[100],
              borderRadius: BorderRadius.circular(12),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  message.content,
                  style: TextStyle(fontSize: 16),
                ),
                SizedBox(height: 4),
                Text(
                  DateFormat('HH:mm').format(message.timestamp),
                  style: TextStyle(fontSize: 12, color: Colors.grey[600]),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
"""

if __name__ == "__main__":
    print("🌾 Frontend Integration Examples for Agricultural AI Assistant")
    print("=" * 70)
    print("This file contains examples for:")
    print("1. JavaScript WebSocket integration")
    print("2. React component integration") 
    print("3. Message format specifications")
    print("4. Flutter/Dart integration")
    print("=" * 70)
    print("Check the source code for detailed implementation examples.")
