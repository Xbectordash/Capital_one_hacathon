#!/usr/bin/env python3
"""
Server Startup Script for Agricultural AI Assistant
"""
import os
import sys
import logging

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def setup_logging():
    """Setup logging configuration for production"""
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )

if __name__ == "__main__":
    # Setup logging first
    setup_logging()
    
    import uvicorn
    
    # Get port from environment variable (for deployment) or default to 8000
    port = int(os.environ.get("PORT", 8000))
    
    # Check if we're in production
    is_production = os.environ.get("NODE_ENV") == "production"
    reload_mode = not is_production
    
    # Start the FastAPI server
    print("🌾 Starting Agricultural AI Assistant Server...")
    print(f"🌍 Environment: {'Production' if is_production else 'Development'}")
    print(f"📡 WebSocket endpoint: ws://localhost:{port}/ws/{{user_id}}")
    print(f"🌐 Test page: http://localhost:{port}/test-page")
    print(f"📊 Health check: http://localhost:{port}/health")
    print(f"🔗 API docs: http://localhost:{port}/docs")
    print(f"🔄 Reload mode: {'Disabled' if is_production else 'Enabled'}")
    
    uvicorn.run(
        "server.app:app",
        host="0.0.0.0",
        port=port,
        reload=reload_mode,
        log_level="info" if is_production else "debug",
        access_log=True
    )
