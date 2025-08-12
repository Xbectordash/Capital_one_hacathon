# 🌾 Agricultural AI Assistant - WebSocket Server

Real-time chat server for agricultural advisory with AI-powered recommendations.

## 🚀 Quick Start

### 1. Start the Server

```bash
cd agent-python/src
python -m uvicorn server.app:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Test the Connection

Visit: http://localhost:8000/test-page

### 3. API Documentation

Visit: http://localhost:8000/docs

## 💬 WebSocket Usage

### Connect

```javascript
const ws = new WebSocket("ws://localhost:8000/ws/your-user-id");
```

### Send Query

```javascript
ws.send(
  JSON.stringify({
    raw_query: "मिट्टी का विश्लेषण कैसे करें?",
    language: "hi",
    location: "Maharashtra",
  })
);
```

### Receive Response

```javascript
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === "agricultural_response" && data.success) {
    console.log("Advice:", data.data.translated_response);
  }
};
```

## 📱 Frontend Integration

### React Example

```jsx
import { useState, useEffect } from "react";

const AgriculturalChat = ({ userId }) => {
  const [ws, setWs] = useState(null);
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const websocket = new WebSocket(`ws://localhost:8000/ws/${userId}`);
    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      handleMessage(data);
    };
    setWs(websocket);

    return () => websocket.close();
  }, [userId]);

  const sendQuery = (query) => {
    if (ws) {
      ws.send(
        JSON.stringify({
          raw_query: query,
          language: "hi",
        })
      );
    }
  };

  // ... rest of component
};
```

### Flutter Example

```dart
import 'package:web_socket_channel/web_socket_channel.dart';

class AgriculturalChatService {
    WebSocketChannel? _channel;

    Future<void> connect(String userId) async {
        _channel = WebSocketChannel.connect(
            Uri.parse('ws://localhost:8000/ws/$userId'),
        );

        _channel!.stream.listen((message) {
            final data = jsonDecode(message);
            handleMessage(data);
        });
    }

    void sendQuery(String query) {
        _channel!.sink.add(jsonEncode({
            'raw_query': query,
            'language': 'hi',
        }));
    }
}
```

## 🎯 Supported Features

- **Real-time Chat:** WebSocket-based communication
- **Agricultural AI:** Weather, soil, market, crop health, government schemes
- **Multi-language:** Hindi, English, and more
- **Location-aware:** State and district-specific advice
- **Status Updates:** Real-time processing updates

## 📊 API Endpoints

- `ws://localhost:8000/ws/{user_id}` - WebSocket chat
- `GET /health` - Server health check
- `GET /stats` - Connection statistics
- `POST /chat` - HTTP chat endpoint
- `GET /test-page` - Interactive test page

## 🧪 Testing

### Test Client

```bash
python test_websocket_client.py
```

### Sample Queries

- "What is the weather forecast for next week?"
- "मिट्टी का विश्लेषण कैसे करें?"
- "What government schemes are available for farmers?"
- "My wheat crop has yellow leaves, what should I do?"

## 🔧 Message Formats

### Frontend to Server

```json
{
  "raw_query": "Your agricultural question",
  "language": "hi",
  "location": "State/District",
  "additional_context": {
    "farm_size": "2 acres",
    "crop_type": "wheat"
  }
}
```

### Server to Frontend

```json
{
  "type": "agricultural_response",
  "success": true,
  "data": {
    "query": "Original query",
    "location": "Detected location",
    "detected_intents": ["soil", "weather"],
    "translated_response": "Hindi response",
    "final_advice": "English advice",
    "explanation": "Detailed explanation"
  },
  "processing_time": 15.5,
  "timestamp": "2025-08-12T16:30:15Z"
}
```

## 🚀 Production Ready

- ✅ Error handling and validation
- ✅ Connection management
- ✅ User session tracking
- ✅ Logging and monitoring
- ✅ CORS support for web apps
- ✅ Health checks and statistics

---

**Server Status: 🟢 RUNNING**  
**Ready for:** Web apps, Mobile apps, Chat interfaces  
**AI Agents:** 5 agricultural experts ready to help farmers!
