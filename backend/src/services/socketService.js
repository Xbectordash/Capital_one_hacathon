const { Server } = require('socket.io')
const WebSocket = require('ws')
const { isLanguageSupported, getStatusMessage, getLabel, getErrorMessage } = require('../config/languageConfig')

class SocketService {
    constructor() {
        this.io = null
        this.pythonConnections = new Map()
        // Use environment variable or Docker container name
        this.PYTHON_SERVER_URL = process.env.PYTHON_SERVER_URL || 'ws://agent-python:8000'
        console.log(`🔧 SocketService initialized with Python server URL: ${this.PYTHON_SERVER_URL}`)
    }

    initialize(server) {
        // Get environment-specific CORS origins
        const isDevelopment = process.env.NODE_ENV !== 'production'
        const corsOrigins = isDevelopment 
            ? ["http://localhost:3000", "http://localhost:3001"]
            : [
                "https://farmmate-frontend.onrender.com",
                "https://capital-one-hacathon.vercel.app",
                "https://capital-one-hacathon-czxg85qmw.vercel.app",
                "http://localhost:3000", // Keep for local testing
                process.env.FRONTEND_URL // Allow dynamic frontend URL
            ].filter(Boolean) // Remove undefined values

        this.io = new Server(server, {
            cors: {
                origin: corsOrigins,
                methods: ["GET", "POST"],
                credentials: true
            }
        })

        this.setupSocketHandlers()
        console.log(`🔌 Socket.IO service initialized with CORS origins: ${corsOrigins.join(', ')}`)
    }

    setupSocketHandlers() {
        this.io.on('connection', (socket) => {
            console.log(`👤 New user connected with socket ID: ${socket.id}`)
            
            socket.on('user_query', async (data) => {
                await this.handleUserQuery(socket, data)
            })
            
            socket.on('disconnect', () => {
                this.handleDisconnect(socket)
            })

            socket.on('error', (error) => {
                console.error(`❌ Socket error for user ${socket.id}:`, error)
            })
        })
    }

    async handleUserQuery(socket, data) {
        const { query, userId = socket.id, language = 'en' } = data
        
        // Validate language support
        const supportedLang = isLanguageSupported(language) ? language : 'en'
        if (language !== supportedLang) {
            console.log(`⚠️  Unsupported language '${language}' for user ${userId}, defaulting to English`)
        }
        
        console.log(`📝 Received query from ${userId} in language '${supportedLang}': ${query}`)
        
        try {
            let pythonWs = this.pythonConnections.get(userId)
            
            if (!pythonWs || pythonWs.readyState !== WebSocket.OPEN) {
                pythonWs = await this.connectToPythonServer(userId, socket, supportedLang)
            }
            
            if (!pythonWs) {
                console.error(`❌ Failed to establish connection to Python AI server for user ${userId}`)
                socket.emit('error', { message: getErrorMessage('connectionError', supportedLang) })
                return
            }
            
            const queryData = {
                raw_query: query,
                language: supportedLang,
                user_id: userId
            }
            
            console.log(`🚀 Sending query to Python server for user ${userId} with language: ${supportedLang}`)
            pythonWs.send(JSON.stringify(queryData))
            
        } catch (error) {
            console.error(`❌ Error processing query for user ${userId}:`, error)
            socket.emit('error', { message: getErrorMessage('serverError', supportedLang) })
        }
    }

