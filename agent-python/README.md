
# 🤖 FarmMate AI - Python AI Processing Engine

Advanced agricultural AI service powered by Google Gemini and LangChain for intelligent farming guidance and decision support.

## 🧠 Overview

The **FarmMate AI Python Engine** is the core intelligence system that processes agricultural queries through specialized AI agents. It provides comprehensive, multilingual, and context-aware farming advice using cutting-edge natural language processing and agricultural domain expertise.

---

## 🚀 Key Features

### 🌾 **Multi-Agent Architecture**
- **Weather Agent**: Real-time weather analysis and farming recommendations
- **Soil Agent**: Soil health assessment and nutrient management
- **Market Agent**: Price trends and selling guidance
- **Government Schemes Agent**: Subsidy and loan information
- **Decision Support Agent**: Comprehensive advice synthesis

### 🧠 **Advanced AI Capabilities**
- **Google Gemini 2.0 Flash**: Latest LLM for agricultural reasoning
- **Multi-Intent Processing**: Handle complex queries with multiple farming aspects
- **Confidence Scoring**: Reliability assessment for recommendations
- **Context Awareness**: Persistent memory across conversations

### 🗣️ **Multilingual Support**
- **Supported Languages**: Hindi, English, Punjabi, Gujarati, Marathi
- **Intent Classification**: Advanced ML models for query understanding
- **Cultural Adaptation**: Region-specific farming practices integration

### ⚡ **Real-Time Data Integration**
- **Weather APIs**: Live weather data and forecasts
- **Market APIs**: Current mandi prices across India
- **Satellite Data**: Soil and crop monitoring (planned)
- **Government APIs**: Latest scheme information

---

## 🏗️ Agent Workflow Architecture

```
         ┌─────────────────────┐
         │ 1. UserContextNode  │
         │  (detect location,  │
         │  language, device)  │
         └─────────┬───────────┘
                   │
                   ▼
         ┌─────────────────────┐
         │ 2. QueryUnderstanding│
         │  (intent, entities,  │
         │   multi-intent)      │
         └─────────┬───────────┘
                   │
                   ▼
         ┌─────────────────────┐
         │ 3. ConditionalRouter │
         │ (route to relevant   │
         │  agent functions)    │
         └───────┬──────────────┘
   ┌─────────────┼─────────────────────────────┐
   ▼             ▼             ▼               ▼
WeatherAgent   SoilAgent   MarketAgent   PolicyAgent
   │             │             │               │
   ▼             ▼             ▼               ▼
CropHealthAgent OfflineAgent (optional)   ... more
   └─────────────┬─────────────────────────────┘
                 ▼
         ┌─────────────────────┐
         │ 4. DecisionSupport  │
         │  (aggregate all     │
         │   agent outputs)    │
         └─────────┬───────────┘
                   ▼
         ┌─────────────────────┐
         │ 5. TranslationNode  │
         │ (final reply in     │
         │  user's language)   │
         └─────────┬───────────┘
                   ▼
                Final
               Response
```

---

## 📦 Project Structure

