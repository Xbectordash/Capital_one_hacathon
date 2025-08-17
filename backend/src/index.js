const express = require('express')
const { createServer } = require('http')
const router = require('./router/router')
const socketService = require('./services/socketService')

const app = express()
const server = createServer(app)
// Use PORT environment variable for deployment (Render sets this automatically)
const port = process.env.PORT || 5000

// Middleware
app.use(express.json())
app.use('/', router)

// Initialize Socket.IO service
socketService.initialize(server)

// Start server
server.listen(port, '0.0.0.0', () => {
    console.log(`🚀 Express + Socket.IO server running on port ${port}`)
    console.log(`📊 Health check: http://localhost:${port}/health`)
    console.log(`🌐 Welcome page: http://localhost:${port}/`)
    console.log(`🔌 Socket.IO endpoint: http://localhost:${port}`)
    
    // Log the Python server URL being used
    const pythonUrl = process.env.PYTHON_SERVER_URL || 'ws://localhost:8000'
    console.log(`🐍 Connecting to Python server: ${pythonUrl}`)
    
    // Log deployment environment
    const env = process.env.NODE_ENV || 'development'
    console.log(`🌍 Environment: ${env}`)
})