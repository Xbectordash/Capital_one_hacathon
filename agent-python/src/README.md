# Agricultural AI Assistant - Python Backend

## 📁 Project Structure

```
agent-python/
├── 📖 README.md                # Main project documentation
├── 📋 requirement.txt          # Python dependencies
├── 🐳 Dockerfile              # Docker configuration
├── � docs/                    # 📚 All project documentation
│   ├── government_schemes_documentation.md
│   ├── soil_agent_documentation.md
│   ├── weather_agent_documentation.md
│   ├── SERVER_SETUP_COMPLETE.md
│   └── SYSTEM_STATUS_REPORT.md
├── 📁 env/                     # Environment configuration
│   ├── .env
│   └── sample.env
└── 📁 src/                     # 💻 Source code
    ├── 🚀 start_server.py      # Server startup script
    ├── 🧠 main.py              # CLI testing interface
    ├── 📁 core/                # Core business logic
    │   └── constants.py        
    ├── 📁 server/              # FastAPI server
    │   ├── app.py              # Main FastAPI application
    │   ├── routes.py           # API routes
    │   └── README.md           # Server documentation
    ├── 📁 graph_arc/           # AI workflow engine
    │   ├── graph.py            # Main workflow graph
    │   ├── router.py           # Query routing logic
    │   ├── state.py            # State management
    │   ├── agents_node/        # AI agents
    │   └── core_nodes/         # Core processing nodes
    ├── 📁 data/                # Data plugins
    │   ├── weather_plugins.py  # Weather data
    │   ├── soil_plugins.py     # Soil analysis
    │   ├── price_from_mandi.py # Market prices
    │   └── government_schemes_plugin.py # Government schemes
    ├── 📁 config/              # Configuration
    │   ├── settings.py         # App settings
    │   └── model_conf.py       # AI model config
    ├── 📁 tools/               # Utility tools
    │   └── mandi_price_tool.py # Price calculation tool
    ├── 📁 utils/               # Utilities
    │   └── loggers.py          # Logging utilities
    ├── 📁 loaders/             # Data loaders
    │   └── pdf_lodder.py       # PDF processing
    ├── 📁 tests/               # All test files
    │   ├── test_government_schemes.py
    │   ├── test_soil_plugins.py
    │   ├── test_weather_plugins.py
    │   ├── test_gov_schemes_llm.py
    │   └── test_websocket_client.py
    └── 📁 examples/            # Integration examples
        └── frontend_integration_examples.py
```

## 🚀 Quick Start

### Start the Server
```bash
cd agent-python/src
python start_server.py
```

### Test CLI Interface
```bash
cd agent-python/src
python main.py
```

### Run Tests
```bash
cd agent-python/src
python -m pytest tests/
```

## 🔌 API Endpoints

- **WebSocket**: `ws://localhost:8000/ws/{user_id}`
- **Health Check**: `http://localhost:8000/health`
- **API Docs**: `http://localhost:8000/docs`
- **Test Page**: `http://localhost:8000/test-page`

## 🏗️ Architecture

1. **FastAPI Server** → WebSocket endpoints for real-time communication
2. **Graph Workflow** → AI processing pipeline with multiple agents
3. **Data Plugins** → External data sources (weather, soil, market, govt)
4. **Core Nodes** → Query understanding, translation, decision support

## 🌐 Integration

Connect with Express.js server for full-stack communication:
- React Frontend → Express Gateway → Python AI Server
