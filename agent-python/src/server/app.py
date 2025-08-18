"""
FastAPI WebSocket Server for Agricultural AI Assistant
Description: Real-time chat server with WebSocket support for agricultural queries
"""
import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional
import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, ValidationError

# Import your agricultural workflow
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Use standard workflow
try:
    from src.graph_arc.graph import workflow
    print("🚀 Using standard workflow")
except ImportError:
    print("❌ Error: Could not import workflow from src.graph_arc.graph")
    raise
from src.utils.loggers import get_logger

# Initialize FastAPI app
app = FastAPI(
    title="Agricultural AI Assistant API",
    description="Real-time WebSocket server for agricultural advisory chat",
    version="1.0.0"
)

# Configure CORS for frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up logging
logger = get_logger("agricultural_server")

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_sessions: Dict[str, Dict] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        self.user_sessions[user_id] = {
            "connected_at": datetime.now(),
            "message_count": 0,
            "last_activity": datetime.now()
        }
        logger.info(f"[WebSocket] User {user_id} connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        if user_id in self.user_sessions:
            del self.user_sessions[user_id]
        logger.info(f"[WebSocket] User {user_id} disconnected. Remaining connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: dict, user_id: str):
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_text(json.dumps(message))
                self.user_sessions[user_id]["last_activity"] = datetime.now()
                return True
            except Exception as e:
                logger.error(f"[WebSocket] Error sending message to {user_id}: {e}")
                self.disconnect(user_id)
                return False
        return False

    async def send_status_update(self, status: str, user_id: str, details: dict = None):
        """Send processing status updates to user"""
        message = {
            "type": "status_update",
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "details": details or {}
        }
        await self.send_personal_message(message, user_id)

    def get_connection_stats(self):
        return {
            "total_connections": len(self.active_connections),
            "connected_users": list(self.active_connections.keys()),
            "total_sessions": len(self.user_sessions)
        }

# Initialize connection manager
manager = ConnectionManager()

# Pydantic models for request validation
class ChatMessage(BaseModel):
    user_id: str
    raw_query: str
    language: Optional[str] = "hi"
    location: Optional[str] = None
    additional_context: Optional[Dict] = None

class ChatResponse(BaseModel):
    message_id: str
    user_id: str
    query: str
    response: Dict
    processing_time: float
    timestamp: str
    success: bool
    error: Optional[str] = None

# Agricultural processing function
async def process_agricultural_query(message: ChatMessage) -> Dict:
    """Process agricultural query through the AI workflow"""
    try:
        logger.info(f"[AgriProcessor] Processing query for user {message.user_id}")
        
        # Prepare initial state
        initial_state = {
            "user_id": message.user_id,
            "raw_query": message.raw_query,
            "language": message.language or "hi",
        }
        
        # Add location if provided
        if message.location:
            initial_state["location"] = message.location
            
        # Add any additional context
        if message.additional_context:
            initial_state.update(message.additional_context)

        # Send status update
        await manager.send_status_update("processing", message.user_id, {"stage": "analyzing_query"})
        
        # Process through workflow (this runs synchronously)
        logger.info("[AgriProcessor] Invoking optimized agricultural workflow")
        start_time_workflow = datetime.now()
        result = workflow.invoke(initial_state)
        workflow_time = (datetime.now() - start_time_workflow).total_seconds()
        
        # Log performance metrics
        logger.info(f"[AgriProcessor] Workflow completed in {workflow_time:.2f}s")
        
        # Send status update
        await manager.send_status_update("processing", message.user_id, {
            "stage": "generating_response", 
            "workflow_time": f"{workflow_time:.2f}s"
        })
        
        # Process result for WebSocket response
        processed_result = {
            "query": result.get('raw_query', ''),
            "location": result.get('location', 'Unknown'),
            "language": result.get('language', 'hi'),
            "detected_intents": result.get('intents', []),
            "agent_results": result.get('agent_results', {}),
            "comprehensive_advice": None,
            "final_advice": None,
            "explanation": None,
            "translated_response": None
        }
        
        # Extract final advice and check if it's comprehensive JSON
        if "decision" in result:
            decision = result["decision"]
            final_advice = decision.get('final_advice', 'No advice available')
            
            # Try to parse final_advice as comprehensive JSON
            try:
                import json
                if isinstance(final_advice, str) and final_advice.strip().startswith('{'):
                    comprehensive_json = json.loads(final_advice)
                    processed_result["comprehensive_advice"] = comprehensive_json
                    processed_result["final_advice"] = comprehensive_json.get("final_advice", "No advice available")
                else:
                    # If not JSON, create a simple structure
                    processed_result["final_advice"] = final_advice
                    processed_result["comprehensive_advice"] = {
                        "final_advice": final_advice,
                        "confidence_score": 0.8
                    }
            except (json.JSONDecodeError, AttributeError) as e:
                logger.warning(f"Failed to parse comprehensive advice as JSON: {e}")
                processed_result["final_advice"] = final_advice
                processed_result["comprehensive_advice"] = {
                    "final_advice": final_advice,
                    "confidence_score": 0.8
                }
            
            processed_result["explanation"] = decision.get('explanation', 'No explanation available')
        
        # Extract translation if available
        if "translation" in result:
            translation = result["translation"]
            print(f"🌐 Processing translation data: {translation}")
            
            # Update response with translated content
            if translation.get('translated_response'):
                processed_result["final_advice"] = translation['translated_response']
                processed_result["response"] = translation['translated_response']
                
            if translation.get('translated_explanation'):
                processed_result["explanation"] = translation['translated_explanation']
            
            # Add translation metadata
            processed_result["translation"] = {
                "target_language": translation.get('target_language', 'hi'),
                "translated_response": translation.get('translated_response', ''),
                "translated_explanation": translation.get('translated_explanation', ''),
                "original_advice": translation.get('original_advice', ''),
                "original_explanation": translation.get('original_explanation', ''),
                "fallback_used": translation.get('fallback_used', False)
            }
            
            logger.info(f"[AgriProcessor] Translation applied for language: {translation.get('target_language', 'hi')}")
        else:
            print("❌ No translation data found in result")
            logger.info("[AgriProcessor] No translation data available")
        
        logger.info(f"[AgriProcessor] Successfully processed query for user {message.user_id}")
        return {
            "success": True,
            "result": processed_result,
            "error": None
        }
        
    except Exception as e:
        logger.error(f"[AgriProcessor] Error processing query for user {message.user_id}: {str(e)}")
        return {
            "success": False,
            "result": None,
            "error": str(e)
        }

# WebSocket endpoint
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    
    # Send welcome message
    welcome_message = {
        "type": "connection_established",
        "message": "आपका स्वागत है! कृषि सलाहकार सेवा में। आप अपने खेती संबंधी प्रश्न पूछ सकते हैं।",
        "user_id": user_id,
        "timestamp": datetime.now().isoformat()
    }
    await manager.send_personal_message(welcome_message, user_id)
    
    try:
        while True:
            # Receive message from WebSocket
            data = await websocket.receive_text()
            logger.info(f"[WebSocket] Received message from user {user_id}")
            
            try:
                # Parse incoming message
                message_data = json.loads(data)
                
                # Validate message using Pydantic
                if "raw_query" not in message_data:
                    raise ValueError("raw_query is required")
                
                message_data["user_id"] = user_id
                chat_message = ChatMessage(**message_data)
                
                # Update session stats
                manager.user_sessions[user_id]["message_count"] += 1
                
                # Send acknowledgment
                ack_message = {
                    "type": "message_received",
                    "message": "आपका प्रश्न प्राप्त हुआ है। कृपया प्रतीक्षा करें...",
                    "query": chat_message.raw_query,
                    "timestamp": datetime.now().isoformat()
                }
                await manager.send_personal_message(ack_message, user_id)
                
                # Process the agricultural query
                start_time = datetime.now()
                result = await process_agricultural_query(chat_message)
                processing_time = (datetime.now() - start_time).total_seconds()
                
                # Create response
                message_id = str(uuid.uuid4())
                response = {
                    "type": "agricultural_response",
                    "message_id": message_id,
                    "user_id": user_id,
                    "query": chat_message.raw_query,
                    "success": result["success"],
                    "processing_time": processing_time,
                    "timestamp": datetime.now().isoformat()
                }
                
                if result["success"]:
                    response["data"] = result["result"]
                    response["message"] = "सफलतापूर्वक प्रोसेस किया गया!"
                else:
                    response["error"] = result["error"]
                    response["message"] = "प्रोसेसिंग में त्रुटि हुई। कृपया पुनः प्रयास करें।"
                
                # Send final response
                await manager.send_personal_message(response, user_id)
                logger.info(f"[WebSocket] Sent response to user {user_id} (processing time: {processing_time:.2f}s)")
                
            except json.JSONDecodeError:
                error_message = {
                    "type": "error",
                    "message": "अमान्य JSON डेटा। कृपया सही फॉर्मेट में भेजें।",
                    "timestamp": datetime.now().isoformat()
                }
                await manager.send_personal_message(error_message, user_id)
                
            except ValidationError as e:
                error_message = {
                    "type": "validation_error",
                    "message": "डेटा वैलिडेशन एरर।",
                    "details": str(e),
                    "timestamp": datetime.now().isoformat()
                }
                await manager.send_personal_message(error_message, user_id)
                
            except Exception as e:
                logger.error(f"[WebSocket] Unexpected error for user {user_id}: {str(e)}")
                error_message = {
                    "type": "server_error",
                    "message": "सर्वर एरर। कृपया बाद में प्रयास करें।",
                    "timestamp": datetime.now().isoformat()
                }
                await manager.send_personal_message(error_message, user_id)
                
    except WebSocketDisconnect:
        logger.info(f"[WebSocket] User {user_id} disconnected")
        manager.disconnect(user_id)

# HTTP endpoints for testing and monitoring

@app.get("/", response_class=HTMLResponse)
async def root():
    """Main landing page with navigation to all features"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🌾 FarmMate AI - Agricultural Intelligence Platform</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .main-container {
                text-align: center;
                max-width: 800px;
                padding: 50px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
            }
            h1 {
                font-size: 4em;
                margin-bottom: 20px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .subtitle {
                font-size: 1.5em;
                margin-bottom: 40px;
                opacity: 0.9;
            }
            .nav-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin: 40px 0;
            }
            .nav-card {
                background: rgba(255, 255, 255, 0.2);
                padding: 30px;
                border-radius: 15px;
                text-decoration: none;
                color: white;
                transition: all 0.3s ease;
                border: 2px solid transparent;
            }
            .nav-card:hover {
                background: rgba(255, 255, 255, 0.3);
                transform: translateY(-5px);
                border-color: rgba(255, 255, 255, 0.5);
            }
            .nav-icon {
                font-size: 3em;
                display: block;
                margin-bottom: 15px;
            }
            .nav-title {
                font-size: 1.3em;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .nav-desc {
                font-size: 0.9em;
                opacity: 0.8;
            }
            .status-bar {
                background: rgba(0, 0, 0, 0.2);
                padding: 20px;
                border-radius: 10px;
                margin-top: 30px;
            }
            .status-item {
                display: inline-block;
                margin: 0 20px;
            }
            .status-indicator {
                width: 12px;
                height: 12px;
                background: #4CAF50;
                border-radius: 50%;
                display: inline-block;
                margin-right: 8px;
                animation: pulse 2s infinite;
            }
            @keyframes pulse {
                0% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7); }
                70% { box-shadow: 0 0 0 10px rgba(76, 175, 80, 0); }
                100% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0); }
            }
        </style>
    </head>
    <body>
        <div class="main-container">
            <h1>🌾 FarmMate AI</h1>
            <p class="subtitle">Intelligent Agricultural Assistant Platform</p>
            
            <div class="nav-grid">
                <a href="/demo" class="nav-card">
                    <span class="nav-icon">🎯</span>
                    <div class="nav-title">Demo Showcase</div>
                    <div class="nav-desc">Explore FarmMate capabilities and see example conversations</div>
                </a>
                
                <a href="/test-page" class="nav-card">
                    <span class="nav-icon">🧪</span>
                    <div class="nav-title">Live WebSocket Test</div>
                    <div class="nav-desc">Real-time chat interface for testing AI responses</div>
                </a>
                
                <a href="/api-test" class="nav-card">
                    <span class="nav-icon">🔬</span>
                    <div class="nav-title">API Testing Suite</div>
                    <div class="nav-desc">Test HTTP endpoints and API functionality</div>
                </a>
                
                <a href="/docs" class="nav-card">
                    <span class="nav-icon">📚</span>
                    <div class="nav-title">API Documentation</div>
                    <div class="nav-desc">Complete API reference and integration guide</div>
                </a>
                
                <a href="/health" class="nav-card">
                    <span class="nav-icon">💚</span>
                    <div class="nav-title">Health Status</div>
                    <div class="nav-desc">Server health and connection statistics</div>
                </a>
                
                <a href="/stats" class="nav-card">
                    <span class="nav-icon">📊</span>
                    <div class="nav-title">Server Statistics</div>
                    <div class="nav-desc">Real-time server metrics and usage data</div>
                </a>
            </div>
            
            <div class="status-bar">
                <div class="status-item">
                    <span class="status-indicator"></span>
                    Server Status: Online
                </div>
                <div class="status-item">
                    <span class="status-indicator"></span>
                    AI Models: Ready
                </div>
                <div class="status-item">
                    <span class="status-indicator"></span>
                    WebSocket: Available
                </div>
            </div>
            
            <p style="margin-top: 30px; opacity: 0.7;">
                Built for Capital One Hackathon 2025 • Empowering Farmers with AI
            </p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "connections": manager.get_connection_stats()
    }

@app.get("/stats")
async def get_stats():
    """Get server statistics"""
    return {
        "server_stats": manager.get_connection_stats(),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/test-page", response_class=HTMLResponse)
async def test_page():
    """Simple test page for WebSocket testing"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🌾 FarmMate AI Test Page</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
            }
            .container {
                background: rgba(255, 255, 255, 0.1);
                padding: 30px;
                border-radius: 15px;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
            }
            h1 {
                text-align: center;
                color: #fff;
                margin-bottom: 30px;
                font-size: 2.5em;
            }
            .chat-container {
                background: rgba(255, 255, 255, 0.9);
                color: #333;
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
                max-height: 400px;
                overflow-y: auto;
            }
            .input-group {
                display: flex;
                gap: 10px;
                margin: 20px 0;
            }
            input[type="text"] {
                flex: 1;
                padding: 12px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                background: rgba(255, 255, 255, 0.9);
            }
            button {
                padding: 12px 24px;
                background: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
                transition: background 0.3s;
            }
            button:hover {
                background: #45a049;
            }
            button:disabled {
                background: #cccccc;
                cursor: not-allowed;
            }
            .status {
                padding: 10px;
                margin: 10px 0;
                border-radius: 5px;
                font-weight: bold;
            }
            .status.connected {
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            .status.disconnected {
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
            .message {
                margin: 10px 0;
                padding: 10px;
                border-radius: 8px;
            }
            .message.user {
                background: #e3f2fd;
                text-align: right;
            }
            .message.bot {
                background: #f1f8e9;
            }
            .api-info {
                background: rgba(255, 255, 255, 0.1);
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
            }
            .api-info h3 {
                margin-top: 0;
            }
            .api-endpoint {
                background: rgba(0, 0, 0, 0.2);
                padding: 10px;
                border-radius: 5px;
                font-family: monospace;
                margin: 5px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌾 FarmMate AI Assistant</h1>
            
            <div class="api-info">
                <h3>📡 API Information</h3>
                <div class="api-endpoint">WebSocket: ws://localhost:8000/ws/{user_id}</div>
                <div class="api-endpoint">Health: /health</div>
                <div class="api-endpoint">API Docs: /docs</div>
                <div class="api-endpoint">Chat HTTP: POST /chat</div>
            </div>

            <div id="status" class="status disconnected">❌ Disconnected</div>
            
            <div class="input-group">
                <input type="text" id="userIdInput" placeholder="Enter User ID (e.g., farmer123)" value="test-user-123">
                <button onclick="connect()" id="connectBtn">Connect</button>
                <button onclick="disconnect()" id="disconnectBtn" disabled>Disconnect</button>
            </div>

            <div class="chat-container" id="chatContainer">
                <div class="message bot">Welcome! Connect to start chatting with FarmMate AI.</div>
            </div>

            <div class="input-group">
                <input type="text" id="messageInput" placeholder="अपना सवाल यहाँ लिखें... (Type your farming question here)" disabled>
                <button onclick="sendMessage()" id="sendBtn" disabled>Send</button>
            </div>

            <div class="api-info">
                <h3>🧪 Sample Questions (Hindi)</h3>
                <button onclick="sendSample('मेरी गेहूं की फसल में कीड़े लग गए हैं, क्या करूं?')" class="sample-btn">Pest Problem</button>
                <button onclick="sendSample('बारिश के मौसम में कौन सी फसल उगाऊं?')" class="sample-btn">Crop Suggestion</button>
                <button onclick="sendSample('मिट्टी की जांच कैसे करूं?')" class="sample-btn">Soil Testing</button>
            </div>
        </div>

        <script>
            let ws = null;
            let userId = null;

            function updateStatus(message, isConnected) {
                const status = document.getElementById('status');
                status.textContent = message;
                status.className = 'status ' + (isConnected ? 'connected' : 'disconnected');
            }

            function addMessage(content, isUser = false) {
                const chatContainer = document.getElementById('chatContainer');
                const messageDiv = document.createElement('div');
                messageDiv.className = 'message ' + (isUser ? 'user' : 'bot');
                messageDiv.innerHTML = content;
                chatContainer.appendChild(messageDiv);
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }

            function connect() {
                userId = document.getElementById('userIdInput').value.trim();
                if (!userId) {
                    alert('Please enter a User ID');
                    return;
                }

                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                const wsUrl = `${protocol}//${window.location.host}/ws/${userId}`;
                
                ws = new WebSocket(wsUrl);
                
                ws.onopen = function(event) {
                    updateStatus('✅ Connected to FarmMate AI', true);
                    document.getElementById('connectBtn').disabled = true;
                    document.getElementById('disconnectBtn').disabled = false;
                    document.getElementById('messageInput').disabled = false;
                    document.getElementById('sendBtn').disabled = false;
                    addMessage('Connected successfully! You can now ask farming questions.');
                };

                ws.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    let messageContent = '';
                    
                    if (data.type === 'connection_established') {
                        messageContent = `🎉 ${data.message}`;
                    } else if (data.type === 'agricultural_response') {
                        if (data.success && data.data) {
                            messageContent = `
                                <strong>🌾 Agricultural Advice:</strong><br>
                                <strong>Query:</strong> ${data.data.query || 'N/A'}<br>
                                <strong>Language:</strong> ${data.data.language || 'N/A'}<br>
                                <strong>Detected Intents:</strong> ${(data.data.detected_intents || []).join(', ') || 'N/A'}<br>
                                <strong>Final Advice:</strong> ${data.data.final_advice || 'N/A'}<br>
                                <strong>Processing Time:</strong> ${data.processing_time?.toFixed(2)}s
                            `;
                        } else {
                            messageContent = `❌ Error: ${data.error || 'Unknown error'}`;
                        }
                    } else if (data.type === 'status_update') {
                        messageContent = `⏳ Status: ${data.status} - ${data.details?.stage || ''}`;
                    } else {
                        messageContent = data.message || JSON.stringify(data);
                    }
                    
                    addMessage(messageContent);
                };

                ws.onclose = function(event) {
                    updateStatus('❌ Disconnected', false);
                    document.getElementById('connectBtn').disabled = false;
                    document.getElementById('disconnectBtn').disabled = true;
                    document.getElementById('messageInput').disabled = true;
                    document.getElementById('sendBtn').disabled = true;
                    addMessage('Connection closed.');
                };

                ws.onerror = function(error) {
                    updateStatus('❌ Connection Error', false);
                    addMessage('WebSocket error: ' + error);
                };
            }

            function disconnect() {
                if (ws) {
                    ws.close();
                }
            }

            function sendMessage() {
                const messageInput = document.getElementById('messageInput');
                const message = messageInput.value.trim();
                
                if (!message || !ws || ws.readyState !== WebSocket.OPEN) {
                    return;
                }

                const messageData = {
                    raw_query: message,
                    language: "hi",
                    location: "India"
                };

                ws.send(JSON.stringify(messageData));
                addMessage(`🧑‍🌾 You: ${message}`, true);
                messageInput.value = '';
            }

            function sendSample(question) {
                if (!ws || ws.readyState !== WebSocket.OPEN) {
                    alert('Please connect first!');
                    return;
                }
                document.getElementById('messageInput').value = question;
                sendMessage();
            }

            // Enter key to send message
            document.getElementById('messageInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });

            // Auto-connect on page load for testing
            window.addEventListener('load', function() {
                setTimeout(connect, 1000);
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/api-test", response_class=HTMLResponse)
async def api_test_page():
    """Static page for testing HTTP API endpoints"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🔬 FarmMate API Testing Suite</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 1000px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #2E8B57 0%, #3CB371 100%);
                color: white;
                min-height: 100vh;
            }
            .container {
                background: rgba(255, 255, 255, 0.1);
                padding: 30px;
                border-radius: 15px;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
            }
            h1 {
                text-align: center;
                color: #fff;
                margin-bottom: 30px;
                font-size: 2.5em;
            }
            .test-section {
                background: rgba(255, 255, 255, 0.9);
                color: #333;
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
            }
            .input-group {
                display: flex;
                gap: 10px;
                margin: 15px 0;
                flex-wrap: wrap;
            }
            input[type="text"], textarea, select {
                flex: 1;
                padding: 12px;
                border: 1px solid #ddd;
                border-radius: 8px;
                font-size: 14px;
                min-width: 200px;
            }
            button {
                padding: 12px 24px;
                background: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 14px;
                transition: background 0.3s;
            }
            button:hover {
                background: #45a049;
            }
            button:disabled {
                background: #cccccc;
                cursor: not-allowed;
            }
            .response-container {
                background: #f5f5f5;
                padding: 15px;
                border-radius: 8px;
                margin: 15px 0;
                max-height: 300px;
                overflow-y: auto;
                border: 1px solid #ddd;
            }
            .endpoint-card {
                border: 1px solid #ddd;
                border-radius: 8px;
                margin: 20px 0;
                overflow: hidden;
            }
            .endpoint-header {
                background: #2E8B57;
                color: white;
                padding: 15px;
                font-weight: bold;
            }
            .endpoint-body {
                padding: 20px;
            }
            .method-badge {
                display: inline-block;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
                margin-right: 10px;
            }
            .method-get { background: #4CAF50; color: white; }
            .method-post { background: #2196F3; color: white; }
            .status-indicator {
                display: inline-block;
                width: 10px;
                height: 10px;
                border-radius: 50%;
                margin-right: 5px;
            }
            .status-success { background: #4CAF50; }
            .status-error { background: #f44336; }
            .status-loading { background: #ff9800; animation: pulse 1s infinite; }
            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.5; }
                100% { opacity: 1; }
            }
            pre {
                background: #f8f8f8;
                padding: 10px;
                border-radius: 4px;
                overflow-x: auto;
                white-space: pre-wrap;
                font-size: 12px;
            }
            .navigation {
                text-align: center;
                margin: 20px 0;
            }
            .navigation a {
                color: white;
                text-decoration: none;
                padding: 10px 20px;
                margin: 0 10px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 20px;
                transition: background 0.3s;
            }
            .navigation a:hover {
                background: rgba(255, 255, 255, 0.3);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔬 FarmMate API Testing Suite</h1>
            
            <div class="navigation">
                <a href="/test-page">WebSocket Test</a>
                <a href="/api-test">API Test</a>
                <a href="/demo">Demo Page</a>
                <a href="/docs">API Docs</a>
                <a href="/health">Health Check</a>
            </div>

            <!-- Health Check Test -->
            <div class="endpoint-card">
                <div class="endpoint-header">
                    <span class="method-badge method-get">GET</span>
                    Health Check - /health
                </div>
                <div class="endpoint-body">
                    <button onclick="testHealth()">
                        <span id="health-status" class="status-indicator"></span>
                        Test Health Endpoint
                    </button>
                    <div id="health-response" class="response-container" style="display: none;"></div>
                </div>
            </div>

            <!-- Stats Test -->
            <div class="endpoint-card">
                <div class="endpoint-header">
                    <span class="method-badge method-get">GET</span>
                    Server Statistics - /stats
                </div>
                <div class="endpoint-body">
                    <button onclick="testStats()">
                        <span id="stats-status" class="status-indicator"></span>
                        Get Server Stats
                    </button>
                    <div id="stats-response" class="response-container" style="display: none;"></div>
                </div>
            </div>

            <!-- Chat HTTP Test -->
            <div class="endpoint-card">
                <div class="endpoint-header">
                    <span class="method-badge method-post">POST</span>
                    Chat Endpoint - /chat
                </div>
                <div class="endpoint-body">
                    <div class="input-group">
                        <input type="text" id="chat-user-id" placeholder="User ID" value="test-user-api">
                        <input type="text" id="chat-query" placeholder="Enter your farming question in Hindi" value="मेरी गेहूं की फसल में कीड़े लग गए हैं">
                    </div>
                    <div class="input-group">
                        <select id="chat-language">
                            <option value="hi">Hindi (हिंदी)</option>
                            <option value="en">English</option>
                            <option value="pa">Punjabi</option>
                            <option value="gu">Gujarati</option>
                        </select>
                        <input type="text" id="chat-location" placeholder="Location" value="India">
                    </div>
                    <button onclick="testChat()">
                        <span id="chat-status" class="status-indicator"></span>
                        Send Chat Message
                    </button>
                    <div id="chat-response" class="response-container" style="display: none;"></div>
                </div>
            </div>

            <!-- Comprehensive Chat Test -->
            <div class="endpoint-card">
                <div class="endpoint-header">
                    <span class="method-badge method-post">POST</span>
                    Comprehensive Chat - /chat/comprehensive
                </div>
                <div class="endpoint-body">
                    <div class="input-group">
                        <input type="text" id="comp-user-id" placeholder="User ID" value="test-user-comp">
                        <textarea id="comp-query" placeholder="Enter detailed farming question" rows="3">मैं राजस्थान में हूँ और मेरे पास 5 एकड़ जमीन है। बारिश के मौसम में कौन सी फसल लगाऊं जो अच्छा मुनाफा दे?</textarea>
                    </div>
                    <button onclick="testComprehensive()">
                        <span id="comp-status" class="status-indicator"></span>
                        Get Comprehensive Advice
                    </button>
                    <div id="comp-response" class="response-container" style="display: none;"></div>
                </div>
            </div>

            <!-- Sample Questions -->
            <div class="test-section">
                <h3>🧪 Quick Test Questions</h3>
                <button onclick="loadSampleQuestion(1)">🐛 Pest Control</button>
                <button onclick="loadSampleQuestion(2)">🌾 Crop Suggestion</button>
                <button onclick="loadSampleQuestion(3)">🌧️ Weather Advice</button>
                <button onclick="loadSampleQuestion(4)">🌱 Soil Testing</button>
                <button onclick="loadSampleQuestion(5)">💰 Market Prices</button>
            </div>
        </div>

        <script>
            const BASE_URL = window.location.origin;

            function setStatus(elementId, status) {
                const element = document.getElementById(elementId);
                element.className = 'status-indicator status-' + status;
            }

            function showResponse(containerId, data) {
                const container = document.getElementById(containerId);
                container.style.display = 'block';
                container.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            }

            async function testHealth() {
                setStatus('health-status', 'loading');
                try {
                    const response = await fetch(BASE_URL + '/health');
                    const data = await response.json();
                    setStatus('health-status', 'success');
                    showResponse('health-response', data);
                } catch (error) {
                    setStatus('health-status', 'error');
                    showResponse('health-response', {error: error.message});
                }
            }

            async function testStats() {
                setStatus('stats-status', 'loading');
                try {
                    const response = await fetch(BASE_URL + '/stats');
                    const data = await response.json();
                    setStatus('stats-status', 'success');
                    showResponse('stats-response', data);
                } catch (error) {
                    setStatus('stats-status', 'error');
                    showResponse('stats-response', {error: error.message});
                }
            }

            async function testChat() {
                setStatus('chat-status', 'loading');
                try {
                    const payload = {
                        user_id: document.getElementById('chat-user-id').value,
                        raw_query: document.getElementById('chat-query').value,
                        language: document.getElementById('chat-language').value,
                        location: document.getElementById('chat-location').value
                    };

                    const response = await fetch(BASE_URL + '/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(payload)
                    });

                    const data = await response.json();
                    setStatus('chat-status', response.ok ? 'success' : 'error');
                    showResponse('chat-response', data);
                } catch (error) {
                    setStatus('chat-status', 'error');
                    showResponse('chat-response', {error: error.message});
                }
            }

            async function testComprehensive() {
                setStatus('comp-status', 'loading');
                try {
                    const payload = {
                        user_id: document.getElementById('comp-user-id').value,
                        raw_query: document.getElementById('comp-query').value,
                        language: "hi",
                        location: "India"
                    };

                    const response = await fetch(BASE_URL + '/chat/comprehensive', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(payload)
                    });

                    const data = await response.json();
                    setStatus('comp-status', response.ok ? 'success' : 'error');
                    showResponse('comp-response', data);
                } catch (error) {
                    setStatus('comp-status', 'error');
                    showResponse('comp-response', {error: error.message});
                }
            }

            function loadSampleQuestion(type) {
                const questions = {
                    1: "मेरी गेहूं की फसल में कीड़े लग गए हैं, क्या करूं?",
                    2: "बारिश के मौसम में कौन सी फसल उगाऊं?",
                    3: "अगले सप्ताह बारिश होगी या नहीं?",
                    4: "मिट्टी की जांच कैसे करूं?",
                    5: "आज गेहूं का भाव क्या है?"
                };
                document.getElementById('chat-query').value = questions[type];
                document.getElementById('comp-query').value = questions[type];
            }

            // Auto-test health on page load
            window.addEventListener('load', function() {
                setTimeout(testHealth, 1000);
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/demo", response_class=HTMLResponse)
async def demo_page():
    """Demo page showcasing FarmMate capabilities"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🌾 FarmMate AI - Demo Showcase</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 50%, #45B7D1 100%);
                color: #333;
                min-height: 100vh;
            }
            .hero {
                text-align: center;
                padding: 50px 20px;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
            }
            .hero h1 {
                font-size: 3.5em;
                color: white;
                margin-bottom: 20px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .hero p {
                font-size: 1.5em;
                color: white;
                margin-bottom: 30px;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            .features-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 30px;
                margin: 50px 0;
            }
            .feature-card {
                background: white;
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                transition: transform 0.3s ease;
            }
            .feature-card:hover {
                transform: translateY(-10px);
            }
            .feature-icon {
                font-size: 3em;
                margin-bottom: 15px;
                display: block;
            }
            .feature-title {
                font-size: 1.5em;
                font-weight: bold;
                margin-bottom: 15px;
                color: #2E8B57;
            }
            .demo-section {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                padding: 40px;
                margin: 40px 0;
                box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
            }
            .chat-demo {
                background: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
                border-left: 5px solid #4ECDC4;
            }
            .question {
                background: #e3f2fd;
                padding: 15px;
                border-radius: 10px;
                margin: 10px 0;
                border-left: 4px solid #2196F3;
            }
            .answer {
                background: #f1f8e9;
                padding: 15px;
                border-radius: 10px;
                margin: 10px 0;
                border-left: 4px solid #4CAF50;
            }
            .navigation {
                text-align: center;
                margin: 30px 0;
            }
            .navigation a {
                color: white;
                text-decoration: none;
                padding: 15px 30px;
                margin: 0 10px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 25px;
                transition: all 0.3s;
                display: inline-block;
                font-weight: bold;
            }
            .navigation a:hover {
                background: rgba(255, 255, 255, 0.3);
                transform: scale(1.05);
            }
            .stats-bar {
                display: flex;
                justify-content: space-around;
                background: rgba(255, 255, 255, 0.1);
                padding: 30px;
                border-radius: 15px;
                margin: 30px 0;
            }
            .stat-item {
                text-align: center;
                color: white;
            }
            .stat-number {
                font-size: 2.5em;
                font-weight: bold;
                display: block;
            }
            .stat-label {
                font-size: 1.1em;
                margin-top: 5px;
            }
            .live-demo-btn {
                background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
                color: white;
                border: none;
                padding: 20px 40px;
                font-size: 1.2em;
                border-radius: 30px;
                cursor: pointer;
                transition: all 0.3s;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            }
            .live-demo-btn:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 20px rgba(0,0,0,0.3);
            }
        </style>
    </head>
    <body>
        <div class="hero">
            <h1>🌾 FarmMate AI</h1>
            <p>Intelligent Agricultural Assistant for Modern Farmers</p>
            <button class="live-demo-btn" onclick="window.open('/test-page', '_blank')">
                🚀 Try Live Demo
            </button>
        </div>

        <div class="navigation">
            <a href="/test-page">🧪 Live Test</a>
            <a href="/api-test">🔬 API Testing</a>
            <a href="/demo">🎯 Demo Page</a>
            <a href="/docs">📚 API Docs</a>
        </div>

        <div class="stats-bar">
            <div class="stat-item">
                <span class="stat-number">5+</span>
                <span class="stat-label">AI Agents</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">7</span>
                <span class="stat-label">Languages</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">24/7</span>
                <span class="stat-label">Available</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">Real-time</span>
                <span class="stat-label">Responses</span>
            </div>
        </div>

        <div class="container">
            <div class="features-grid">
                <div class="feature-card">
                    <span class="feature-icon">🐛</span>
                    <div class="feature-title">Pest & Disease Control</div>
                    <p>AI-powered diagnosis and treatment recommendations for crop diseases and pest infestations. Get instant solutions with image analysis and symptom matching.</p>
                </div>

                <div class="feature-card">
                    <span class="feature-icon">🌧️</span>
                    <div class="feature-title">Weather Advisory</div>
                    <p>Real-time weather updates, forecasts, and farming recommendations based on weather patterns. Plan your farming activities with precision.</p>
                </div>

                <div class="feature-card">
                    <span class="feature-icon">🌱</span>
                    <div class="feature-title">Crop Recommendations</div>
                    <p>Smart crop selection based on soil type, weather, season, and market conditions. Maximize your yield and profit with data-driven suggestions.</p>
                </div>

                <div class="feature-card">
                    <span class="feature-icon">🌍</span>
                    <div class="feature-title">Soil Analysis</div>
                    <p>Comprehensive soil health assessment and improvement recommendations. Upload soil test reports or describe soil conditions for analysis.</p>
                </div>

                <div class="feature-card">
                    <span class="feature-icon">💰</span>
                    <div class="feature-title">Market Prices</div>
                    <p>Live market rates from major mandis across India. Get real-time pricing information to make informed selling decisions.</p>
                </div>

                <div class="feature-card">
                    <span class="feature-icon">🏛️</span>
                    <div class="feature-title">Government Schemes</div>
                    <p>Complete information about agricultural subsidies, loans, and government schemes. Find relevant schemes and application procedures.</p>
                </div>
            </div>

            <div class="demo-section">
                <h2 style="color: #2E8B57; text-align: center; margin-bottom: 30px;">🎭 Live Chat Examples</h2>

                <div class="chat-demo">
                    <div class="question">
                        <strong>🧑‍🌾 Farmer:</strong> "मेरी गेहूं की फसल में पीले धब्बे आ गए हैं, क्या करूं?"
                    </div>
                    <div class="answer">
                        <strong>🤖 FarmMate AI:</strong> "यह गेहूं की पत्तियों में जंग (Rust) की समस्या हो सकती है। तुरंत प्रोपिकोनाजोल 25% EC का छिड़काव करें। मौसम में नमी अधिक हो तो 15 दिन बाद दोबारा छिड़काव करें। इसके अलावा नाइट्रोजन की मात्रा कम करें और पोटाश बढ़ाएं।"
                    </div>
                </div>

                <div class="chat-demo">
                    <div class="question">
                        <strong>🧑‍🌾 Farmer:</strong> "राजस्थान में अगले महीने कौन सी फसल लगाऊं?"
                    </div>
                    <div class="answer">
                        <strong>🤖 FarmMate AI:</strong> "राजस्थान में मार्च में रबी फसल की कटाई का समय है। गर्मियों के लिए आप मूंग, तिल, ग्वार या चारा फसलें लगा सकते हैं। सिंचाई की व्यवस्था अच्छी हो तो बाजरा भी एक अच्छा विकल्प है। मिट्टी टेस्ट कराकर उर्वरक की मात्रा तय करें।"
                    </div>
                </div>

                <div class="chat-demo">
                    <div class="question">
                        <strong>🧑‍🌾 Farmer:</strong> "आज गेहूं का भाव क्या चल रहा है?"
                    </div>
                    <div class="answer">
                        <strong>🤖 FarmMate AI:</strong> "आज मुख्य मंडियों में गेहूं का भाव: दिल्ली - ₹2,250/क्विंटल, जयपुर - ₹2,200/क्विंटल, लुधियाना - ₹2,300/क्विंटल। पिछले सप्ताह से 50-70 रुपये की बढ़त है। अच्छी गुणवत्ता के लिए प्रीमियम मिल रहा है।"
                    </div>
                </div>
            </div>

            <div class="demo-section">
                <h2 style="color: #2E8B57; text-align: center;">🚀 Try It Yourself</h2>
                <p style="text-align: center; font-size: 1.2em;">
                    Connect with our AI assistant in real-time through WebSocket or test our HTTP APIs.
                    Available in Hindi, English, Punjabi, Gujarati, and more regional languages.
                </p>
                <div style="text-align: center; margin-top: 30px;">
                    <button class="live-demo-btn" onclick="window.open('/test-page', '_blank')">
                        🌐 WebSocket Chat Demo
                    </button>
                    <button class="live-demo-btn" onclick="window.open('/api-test', '_blank')" style="margin-left: 20px;">
                        🔬 HTTP API Testing
                    </button>
                </div>
            </div>
        </div>

        <div style="text-align: center; padding: 50px; background: rgba(0,0,0,0.8); color: white; margin-top: 50px;">
            <h3>🌟 Built for Capital One Hackathon 2025</h3>
            <p>Empowering farmers with AI-driven agricultural intelligence</p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/chat")
async def chat_endpoint(message: ChatMessage):
    """HTTP endpoint for testing (non-WebSocket)"""
    try:
        start_time = datetime.now()
        result = await process_agricultural_query(message)
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return ChatResponse(
            message_id=str(uuid.uuid4()),
            user_id=message.user_id,
            query=message.raw_query,
            response=result["result"] if result["success"] else {},
            processing_time=processing_time,
            timestamp=datetime.now().isoformat(),
            success=result["success"],
            error=result["error"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/comprehensive")
async def comprehensive_chat_endpoint(message: ChatMessage):
    """HTTP endpoint that returns comprehensive agricultural advice in structured format"""
    try:
        start_time = datetime.now()
        result = await process_agricultural_query(message)
        processing_time = (datetime.now() - start_time).total_seconds()
        
        response_data = {
            "message_id": str(uuid.uuid4()),
            "user_id": message.user_id,
            "query": message.raw_query,
            "processing_time": processing_time,
            "timestamp": datetime.now().isoformat(),
            "success": result["success"]
        }
        
        if result["success"]:
            # Include comprehensive advice if available
            if result["result"].get("comprehensive_advice"):
                response_data["comprehensive_advice"] = result["result"]["comprehensive_advice"]
            response_data["data"] = result["result"]
        else:
            response_data["error"] = result["error"]
        
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
