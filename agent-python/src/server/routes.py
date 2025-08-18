"""
API Routes for Agricultural AI Assistant
Description: Additional REST API routes for the agricultural chat application
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional, Dict
from datetime import datetime
import uuid

from server.app import manager, ChatMessage, process_agricultural_query

# Create router
router = APIRouter(prefix="/api/v1", tags=["Agricultural AI"])

@router.get("/queries/{user_id}")
async def get_user_queries(user_id: str):
    """Get query history for a specific user"""
    try:
        if user_id in manager.user_sessions:
            session = manager.user_sessions[user_id]
            return {
                "user_id": user_id,
                "session_info": {
                    "connected_at": session["connected_at"],
                    "message_count": session["message_count"],
                    "last_activity": session["last_activity"]
                },
                "is_connected": user_id in manager.active_connections
            }
        else:
            raise HTTPException(status_code=404, detail="User session not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/process")
async def process_query(message: ChatMessage):
    """Process agricultural query via REST API"""
    try:
        result = await process_agricultural_query(message)
        
        if result["success"]:
            return {
                "message_id": str(uuid.uuid4()),
                "success": True,
                "data": result["result"],
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=500, detail=result["error"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/intents")
async def get_supported_intents():
    """Get list of supported agricultural intents"""
    return {
        "supported_intents": [
            "weather",
            "soil",
            "market",
            "crop_health",
            "government_schemes"
        ],
        "description": {
            "weather": "Weather forecasts and irrigation advice",
            "soil": "Soil analysis and crop recommendations",
            "market": "Market prices and selling suggestions",
            "crop_health": "Pest and disease diagnosis",
            "government_schemes": "Government subsidies and schemes"
        }
    }

@router.get("/agents/status")
async def get_agents_status():
    """Get status of all agricultural agents"""
    return {
        "agents": {
            "weather_agent": {"status": "active", "description": "Weather forecasting and irrigation advice"},
            "soil_agent": {"status": "active", "description": "Soil analysis and crop recommendations"},
            "market_agent": {"status": "active", "description": "Market price intelligence"},
            "crop_health_agent": {"status": "active", "description": "Pest and disease monitoring"},
            "government_schemes_agent": {"status": "active", "description": "Government schemes and subsidies"}
        },
        "total_agents": 5,
        "timestamp": datetime.now().isoformat()
    }

@router.post("/feedback")
async def submit_feedback(
    user_id: str,
    message_id: str,
    rating: int,
    feedback: Optional[str] = None
):
    """Submit feedback for agricultural advice"""
    if rating < 1 or rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    
    # In a real implementation, you would save this to a database
    feedback_data = {
        "feedback_id": str(uuid.uuid4()),
        "user_id": user_id,
        "message_id": message_id,
        "rating": rating,
        "feedback": feedback,
        "timestamp": datetime.now().isoformat()
    }
    
    return {
        "message": "Feedback submitted successfully",
        "feedback_id": feedback_data["feedback_id"]
    }

@router.get("/languages")
async def get_supported_languages():
    """Get list of supported languages"""
    return {
        "supported_languages": {
            "hi": "Hindi (हिंदी)",
            "en": "English",
            "mr": "Marathi (मराठी)",
            "pa": "Punjabi (ਪੰਜਾਬੀ)",
            "gu": "Gujarati (ગુજરાતી)",
            "ta": "Tamil (தமிழ்)",
            "te": "Telugu (తెలుగు)",
            "kn": "Kannada (ಕನ್ನಡ)"
        },
        "default_language": "hi",
        "note": "Currently optimized for Hindi and English"
    }

@router.get("/test/sample-queries")
async def get_sample_queries():
    """Get sample queries for testing"""
    return {
        "sample_queries": {
            "weather": [
                "What is the weather forecast for next week?",
                "अगले सप्ताह का मौसम पूर्वानुमान क्या है?",
                "Should I irrigate my crops today?"
            ],
            "soil": [
                "What crops should I plant in clay soil?",
                "मिट्टी का विश्लेषण कैसे करें?",
                "My soil has low nitrogen, what should I do?"
            ],
            "market": [
                "What are current wheat prices in Delhi mandi?",
                "गेहूं की वर्तमान कीमत क्या है?",
                "When should I sell my rice crop?"
            ],
            "crop_health": [
                "My wheat plants have yellow leaves, what's wrong?",
                "कपास में कीट लगा है, क्या करें?",
                "How to prevent fungal diseases in tomatoes?"
            ],
            "government_schemes": [
                "What government schemes are available for small farmers?",
                "PM-KISAN scheme के लिए कैसे अप्लाई करें?",
                "Which subsidies can I get for organic farming?"
            ]
        }
    }
