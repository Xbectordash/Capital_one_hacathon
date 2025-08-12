const { Server } = require('socket.io')
const WebSocket = require('ws')

class SocketService {
    constructor() {
        this.io = null
        this.pythonConnections = new Map()
        // Use environment variable or Docker container name
        this.PYTHON_SERVER_URL = process.env.PYTHON_SERVER_URL || 'ws://agent-python:8000'
    }

    initialize(server) {
        this.io = new Server(server, {
            cors: {
                origin: ["http://localhost:3000", "http://localhost:3001"],
                methods: ["GET", "POST"],
                credentials: true
            }
        })

        this.setupSocketHandlers()
        console.log('🔌 Socket.IO service initialized')
    }

    setupSocketHandlers() {
        this.io.on('connection', (socket) => {
            console.log(`👤 User connected: ${socket.id}`)
            
            socket.on('user_query', async (data) => {
                await this.handleUserQuery(socket, data)
            })
            
            socket.on('disconnect', () => {
                this.handleDisconnect(socket)
            })
        })
    }

    async handleUserQuery(socket, data) {
        const { query, userId = socket.id, language = 'hi' } = data
        console.log(`📝 Received query from ${userId}: ${query}`)
        
        try {
            let pythonWs = this.pythonConnections.get(userId)
            
            if (!pythonWs || pythonWs.readyState !== WebSocket.OPEN) {
                pythonWs = await this.connectToPythonServer(userId, socket, language)
            }
            
            if (!pythonWs) {
                socket.emit('error', { message: 'Failed to connect to AI server' })
                return
            }
            
            const queryData = {
                raw_query: query,
                language: language,
                user_id: userId
            }
            
            pythonWs.send(JSON.stringify(queryData))
            
        } catch (error) {
            console.error(`❌ Error processing query for ${userId}:`, error)
            socket.emit('error', { message: 'Internal server error' })
        }
    }

    handlePythonResponse(socket, message, language) {
        try {
            const response = JSON.parse(message.toString())
            console.log(`📤 Python response type: ${response.type}`)
            
            // Only send final responses to the client, not intermediate status updates
            if (response.type === 'connection_established') {
                console.log('✅ Python connection established')
                return
            }
            
            if (response.type === 'message_received') {
                socket.emit('ai_status', { 
                    message: 'आपका प्रश्न प्राप्त हुआ है। कृपया प्रतीक्षा करें...',
                    status: 'received'
                })
                return
            }
            
            if (response.type === 'status_update') {
                const statusMessages = {
                    'analyzing_query': 'आपके प्रश्न का विश्लेषण हो रहा है...',
                    'generating_response': 'उत्तर तैयार किया जा रहा है...'
                }
                const statusMsg = statusMessages[response.details?.stage] || 'प्रक्रिया जारी है...'
                socket.emit('ai_status', { 
                    message: statusMsg,
                    status: 'processing'
                })
                return
            }
            
            // Handle the final agricultural response
            if (response.type === 'agricultural_response' && response.success && response.data) {
                const data = response.data
                let formattedResponse = ''
                
                if (data.translated_response && language !== 'en') {
                    formattedResponse = data.translated_response
                    if (data.translated_explanation) {
                        formattedResponse += '\n\nविस्तार: ' + data.translated_explanation
                    }
                } else {
                    formattedResponse = data.final_advice || 'No advice available'
                    if (data.explanation) {
                        formattedResponse += '\n\nExplanation: ' + data.explanation
                    }
                }
                
                if (data.location && data.location !== 'Unknown') {
                    formattedResponse += `\n\n📍 स्थान: ${data.location}`
                }
                
                if (data.detected_intents && data.detected_intents.length > 0) {
                    formattedResponse += `\n\n🎯 विषय: ${data.detected_intents.join(', ')}`
                }
                
                socket.emit('ai_response', {
                    message: formattedResponse,
                    success: true,
                    type: 'agricultural_advice',
                    timestamp: new Date().toISOString()
                })
            } else if (response.message) {
                socket.emit('ai_response', {
                    message: response.message,
                    success: response.success !== false,
                    timestamp: new Date().toISOString()
                })
            }
        } catch (error) {
            console.error('Error parsing Python response:', error)
            socket.emit('error', { message: 'Failed to process AI response' })
        }
    }

    async connectToPythonServer(userId, socket, language) {
        try {
            const ws = new WebSocket(`${this.PYTHON_SERVER_URL}/ws/${userId}`)
            
            return new Promise((resolve, reject) => {
                const timeout = setTimeout(() => {
                    reject(new Error('Connection timeout'))
                }, 10000) // 10 second timeout
                
                ws.on('open', () => {
                    clearTimeout(timeout)
                    console.log(`🔗 Connected to Python server for user: ${userId}`)
                    resolve(ws)
                })
                
                ws.on('message', (message) => {
                    this.handlePythonResponse(socket, message, language)
                })
                
                ws.on('error', (error) => {
                    clearTimeout(timeout)
                    console.error(`❌ Python server connection error for ${userId}:`, error.message)
                    reject(error)
                })
                
                ws.on('close', () => {
                    console.log(`🔌 Python server connection closed for user: ${userId}`)
                    this.pythonConnections.delete(userId)
                })
                
                this.pythonConnections.set(userId, ws)
            })
        } catch (error) {
            console.error(`❌ Failed to connect to Python server for ${userId}:`, error.message)
            return null
        }
    }

    handleDisconnect(socket) {
        console.log(`👋 User disconnected: ${socket.id}`)
        
        const pythonWs = this.pythonConnections.get(socket.id)
        if (pythonWs) {
            pythonWs.close()
            this.pythonConnections.delete(socket.id)
        }
    }

    getConnectionsCount() {
        return this.pythonConnections.size
    }
}

module.exports = new SocketService()
