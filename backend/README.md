# 🌐 FarmMate Backend - Express.js API Gateway

High-performance Node.js backend service providing API gateway functionality, WebSocket management, and real-time communication between frontend and AI services.

## 🧠 Overview

The **FarmMate Backend** serves as the central communication hub, managing real-time WebSocket connections, API routing, and seamless integration between the React frontend and Python AI services. Built with Express.js and Socket.IO for optimal performance and scalability.

---

## 🚀 Key Features

### ⚡ **Real-Time Communication**
- **Socket.IO Integration**: Bidirectional real-time communication
- **WebSocket Management**: Efficient connection handling and scaling
- **Message Broadcasting**: Multi-client synchronization
- **Auto-Reconnection**: Robust connection resilience

### 🌐 **API Gateway Architecture**
- **Express.js Framework**: Fast, minimalist web framework
- **RESTful Endpoints**: Standard HTTP API routes
- **Middleware Stack**: Authentication, logging, and error handling
- **CORS Support**: Cross-origin resource sharing configuration

### 🔄 **AI Service Integration**
- **Python AI Bridge**: Seamless communication with FastAPI services
- **Request Forwarding**: Intelligent routing to AI agents
- **Response Formatting**: Structured data transformation
- **Error Handling**: Graceful failure management

### 📊 **Monitoring & Analytics**
- **Request Logging**: Comprehensive API usage tracking
- **Performance Metrics**: Response time and throughput monitoring
- **Error Tracking**: Real-time error detection and reporting
- **Health Checks**: Service availability monitoring

---

## 🏗️ Service Architecture

```
Frontend (React) ←→ Backend (Express.js) ←→ AI Service (Python/FastAPI)
                           │
                           ├── Socket.IO Server
                           ├── REST API Routes
                           ├── Middleware Stack
                           ├── WebSocket Bridge
                           └── Error Handling
```

### 🔀 Request Flow
```
1. Client Request → Express.js Middleware
2. Authentication & Validation
3. WebSocket/HTTP Route Selection
4. AI Service Communication
5. Response Formatting
6. Client Response Delivery
```

---

## 📦 Project Structure

```
🌐 backend/
├── 📄 README.md                    # This documentation
├── 📄 Dockerfile                   # Container configuration
├── 📄 Dockerfile.enhanced          # Enhanced production container
├── 📄 package.json                 # Node.js dependencies
├── 📄 package.toml                 # Configuration metadata
│
├── 📁 src/                         # Core application code
│   ├── index.js                    # Main application entry point
│   ├── enhanced_server.js          # Enhanced production server
│   │
│   ├── 📁 config/                  # Configuration management
│   │   ├── database.js             # Database configuration
│   │   ├── cors.js                 # CORS settings
│   │   ├── socket.js               # Socket.IO configuration
│   │   └── environment.js          # Environment variables
│   │
│   ├── 📁 controller/              # Request controllers
│   │   ├── chatController.js       # Chat message handling
│   │   ├── healthController.js     # Health check endpoints
│   │   ├── apiController.js        # API route management
│   │   └── wsController.js         # WebSocket management
│   │
│   ├── 📁 router/                  # Express route definitions
│   │   ├── chatRoutes.js           # Chat API routes
│   │   ├── healthRoutes.js         # Health check routes
│   │   ├── apiRoutes.js            # General API routes
│   │   └── index.js                # Route aggregation
│   │
│   ├── 📁 services/                # Core business logic
│   │   ├── socketService.js        # Socket.IO service logic
│   │   ├── aiService.js            # AI integration service
│   │   ├── languageService.js      # Language configuration
│   │   ├── validationService.js    # Request validation
│   │   └── loggerService.js        # Logging utilities
│   │
│   └── 📁 middleware/              # Express middleware
│       ├── auth.js                 # Authentication middleware
│       ├── validation.js           # Request validation
│       ├── logging.js              # Request logging
│       ├── errorHandler.js         # Error handling
│       └── rateLimiter.js          # Rate limiting
│
└── 📁 tests/                       # Comprehensive test suite
    ├── README.md                   # Testing documentation
    ├── run-all-tests.js            # Test runner utility
    ├── test-communication.js       # Communication testing
    ├── test-comprehensive-farm.js  # Farm functionality tests
    ├── test-direct-ai.js           # AI integration tests
    └── test-farm-query.js          # Query processing tests
```

---

## 🚀 Quick Start

### 🔧 Prerequisites
- **Node.js 18+**
- **npm** or **yarn** package manager
- **Docker** (optional)
- **Python AI Service** running on port 8000

### 1. 📦 Installation

#### Option A: npm (Recommended)
```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Start production server
npm start
```

#### Option B: yarn
```bash
# Install dependencies
yarn install

# Start development server
yarn dev

# Start production server
yarn start
```

#### Option C: Docker
```bash
# Build container
docker build -t farmmate-backend .

# Run container
docker run -p 3000:3000 farmmate-backend
```

#### Option D: Docker Compose (Full Stack)
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend
```

### 2. ⚙️ Environment Configuration

Create `.env` file:
```env
# Server Configuration
PORT=3000
NODE_ENV=development
HOST=localhost

# AI Service Integration
AI_SERVICE_URL=http://localhost:8000
AI_SERVICE_WS=ws://localhost:8000

# CORS Configuration
FRONTEND_URL=http://localhost:3000
ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend-domain.com

# WebSocket Configuration
SOCKET_IO_CORS_ORIGIN=http://localhost:3000
MAX_CONNECTIONS=100

# Logging
LOG_LEVEL=info
LOG_FORMAT=combined

# Optional: Rate Limiting
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=100