```
🤖 agent-python/
├── 📄 README.md                    # This documentation
├── 📄 Dockerfile                   # Container configuration
├── 📄 requirement.txt              # Python dependencies
├── 📄 pyproject.toml               # Poetry configuration
├── 
├── 📁 src/                         # Core application code
│   ├── main.py                     # FastAPI application entry
│   ├── start_server.py             # Production server startup
│   ├── performance_test.py         # Performance benchmarks
│   │
│   ├── 📁 config/                  # Configuration management
│   │   ├── settings.py             # Application settings
│   │   └── model_conf.py           # AI model configuration
│   │
│   ├── 📁 graph_arc/               # Agent workflow architecture
│   │   ├── graph.py                # Main workflow orchestration
│   │   ├── router.py               # Intent-based agent routing
│   │   ├── prompts.py              # AI prompt engineering
│   │   ├── schemas.py              # Data validation schemas
│   │   ├── state.py                # Conversation state management
│   │   ├── 📁 agents_node/         # Specialized AI agents
│   │   └── 📁 core_nodes/          # Core processing nodes
│   │
│   ├── 📁 data/                    # Data plugins and integrations
│   │   ├── weather_plugins.py      # Weather API integrations
│   │   ├── soil_plugins.py         # Soil data processing
│   │   ├── price_from_mandi.py     # Market price fetching
│   │   ├── government_schemes_plugin.py # Schemes database
│   │   └── soil.csv                # Soil reference data
│   │
│   ├── 📁 server/                  # Web server implementation
│   │   ├── app.py                  # FastAPI application
│   │   ├── routes.py               # HTTP endpoint routes
│   │   └── README.md               # Server documentation
│   │
│   ├── 📁 services/                # Core services
│   │   └── intent_classification_service.py # ML-based intent detection
│   │
│   ├── 📁 tests/                   # Comprehensive test suite
│   │   ├── test_intent_model.py    # Intent classification tests
│   │   ├── test_weather_plugins.py # Weather integration tests
│   │   ├── test_soil_plugins.py    # Soil analysis tests
│   │   ├── test_government_schemes.py # Schemes data tests
│   │   └── test_websocket_client.py # WebSocket functionality
│   │
│   ├── 📁 tools/                   # Utility tools
│   │   └── mandi_price_tool.py     # Market price utilities
│   │
│   ├── 📁 utils/                   # Shared utilities
│   │   └── loggers.py              # Logging configuration
│   │
│   └── 📁 examples/                # Integration examples
│       └── frontend_integration_examples.py
│
├── 📁 model/                       # Pre-trained ML models
│   ├── agricultural_multilabel_model.pkl
│   ├── multilabel_binarizer.pkl
│   └── multilabel_tfidf_vectorizer.pkl
│
├── 📁 docs/                        # Comprehensive documentation
│   ├── MULTILINGUAL_INTENT_CLASSIFICATION.md
│   ├── soil_agent_documentation.md
│   ├── weather_agent_documentation.md
│   ├── government_schemes_documentation.md
│   └── SYSTEM_STATUS_REPORT.md
│
├── 📁 env/                         # Environment configurations
│   ├── .env                        # Local development
│   ├── production.env              # Production settings
│   └── sample.env                  # Template configuration
│
└── 📁 test/                        # Additional test files
    └── test_intent_model.py        # Intent model validation
```

---

## 🚀 Quick Start

### 🔧 Prerequisites
- **Python 3.11+**
- **Poetry** or **pip** for dependency management
- **Google AI API Key** (Gemini)
- **Weather API Key**
- **Docker** (optional)

### 1. 📦 Installation

#### Option A: Poetry (Recommended)
```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Start server
poetry run python src/start_server.py
```

#### Option B: pip
```bash
# Create virtual environment
python -m venv farmmate-ai
source farmmate-ai/bin/activate  # Linux/Mac
# farmmate-ai\Scripts\activate   # Windows

# Install dependencies
pip install -r requirement.txt

# Start server
python src/start_server.py
```

#### Option C: Docker
```bash
# Build container
docker build -t farmmate-ai .

# Run container
docker run -p 8000:8000 farmmate-ai
```

### 2. ⚙️ Environment Configuration

Create `.env` file:
```env
# AI Configuration
GEMINI_API_KEY=your_gemini_api_key_here
QUERY_UNDERSTANDING_MODEL=gemini-2.0-flash

# Weather API
WEATHER_API=your_weather_api_key_here

# Optional: LangSmith Tracing
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key

# Optional: Agriculture Market API
AGMARKNET_API_KEY=your_agmarknet_api_key

# Server Configuration
PORT=8000
LOG_LEVEL=INFO
PYTHONUNBUFFERED=1
```

### 3. 🌐 Access Services

