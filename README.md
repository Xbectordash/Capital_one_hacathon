# 🌾 FarmMate – Your AI-Powered Farming Companion

**FarmMate** is an agentic AI application designed to assist farmers with intelligent, localized, and real-time agricultural support. From weather-based planning to crop suggestions and market insights — FarmMate is a smart, multilingual, and farmer-friendly solution built with love for India's diverse agricultural community.

---

## 🧠 Why FarmMate?

In a country as vast and diverse as India, farmers often face:
- Unpredictable weather patterns
- Lack of region-specific crop guidance
- Fragmented information systems
- Language barriers across states

**FarmMate** bridges this gap using Agentic AI, multimodal inputs, and real-time data integrations.

---

## 🚀 Key Features

- 🌤️ **Weather-Aware Planning** – AI recommendations based on weather forecasts
- 🧠 **Agentic Decision Support** – Goal-driven, proactive agents for each crop/lifecycle stage
- 🗣️ **Multilingual Support** – Talk or type in your native language
- 🧑‍🌾 **Farmer-Centric Design** – Built for low-tech users with clean UI
- 🛰️ **Satellite & Market APIs** – Access satellite insights and mandi prices
- 🧩 **Modular Architecture** – Easily pluggable backend modules (Python/JS)

---

## 🏗️ Tech Stack

| Layer | Tech |
|-------|------|
| 🌐 Frontend | Flutter (for Web + Mobile) |
| 🧠 AI Engine | Gemini Pro + LangChain |
| 🔙 Backend | Node.js (agent routing, auth), Python (AI agents) |
| 🐳 Containerization | Docker with multi-service setup |
| 🌩️ Data Sources | Weather APIs, Satellite APIs, Agri Market APIs |
| 🧠 Memory DB | ChromaDB (for contextual agent memory) |

---

## 📦 Project Structure

```
🌾 FarmMate/
├── 📄 README.md                    # Project documentation
├── 📄 docker-compose.yml           # Multi-service Docker orchestration
├── 📄 DOCKER_DEPLOYMENT.md         # Docker deployment guide
├── 
├── 📁 scripts/                     # Startup and utility scripts
│   ├── start-farmmate.ps1         # PowerShell startup script
│   └── start-farmmate.sh          # Bash startup script
│
├── 📁 backend/                     # Express.js Gateway Service
│   ├── 📄 Dockerfile              # Backend containerization
│   ├── 📄 package.json            # Node.js dependencies & scripts
│   ├── 📁 src/                    # Source code
│   │   ├── index.js               # Express server entry point
│   │   ├── 📁 controller/         # Request handlers
│   │   ├── 📁 router/             # API routing
│   │   └── 📁 services/           # Socket.IO & WebSocket services
│   └── 📁 tests/                  # Test suites
│       ├── test-communication.js   # Basic connectivity tests
│       ├── test-direct-ai.js      # Direct Python AI tests
│       ├── test-farm-query.js     # Single query tests
│       ├── test-comprehensive-farm.js # Complete workflow tests
│       ├── run-all-tests.js       # Test runner
│       └── README.md              # Test documentation
│
├── 📁 agent-python/               # Python AI Server
│   ├── 📄 Dockerfile             # AI server containerization
│   ├── 📄 requirement.txt        # Python dependencies
│   ├── 📁 src/                   # AI source code
│   │   ├── main.py               # FastAPI server entry
│   │   ├── 📁 graph_arc/         # Agent workflow architecture
│   │   ├── 📁 data/              # Data plugins (weather, soil, etc.)
│   │   ├── 📁 server/            # WebSocket server
│   │   └── 📁 tests/             # Python test suites
│   └── 📁 docs/                  # AI agent documentation
│
├── 📁 frontend/                   # React Web Application
│   └── 📁 web/agricultural-chat-app/
│       ├── 📄 Dockerfile         # Frontend containerization
│       ├── 📄 package.json       # React dependencies
│       └── 📁 src/               # React components
│
└── 📁 chromaDB/                  # Vector Database Service
    ├── 📄 Dockerfile             # ChromaDB containerization
    ├── 📄 requirements.txt       # Database dependencies
    └── starter.py                # Database initialization
```

## 🚀 Quick Start

### 1. Start All Services
```bash
# PowerShell (Windows)
.\scripts\start-farmmate.ps1

# Bash (Linux/Mac)
./scripts/start-farmmate.sh

# Manual Docker
docker-compose up --build -d
```

### 2. Run Tests
```bash
# Navigate to backend
cd backend

# Run all tests
npm run test:all

# Or individual tests
npm run test              # Basic communication
npm run test:direct       # Direct AI connection
npm run test:query        # Single farm query
npm run test:comprehensive # Complete workflow
```

### 3. Access Services
- 🌐 **Frontend**: http://localhost:3000
- 🔗 **Express API**: http://localhost:5000  
- 🤖 **Python AI**: http://localhost:8000
- 📚 **API Docs**: http://localhost:8000/docs

---

