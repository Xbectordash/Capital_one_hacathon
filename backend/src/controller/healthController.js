const socketService = require('../services/socketService')

module.exports.healthCheck = (req, res) => {
    const connectionStats = socketService.getConnectionStats()
    
    res.json({
        status: 'OK',
        timestamp: new Date().toISOString(),
        server: 'Express + Socket.IO Gateway',
        connections: connectionStats.total,
        activeConnections: connectionStats.active,
        pythonServerUrl: process.env.PYTHON_SERVER_URL || 'ws://agent-python:8000',
        ports: {
            express: 5000,
            python: 8000,
            react: 3000
        },
        features: {
            multilingual: true,
            supportedLanguages: ['en', 'hi', 'mr', 'gu', 'pa'],
            realTimeChat: true,
            agriculturalAI: true
        }
    })
}

module.exports.apiStatus = (req, res) => {
    res.json({
        api: 'Agricultural AI Backend',
        version: '1.0.0',
        status: 'online',
        endpoints: {
            health: '/health',
            welcome: '/',
            socketio: 'ws://localhost:5000'
        }
    })
}
