const express = require('express')
const { createServer } = require('http')
const router = require('./router/router')
const socketService = require('./services/socketService')

const app = express()
const server = createServer(app)
const port = 5000

// Middleware
app.use(express.json())
app.use('/', router)

// Initialize Socket.IO service
socketService.initialize(server)

// Start server
server.listen(port, () => {
    console.log(`🚀 Express + Socket.IO server running on port ${port}`)
    console.log(`📊 Health check: http://localhost:${port}/health`)
    console.log(`🌐 Welcome page: http://localhost:${port}/`)
    console.log(`🔌 Socket.IO endpoint: http://localhost:${port}`)
    console.log(`🐍 Connecting to Python server: ws://localhost:8000`)
})