    handlePythonResponse(socket, message, language) {
        try {
            const response = JSON.parse(message.toString())
            console.log(`📤 Received Python response type: ${response.type} for language: ${language}`)
            
            // Only send final responses to the client, not intermediate status updates
            if (response.type === 'connection_established') {
                console.log('✅ Python AI server connection established successfully')
                return
            }
            
            if (response.type === 'message_received') {
                socket.emit('ai_status', { 
                    message: getStatusMessage('messageReceived', language),
                    status: 'received'
                })
                return
            }
            
            if (response.type === 'status_update') {
                const stage = response.details?.stage
                let statusMsg
                
                if (stage === 'analyzing_query') {
                    statusMsg = getStatusMessage('analyzingQuery', language)
                } else if (stage === 'generating_response') {
                    statusMsg = getStatusMessage('generatingResponse', language)
                } else {
                    statusMsg = getStatusMessage('processing', language)
                }
                
                socket.emit('ai_status', { 
                    message: statusMsg,
                    status: 'processing'
                })
                return
            }
            
            // Handle the final agricultural response
            if (response.type === 'agricultural_response' && response.success && response.data) {
                console.log(`✅ Successfully processed agricultural response for language: ${language}`)
                const data = response.data
                let formattedResponse = ''
                
                // Check if we have comprehensive advice (new enhanced format)
                if (data.comprehensive_advice) {
                    console.log('📊 Using comprehensive advice format')
                    const comprehensive = data.comprehensive_advice
                    
                    // Format comprehensive response with better visual structure
                    formattedResponse = `🎯 🌾 ${comprehensive.final_advice || 'Agricultural advice'}\n\n`
                    
                    if (comprehensive.weather_analysis) {
                        const weather = comprehensive.weather_analysis
                        formattedResponse += `═══════════════════════════════════════\n`
                        formattedResponse += `🌤️ WEATHER ANALYSIS:\n`
                        formattedResponse += `═══════════════════════════════════════\n`
                        formattedResponse += `📊 Current: ${weather.current_conditions || 'N/A'}\n`
                        formattedResponse += `⚡ Farming: ${weather.farming_suitability || 'N/A'}\n`
                        formattedResponse += `🕒 Next 24h: ${weather.next_24h_guidance || 'N/A'}\n\n`
                    }
                    
                    if (comprehensive.soil_analysis) {
                        const soil = comprehensive.soil_analysis
                        formattedResponse += `═══════════════════════════════════════\n`
                        formattedResponse += `🌱 SOIL ANALYSIS:\n`
                        formattedResponse += `═══════════════════════════════════════\n`
                        formattedResponse += `📊 Nutrients: ${soil.nutrient_status || 'N/A'}\n`
                        formattedResponse += `⭐ Health: ${soil.soil_health_score || 'N/A'}\n`
                        if (soil.immediate_actions && soil.immediate_actions.length > 0) {
                            formattedResponse += `🔧 Actions:\n`
                            soil.immediate_actions.forEach(action => {
                                formattedResponse += `   • ${action}\n`
                            })
                        }
                        if (soil.crop_recommendations && soil.crop_recommendations.length > 0) {
                            formattedResponse += `🌾 Recommended Crops:\n`
                            soil.crop_recommendations.forEach(crop => {
                                formattedResponse += `   • ${crop}\n`
                            })
                        }
                        formattedResponse += '\n'
                    }
                    
                    if (comprehensive.market_insights) {
                        const market = comprehensive.market_insights
                        formattedResponse += `═══════════════════════════════════════\n`
                        formattedResponse += `💰 MARKET INSIGHTS:\n`
                        formattedResponse += `═══════════════════════════════════════\n`
                        formattedResponse += `💵 Prices: ${market.current_prices || '💰 (Check agmarknet.gov.in for current prices)'}\n`
                        formattedResponse += `📈 Trend: ${market.price_trend || '📊 (Check agmarknet.gov.in for price trends)'}\n`
                        formattedResponse += `⏰ Timing: ${market.selling_timing || '🕒 (Check agmarknet.gov.in for best selling times)'}\n\n`
                    }
                    
                    if (comprehensive.priority_actions && comprehensive.priority_actions.length > 0) {
                        formattedResponse += `═══════════════════════════════════════\n`
                        formattedResponse += `🔥 PRIORITY ACTIONS:\n`
                        formattedResponse += `═══════════════════════════════════════\n`
                        comprehensive.priority_actions.forEach(action => {
                            formattedResponse += `${action}\n`
                        })
                        formattedResponse += '\n'
                    }
                    
                    if (comprehensive.cost_benefit) {
                        const cost = comprehensive.cost_benefit
                        formattedResponse += `═══════════════════════════════════════\n`
                        formattedResponse += `💵 COST-BENEFIT ANALYSIS:\n`
                        formattedResponse += `═══════════════════════════════════════\n`
                        formattedResponse += `💰 Cost: ${cost.estimated_cost || 'Contact local dealer for current prices'}\n`
                        formattedResponse += `💎 Return: ${cost.expected_return || 'Depends on crop and market conditions'}\n`
                        formattedResponse += `📅 Timeline: ${cost.roi_timeframe || 'Typically 6-12 months'}\n\n`
                    }
                    
                    if (comprehensive.risk_warnings && comprehensive.risk_warnings.length > 0) {
                        formattedResponse += `═══════════════════════════════════════\n`
                        formattedResponse += `⚠️  IMPORTANT WARNINGS:\n`
                        formattedResponse += `═══════════════════════════════════════\n`
                        comprehensive.risk_warnings.forEach(warning => {
                            formattedResponse += `${warning}\n`
                        })
                        formattedResponse += '\n'
                    }
                    
                    if (comprehensive.confidence_score) {
                        formattedResponse += `═══════════════════════════════════════\n`
                        formattedResponse += `📊 Confidence: ${(comprehensive.confidence_score * 100).toFixed(1)}% `
                    }
                    
                } else {
                    // Fallback to simple format for backward compatibility
                    console.log('📝 Using simple advice format')
                    if (data.translated_response && language !== 'en') {
                        formattedResponse = data.translated_response
                        if (data.translated_explanation) {
                            formattedResponse += `\n\n${getLabel('explanation', language)}: ${data.translated_explanation}`
                        }
                    } else {
                        formattedResponse = data.final_advice || 'No advice available'
                        if (data.explanation) {
                            formattedResponse += '\n\nExplanation: ' + data.explanation
                        }
                    }
                }
                
                if (data.location && data.location !== 'Unknown') {
                    formattedResponse += `\n📍 ${getLabel('location', language)}: ${data.location}`
                }
                
                if (data.detected_intents && data.detected_intents.length > 0) {
                    formattedResponse += `\n🎯 ${getLabel('topic', language)}: ${data.detected_intents.join(', ')}`
                }
                
                socket.emit('ai_response', {
                    message: formattedResponse,
                    success: true,
                    type: 'agricultural_advice',
                    language: language,
                    timestamp: new Date().toISOString(),
                    comprehensive: !!data.comprehensive_advice
                })
            } else if (response.message) {
                console.log(`📝 Sending general response for language: ${language}`)
                socket.emit('ai_response', {
                    message: response.message,
                    success: response.success !== false,
                    language: language,
                    timestamp: new Date().toISOString()
                })
            }
        } catch (error) {
            console.error('❌ Error parsing Python response:', error)
            socket.emit('error', { message: getErrorMessage('responseError', language) })
        }
    }