# Optional: Database
DATABASE_URL=mongodb://localhost:27017/farmmate
REDIS_URL=redis://localhost:6379
```

### 3. 🌐 Access Services

| Endpoint | URL | Description |
|----------|-----|-------------|
| 🏠 **API Base** | http://localhost:3000 | API root endpoint |
| 💬 **Chat API** | http://localhost:3000/api/chat | HTTP chat endpoint |
| 🔌 **WebSocket** | ws://localhost:3000 | Socket.IO connection |
| 💚 **Health Check** | http://localhost:3000/health | Service health status |
| 📊 **Status** | http://localhost:3000/status | Detailed service status |

---

## 🎯 API Documentation

### 💬 Chat Endpoints

#### POST `/api/chat`
Send a chat message via HTTP
```javascript
// Request
{
  "user_id": "farmer123",
  "message": "मेरी गेहूं की फसल में कीड़े लग गए हैं",
  "language": "hi",
  "location": "राजस्थान"
}

// Response
{
  "success": true,
  "response": "आपकी गेहूं की फसल में कीड़ों की समस्या के लिए...",
  "final_advice": "तुरंत नीम का तेल का छिड़काव करें",
  "summary_message": "फसल की सुरक्षा के लिए जैविक कीटनाशक का उपयोग सबसे अच्छा है",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 🔌 WebSocket Events

#### Client → Server Events
```javascript
// Connect to WebSocket
const socket = io('http://localhost:3000');

// Send message
socket.emit('send_message', {
  user_id: 'farmer123',
  message: 'बारिश के मौसम में कौन सी फसल लगाऊं?',
  language: 'hi',
  location: 'महाराष्ट्र'
});

// Join user room
socket.emit('join_room', { user_id: 'farmer123' });
```

#### Server → Client Events
```javascript
// Receive response
socket.on('ai_response', (data) => {
  console.log('AI Response:', data.response);
  console.log('Final Advice:', data.final_advice);
  console.log('Summary:', data.summary_message);
});

// Connection status
socket.on('connect', () => console.log('Connected to server'));
socket.on('disconnect', () => console.log('Disconnected'));

// Error handling
socket.on('error', (error) => console.error('Error:', error));
```

### 💚 Health Check

#### GET `/health`
```javascript
// Response
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "services": {
    "ai_service": "connected",
    "database": "connected",
    "redis": "connected"
  },
  "uptime": 86400,
  "memory_usage": "45.2 MB"
}
```

---

## 🧪 Testing

### 🔍 Run Test Suite
```bash
# All tests
npm test

# Specific test files
npm run test:communication     # Communication testing
npm run test:farm             # Farm functionality
npm run test:ai               # AI integration
npm run test:query            # Query processing

# Integration testing
node tests/run-all-tests.js   # Complete test suite
```

### 🎯 Manual Testing Examples
```bash
# Test HTTP endpoint
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","message":"गेहूं की फसल की जानकारी चाहिए","language":"hi"}'

# Test WebSocket (using wscat)
wscat -c ws://localhost:3000
```

---

## 📊 Performance & Monitoring

### ⚡ Performance Targets
- **API Response Time**: < 100ms (excluding AI processing)
- **WebSocket Latency**: < 50ms
- **Throughput**: 1000+ requests/minute
- **Concurrent Connections**: 100+ WebSocket connections

### 📈 Monitoring
```javascript
// Built-in performance monitoring
app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log(`${req.method} ${req.path} - ${duration}ms`);
  });
  next();
});
```

---

## 🛠️ Production Deployment

### 🐳 Docker Production
```bash
# Build production image
docker build -f Dockerfile.enhanced -t farmmate-backend:prod .

# Run with environment variables
docker run -d \
  --name farmmate-backend \
  -p 3000:3000 \
  --env-file .env.production \
  farmmate-backend:prod
```

### ☁️ Cloud Deployment
```yaml
# Example: docker-compose.yml for production
version: '3.8'
services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.enhanced
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - AI_SERVICE_URL=http://ai-service:8000
    depends_on:
      - ai-service
      - redis
    restart: unless-stopped
```

---

## 🤝 Contributing

### 🛠️ Development Setup
```bash
# Clone repository
git clone https://github.com/Xbectordash/Capital_one_hacathon.git
cd Capital_one_hacathon/backend

# Install dependencies
npm install

# Run development server with hot reload
npm run dev

# Run tests
npm test

# Lint code
npm run lint
```

### 📝 Code Standards
- **ESLint**: JavaScript linting
- **Prettier**: Code formatting
- **JSDoc**: Function documentation
- **Jest**: Unit testing framework
- **Supertest**: API testing

---

## 🌟 Advanced Features

### 🔮 Planned Enhancements
- **Redis Integration**: Session management and caching
- **Database Integration**: User data and conversation history
- **API Rate Limiting**: Request throttling and abuse prevention
- **Load Balancing**: Multi-instance deployment support
- **Metrics Dashboard**: Real-time performance monitoring

### 🔒 Security Features
- **CORS Protection**: Cross-origin request filtering
- **Input Validation**: Request data sanitization
- **Error Sanitization**: Secure error responses
- **Rate Limiting**: DDoS protection

---

## 📜 Available Scripts

| Command | Description |
|---------|-------------|
| `npm start` | Start production server |
| `npm run dev` | Start development server with hot reload |
| `npm test` | Run test suite |
| `npm run lint` | Lint JavaScript code |
| `npm run format` | Format code with Prettier |
| `npm run build` | Build for production |

---

**🌐 Express.js API Gateway | Real-time WebSocket Communication | Built for FarmMate 🌾**
