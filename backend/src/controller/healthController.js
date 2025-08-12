const socketService = require('../services/socketService')

module.exports.healthCheck = (req, res) => {
    res.json({
        status: 'OK',
        timestamp: new Date().toISOString(),
        server: 'Express + Socket.IO Gateway',
        connections: socketService.getConnectionsCount(),
        pythonServerUrl: 'ws://localhost:8000',
        ports: {
            express: 5000,
            python: 8000,
            react: 3000
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
