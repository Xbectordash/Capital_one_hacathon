#!/usr/bin/env python3
"""
FarmMate AI Simple Web Application
A lightweight web interface for the FarmMate agricultural assistant with CSV-based soil analysis.
"""

import sys
import os
import json
from pathlib import Path
from flask import Flask, request, jsonify, render_template_string
import threading
import time

# Add the src directory to Python path
project_root = Path(__file__).resolve().parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

try:
    from src.graph_arc.graph import workflow
    from src.data.soil_plugins import get_soil_data_from_csv, fetch_soil_data_by_location
    from src.data.weather_plugins import fetch_weather_data
    from src.utils.loggers import get_logger
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Make sure you're running from the agent-python directory and all dependencies are installed.")
    sys.exit(1)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'farmmate_secret_key_2024'

# Configure logging
logger = get_logger("simple_web")

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FarmMate AI - Agricultural Assistant</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        .header h1 {
            color: #2c5530;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header .subtitle {
            color: #666;
            font-size: 1.2em;
            margin-bottom: 20px;
        }
        
        .features {
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .feature {
            background: #4CAF50;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
        }
        
        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        .card h2 {
            color: #2c5530;
            margin-bottom: 20px;
            font-size: 1.5em;
        }
        
        .query-form {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        .input-group {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }
        
        .input-group label {
            font-weight: 600;
            color: #555;
        }
        
        .input-group input,
        .input-group textarea {
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s;
        }
        
        .input-group input:focus,
        .input-group textarea:focus {
            outline: none;
            border-color: #4CAF50;
        }
        
        .btn {
            padding: 12px 24px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            font-weight: 600;
            transition: background 0.3s;
        }
        
        .btn:hover {
            background: #45a049;
        }
        
        .btn:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        
        .quick-actions {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        
        .quick-btn {
            padding: 15px;
            background: #f8f9fa;
            border: 2px solid #ddd;
            border-radius: 10px;
            cursor: pointer;
            text-align: center;
            transition: all 0.3s;
        }
        
        .quick-btn:hover {
            background: #e9ecef;
            border-color: #4CAF50;
        }
        
        .response-section {
            grid-column: span 2;
        }
        
        .response-content {
            background: #f8f9fa;
            border-left: 4px solid #4CAF50;
            padding: 20px;
            border-radius: 8px;
            margin-top: 15px;
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
            line-height: 1.6;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
            color: #666;
        }
        
        .loading .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #4CAF50;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .examples {
            margin-top: 20px;
        }
        
        .example {
            background: #e8f5e8;
            padding: 10px;
            border-radius: 5px;
            margin: 5px 0;
            cursor: pointer;
            transition: background 0.3s;
        }
        
        .example:hover {
            background: #d4edda;
        }
        
        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
            }
            
            .response-section {
                grid-column: span 1;
            }
            
            .header h1 {
                font-size: 2em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌾 FarmMate AI 🌾</h1>
            <p class="subtitle">Your Intelligent Agricultural Assistant</p>
            <div class="features">
                <span class="feature">🧪 CSV Soil Analysis</span>
                <span class="feature">🌤️ Weather Integration</span>
                <span class="feature">🌱 Crop Recommendations</span>
                <span class="feature">💰 Market Intelligence</span>
                <span class="feature">🏛️ Government Schemes</span>
            </div>
        </div>
        
        <div class="main-content">
            <div class="card">
                <h2>🤖 Ask FarmMate</h2>
                <form class="query-form" id="queryForm">
                    <div class="input-group">
                        <label for="location">📍 Location (Optional)</label>
                        <input type="text" id="location" name="location" 
                               placeholder="e.g., Delhi, Punjab, Maharashtra">
                    </div>
                    
                    <div class="input-group">
                        <label for="query">💬 Your Question</label>
                        <textarea id="query" name="query" rows="4" 
                                  placeholder="Ask about crops, soil, weather, farming techniques..."></textarea>
                    </div>
                    
                    <button type="submit" class="btn" id="submitBtn">
                        🚀 Get Agricultural Advice
                    </button>
                </form>
                
                <div class="quick-actions">
                    <div class="quick-btn" onclick="quickQuery('soil analysis for Delhi')">
                        🧪 Quick Soil Analysis
                    </div>
                    <div class="quick-btn" onclick="quickQuery('weather forecast for farming')">
                        🌤️ Weather Check
                    </div>
                    <div class="quick-btn" onclick="quickQuery('best crops for this season')">
                        🌱 Crop Suggestions
                    </div>
                    <div class="quick-btn" onclick="quickQuery('government schemes for farmers')">
                        🏛️ Government Schemes
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h2>📚 Example Queries</h2>
                <div class="examples">
                    <div class="example" onclick="setQuery('What crops should I grow in Punjab during winter?')">
                        "What crops should I grow in Punjab during winter?"
                    </div>
                    <div class="example" onclick="setQuery('Soil analysis for black cotton soil in Maharashtra')">
                        "Soil analysis for black cotton soil in Maharashtra"
                    </div>
                    <div class="example" onclick="setQuery('Best organic farming practices for tomatoes')">
                        "Best organic farming practices for tomatoes"
                    </div>
                    <div class="example" onclick="setQuery('Current market prices for wheat')">
                        "Current market prices for wheat"
                    </div>
                    <div class="example" onclick="setQuery('Zinc deficiency in soil, what fertilizer to use?')">
                        "Zinc deficiency in soil, what fertilizer to use?"
                    </div>
                    <div class="example" onclick="setQuery('Irrigation schedule based on weather forecast')">
                        "Irrigation schedule based on weather forecast"
                    </div>
                </div>
            </div>
            
            <div class="card response-section">
                <h2>🎯 FarmMate Response</h2>
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>FarmMate is analyzing your query...</p>
                </div>
                <div class="response-content" id="response">
                    Welcome to FarmMate AI! 🌾
                    
                    Ask me anything about:
                    • Soil analysis and nutrient management
                    • Crop recommendations for your region
                    • Weather-based farming decisions
                    • Market prices and trends
                    • Government schemes and subsidies
                    • Pest and disease management
                    • Irrigation and water management
                    
                    Type your question above and get expert agricultural advice!
                </div>
            </div>
        </div>
    </div>
    
    <script>
        document.getElementById('queryForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const location = document.getElementById('location').value.trim();
            const query = document.getElementById('query').value.trim();
            
            if (!query) {
                alert('Please enter your question!');
                return;
            }
            
            // Show loading
            document.getElementById('loading').style.display = 'block';
            document.getElementById('response').textContent = '';
            document.getElementById('submitBtn').disabled = true;
            document.getElementById('submitBtn').textContent = '⏳ Processing...';
            
            try {
                const response = await fetch('/api/query', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        location: location,
                        query: query
                    })
                });
                
                const data = await response.json();
                
                // Hide loading
                document.getElementById('loading').style.display = 'none';
                
                if (data.success) {
                    document.getElementById('response').textContent = data.response;
                } else {
                    document.getElementById('response').textContent = 
                        'Sorry, there was an error processing your query: ' + data.error;
                }
                
            } catch (error) {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('response').textContent = 
                    'Network error: ' + error.message;
            }
            
            // Reset button
            document.getElementById('submitBtn').disabled = false;
            document.getElementById('submitBtn').textContent = '🚀 Get Agricultural Advice';
        });
        
        function setQuery(exampleQuery) {
            document.getElementById('query').value = exampleQuery;
        }
        
        function quickQuery(query) {
            document.getElementById('query').value = query;
            document.getElementById('queryForm').dispatchEvent(new Event('submit'));
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/query', methods=['POST'])
def handle_query():
    """Handle API queries from the web interface"""
    try:
        data = request.get_json()
        
        if not data or not data.get('query'):
            return jsonify({
                'success': False,
                'error': 'Query is required'
            }), 400
        
        query = data['query'].strip()
        location = data.get('location', '').strip()
        
        # Enhance query with location if provided
        if location and 'location' not in query.lower() and 'in ' not in query.lower():
            enhanced_query = f"{query} in {location}"
        else:
            enhanced_query = query
            
        logger.info(f"Processing web query: {enhanced_query}")
        
        # Create initial state for the workflow
        initial_state = {
            "user_id": "web_user",
            "raw_query": enhanced_query,
            "language": "en"  # Default to English for web
        }
        
        # Process with FarmMate AI workflow
        result = workflow.invoke(initial_state)
        
        # Extract the response from the result
        if result.get("decision"):
            response = result["decision"].get("final_advice", "No advice available")
        else:
            response = "I couldn't process your query. Please try rephrasing it."
        
        return jsonify({
            'success': True,
            'response': response,
            'query': enhanced_query
        })
        
    except Exception as e:
        logger.error(f"Error processing web query: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/soil', methods=['POST'])
def handle_soil_analysis():
    """Handle soil analysis requests"""
    try:
        data = request.get_json()
        location = data.get('location', '').strip()
        
        if not location:
            return jsonify({
                'success': False,
                'error': 'Location is required for soil analysis'
            }), 400
            
        logger.info(f"Processing soil analysis for: {location}")
        
        # Get soil data using CSV-based system
        soil_data = get_soil_data_from_csv(location, "web soil analysis")
        
        return jsonify({
            'success': True,
            'soil_data': soil_data,
            'location': location
        })
        
    except Exception as e:
        logger.error(f"Error in soil analysis: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/weather', methods=['POST'])
def handle_weather():
    """Handle weather requests"""
    try:
        data = request.get_json()
        location = data.get('location', '').strip()
        
        if not location:
            return jsonify({
                'success': False,
                'error': 'Location is required for weather data'
            }), 400
            
        logger.info(f"Processing weather request for: {location}")
        
        # Get weather data
        weather_data = fetch_weather_data(location)
        
        return jsonify({
            'success': True,
            'weather_data': weather_data,
            'location': location
        })
        
    except Exception as e:
        logger.error(f"Error in weather request: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'FarmMate AI Simple Web',
        'version': '1.0.0',
        'features': [
            'CSV-based soil analysis',
            'Weather integration', 
            'Crop recommendations',
            'Market intelligence',
            'Government schemes'
        ]
    })

def run_server(host='127.0.0.1', port=5000, debug=False):
    """Run the Flask server"""
    print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                          🌾 FARMMATE AI WEB 🌾                               ║
║                     Simple Web Interface Starting...                         ║
║                                                                              ║
║  🌐 URL: http://{host}:{port}                                        ║
║  🧪 CSV Soil Analysis Ready                                                  ║
║  🌤️ Weather Integration Active                                               ║
║  🚀 Enhanced Agricultural Intelligence                                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    logger.info(f"Starting FarmMate AI web server on {host}:{port}")
    
    try:
        app.run(host=host, port=port, debug=debug, threaded=True)
    except Exception as e:
        logger.error(f"Failed to start web server: {e}")
        print(f"❌ Failed to start server: {e}")

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='FarmMate AI Simple Web Application')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to (default: 5000)')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    # Check if we're in the right directory
    if not os.path.exists("src"):
        print("❌ Error: Please run this script from the agent-python directory")
        print("Current directory should contain the 'src' folder")
        sys.exit(1)
    
    # Check for Flask
    try:
        import flask
    except ImportError:
        print("❌ Flask is not installed. Install it with: pip install flask")
        sys.exit(1)
    
    run_server(host=args.host, port=args.port, debug=args.debug)

if __name__ == "__main__":
    main()
