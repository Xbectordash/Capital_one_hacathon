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
                if isinstance(final_advice, str) and final_advice.startswith('{'):
                    comprehensive_json = json.loads(final_advice)
                    processed_result["comprehensive_advice"] = comprehensive_json
                    processed_result["final_advice"] = comprehensive_json.get("final_advice", "No advice available")
                else:
                    processed_result["final_advice"] = final_advice
            except (json.JSONDecodeError, AttributeError):
                processed_result["final_advice"] = final_advice
            
            processed_result["explanation"] = decision.get('explanation', 'No explanation available')
        
        # Extract translation if available
        if "translation" in result:
            translation = result["translation"]
            processed_result["translated_response"] = translation.get('translated_response', '')
            processed_result["translated_explanation"] = translation.get('translated_explanation', '')
        
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

@app.get("/")
async def root():
    return {"message": "Agricultural AI Assistant Server", "status": "running"}

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
