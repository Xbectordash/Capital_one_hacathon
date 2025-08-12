#!/usr/bin/env python3
"""
Server Startup Script for Agricultural AI Assistant
"""
import os
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

if __name__ == "__main__":
    import uvicorn
    
    # Start the FastAPI server
    print("🌾 Starting Agricultural AI Assistant Server...")
    print("📡 WebSocket endpoint: ws://localhost:8000/ws/{user_id}")
    print("🌐 Test page: http://localhost:8000/test-page")
    print("📊 Health check: http://localhost:8000/health")
    print("🔗 API docs: http://localhost:8000/docs")
    
    uvicorn.run(
        "server.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
