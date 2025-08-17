
const express = require('express');

module.exports.welcomeAPIMessage = (req, res) => {
   res.send(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Agentic API</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                color: white;
            }
            .container {
                text-align: center;
                padding: 2rem;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
                border: 1px solid rgba(255, 255, 255, 0.18);
                max-width: 600px;
            }
            h1 {
                font-size: 3rem;
                margin-bottom: 1rem;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .subtitle {
                font-size: 1.5rem;
                margin-bottom: 2rem;
                opacity: 0.9;
            }
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1rem;
                margin-top: 2rem;
            }
            .feature {
                background: rgba(255, 255, 255, 0.1);
                padding: 1rem;
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            .api-status {
                background: #4CAF50;
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 20px;
                display: inline-block;
                margin-top: 1rem;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Welcome to Agentic API</h1>
            <p class="subtitle">Your Intelligent Agricultural Assistant Backend</p>
            <div class="api-status">✅ API Status: Online</div>
            
            <div class="features">
                <div class="feature">
                    <h3>🌾 Crop Management</h3>
                    <p>Smart recommendations for optimal crop health</p>
                </div>
                <div class="feature">
                    <h3>💰 Market Insights</h3>
                    <p>Real-time pricing and market analysis</p>
                </div>
                <div class="feature">
                    <h3>🌡️ Weather Intelligence</h3>
                    <p>Advanced weather predictions and alerts</p>
                </div>
                <div class="feature">
                    <h3>🔬 Soil Analysis</h3>
                    <p>Comprehensive soil health monitoring</p>
                </div>
            </div>
            
            <p style="margin-top: 2rem; opacity: 0.8;">
                Powered by AI • Built for Farmers • Capital One Hackathon 2025
            </p>
        </div>
    </body>
    </html>
  `);
};