| Endpoint | URL | Description |
|----------|-----|-------------|
| 🏠 **Home** | http://localhost:8000 | Landing page with navigation |
| 🧪 **Test Page** | http://localhost:8000/test-page | WebSocket testing interface |
| 🔬 **API Testing** | http://localhost:8000/api-test | HTTP API testing suite |
| 📚 **API Docs** | http://localhost:8000/docs | FastAPI documentation |
| 💚 **Health Check** | http://localhost:8000/health | Service health status |
| 📊 **Statistics** | http://localhost:8000/stats | Usage statistics |

---

## 🎯 API Usage Examples

### 📡 WebSocket Connection
```python
import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8000/ws/farmer123"
    
    async with websockets.connect(uri) as websocket:
        # Send agricultural query
        query = {
            "raw_query": "मेरी गेहूं की फसल में कीड़े लग गए हैं",
            "language": "hi",
            "location": "राजस्थान"
        }
        
        await websocket.send(json.dumps(query))
        
        # Receive response
        response = await websocket.recv()
        print(json.loads(response))

asyncio.run(test_websocket())
```

### 🌐 HTTP API
```python
import requests

# Send agricultural query
response = requests.post("http://localhost:8000/chat", json={
    "user_id": "farmer123",
    "raw_query": "बारिश के मौसम में कौन सी फसल लगाऊं?",
    "language": "hi",
    "location": "महाराष्ट्र"
})

advice = response.json()
print(advice["response"])
```

---

## 🧪 Testing

### 🔍 Run Test Suite
```bash
# All tests
python -m pytest src/tests/ -v

# Specific test categories
python -m pytest src/tests/test_intent_model.py      # Intent classification
python -m pytest src/tests/test_weather_plugins.py  # Weather integration
python -m pytest src/tests/test_soil_plugins.py     # Soil analysis
python -m pytest src/tests/test_government_schemes.py # Schemes data

# Integration tests
python src/tests/test_websocket_client.py            # WebSocket functionality
python src/performance_test.py                      # Performance benchmarks
```

### 🎯 Sample Test Queries
```python
test_queries = [
    "मेरी गेहूं की फसल में कीड़े लग गए हैं, क्या करूं?",
    "बारिश के मौसम में कौन सी फसल उगाऊं?",
    "मिट्टी की जांच कैसे करूं?",
    "आज गेहूं का भाव क्या है?",
    "किसान योजना के लिए कैसे अप्लाई करूं?",
    "मेरे खेत की मिट्टी में नाइट्रोजन की कमी है"
]
```

---

## 📊 Performance Metrics

### ⚡ Response Time Targets
- **Simple Queries**: < 2 seconds
- **Complex Multi-Intent**: < 5 seconds
- **Weather Data Fetch**: < 1 second
- **Market Price Updates**: < 1.5 seconds

### 🧠 AI Model Performance
- **Intent Classification Accuracy**: 95%+
- **Multi-language Support**: 5 Indian languages
- **Confidence Scoring**: 0.0-1.0 reliability scale
- **Context Retention**: 10-message conversation window

---

## 🤝 Contributing

### 🛠️ Development Setup
```bash
# Clone repository
git clone https://github.com/Xbectordash/Capital_one_hacathon.git
cd Capital_one_hacathon/agent-python

# Setup development environment
poetry install --dev
pre-commit install

# Run tests before contributing
poetry run pytest
poetry run black src/
poetry run isort src/
```

### 📝 Code Standards
- **Black**: Code formatting
- **isort**: Import sorting
- **Type Hints**: All functions must have type annotations
- **Docstrings**: Google-style documentation
- **Testing**: 90%+ code coverage required

---

## 🌟 Advanced Features

### 🔮 Future Enhancements
- **Satellite Imagery**: Integration with agricultural satellite data
- **IoT Sensors**: Real-time field sensor data processing
- **Predictive Analytics**: Crop yield and disease prediction
- **Voice Interface**: Speech-to-text and text-to-speech support

---

**🤖 Powered by Google Gemini AI | Built for Indian Farmers 🌾**
