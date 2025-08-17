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
    
    # Get port from environment variable (for deployment) or default to 8000
    port = int(os.environ.get("PORT", 8000))
    
    # Start the FastAPI server
    print("🌾 Starting Agricultural AI Assistant Server...")
    print(f"📡 WebSocket endpoint: ws://localhost:{port}/ws/{{user_id}}")
    print(f"🌐 Test page: http://localhost:{port}/test-page")
    print(f"📊 Health check: http://localhost:{port}/health")
    print(f"🔗 API docs: http://localhost:{port}/docs")
    
    # Check if we're in production (disable reload for production)
    reload_mode = os.environ.get("NODE_ENV") != "production"
    
    uvicorn.run(
        "server.app:app",
        host="0.0.0.0",
        port=port,
        reload=reload_mode,
        log_level="info"
    )