    async connectToPythonServer(userId, socket, language) {
        try {
            console.log(`🔗 Attempting to connect to Python AI server for user: ${userId} with language: ${language}`)
            
            // Convert HTTPS URL to WSS for WebSocket connection
            const wsUrl = this.PYTHON_SERVER_URL.replace('https://', 'wss://').replace('http://', 'ws://')
            const ws = new WebSocket(`${wsUrl}/ws/${userId}`)
            
            return new Promise((resolve, reject) => {
                const timeout = setTimeout(() => {
                    console.error(`⏰ Connection timeout for user ${userId} after 10 seconds`)
                    reject(new Error('Connection timeout'))
                }, 10000) // 10 second timeout
                
                ws.on('open', () => {
                    clearTimeout(timeout)
                    console.log(`✅ Successfully connected to Python AI server for user: ${userId}`)
                    resolve(ws)
                })
                
                ws.on('message', (message) => {
                    this.handlePythonResponse(socket, message, language)
                })
                
                ws.on('error', (error) => {
                    clearTimeout(timeout)
                    console.error(`❌ Python AI server connection error for user ${userId}:`, error.message)
                    reject(error)
                })
                
                ws.on('close', () => {
                    console.log(`🔌 Python AI server connection closed for user: ${userId}`)
                    this.pythonConnections.delete(userId)
                })
                
                this.pythonConnections.set(userId, ws)
            })
        } catch (error) {
            console.error(`❌ Failed to connect to Python AI server for user ${userId}:`, error.message)
            return null
        }
    }

    handleDisconnect(socket) {
        console.log(`👋 User disconnected: ${socket.id}`)
        
        const pythonWs = this.pythonConnections.get(socket.id)
        if (pythonWs) {
            console.log(`🔌 Closing Python AI server connection for user: ${socket.id}`)
            pythonWs.close()
            this.pythonConnections.delete(socket.id)
        }
        
        console.log(`📊 Active connections remaining: ${this.pythonConnections.size}`)
    }

    getConnectionsCount() {
        return this.pythonConnections.size
    }

    getConnectionStats() {
        const activeConnections = Array.from(this.pythonConnections.entries()).map(([userId, ws]) => ({
            userId,
            state: ws.readyState,
            connected: ws.readyState === WebSocket.OPEN
        }))
        
        return {
            total: this.pythonConnections.size,
            active: activeConnections.filter(conn => conn.connected).length,
            connections: activeConnections
        }
    }
}

module.exports = new SocketService()
