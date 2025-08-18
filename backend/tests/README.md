# 🧪 FarmMate Backend Tests

This directory contains all test suites for the FarmMate Agricultural AI backend services.

## 📁 Test Files

| Test File | Purpose | Description |
|-----------|---------|-------------|
| `test-communication.js` | **Basic Communication** | Tests Socket.IO connection between frontend and Express gateway |
| `test-direct-ai.js` | **Direct AI Connection** | Tests direct WebSocket connection to Python AI server |
| `test-farm-query.js` | **Single Query Test** | Tests specific agricultural query processing |
| `test-comprehensive-farm.js` | **Full Workflow** | Tests complete agricultural workflow with multiple query types |
| `run-all-tests.js` | **Test Runner** | Executes all tests in sequence with proper reporting |

## 🚀 Running Tests

### Prerequisites
- Ensure Docker services are running:
  ```bash
  docker-compose up -d
  ```

### Individual Tests
```bash
# Basic communication test
npm run test

# Direct Python AI test  
npm run test:direct

# Single farm query test
npm run test:query

# Comprehensive workflow test
npm run test:comprehensive

# Run all tests sequentially
npm run test:all
```

### Manual Test Execution
```bash
# Run individual test files
node tests/test-communication.js
node tests/test-direct-ai.js
node tests/test-farm-query.js
node tests/test-comprehensive-farm.js

# Run complete test suite
node tests/run-all-tests.js
```

## 🔍 Test Coverage

### 🌐 **Network Communication**
- ✅ Socket.IO client-server connection
- ✅ WebSocket Express → Python AI bridge
- ✅ Error handling and timeouts

### 🤖 **AI Processing**
- ✅ Agricultural query processing
- ✅ Multi-language support (Hindi/English)
- ✅ Intent detection (crop_health, soil, weather, etc.)
- ✅ Response formatting and translation

### 🌾 **Agricultural Workflows**
- ✅ Crop health diagnosis
- ✅ Soil analysis and recommendations
- ✅ Weather-based irrigation advice
- ✅ Government scheme information
- ✅ Market price analysis

### 🐳 **Docker Integration**
- ✅ Three-tier containerized architecture
- ✅ Service-to-service communication
- ✅ Health checks and error recovery

## 📊 Expected Test Results

### Successful Test Output:
```
🌾 FarmMate Agricultural AI - Test Suite Runner
============================================================

🔧 Basic Communication Test
📋 Tests Socket.IO connection between frontend and backend
------------------------------------------------------------
✅ Connected to FarmMate System
✅ Basic Communication Test - PASSED

🐍 Direct Python AI Test
📋 Tests direct connection to Python AI server  
------------------------------------------------------------
✅ Connected directly to Python AI server
✅ Direct Python AI Test - PASSED

📝 Farm Query Test
📋 Tests specific agricultural query processing
------------------------------------------------------------
✅ Connected to FarmMate System
🤖 FarmMate AI Response received
✅ Farm Query Test - PASSED

🌾 Comprehensive Farm Test
📋 Tests complete agricultural workflow with multiple queries
------------------------------------------------------------
✅ Multiple agricultural queries processed
✅ Comprehensive Farm Test - PASSED

🎉 All tests completed!
✅ FarmMate Agricultural AI system verified
```

## 🐛 Troubleshooting

### Common Issues:

1. **Connection Refused**: Ensure Docker services are running
2. **Timeout Errors**: Check if Python AI server is healthy
3. **Generic Responses**: Verify Express gateway is properly routing to AI

### Debug Commands:
```bash
# Check Docker service status
docker-compose ps

# View service logs
docker-compose logs backend
docker-compose logs agent-python

# Restart specific service
docker-compose restart backend
```

## 🔧 Adding New Tests

1. Create test file in `/tests/` directory
2. Follow naming convention: `test-[feature-name].js`
3. Add script entry to `package.json`
4. Update test runner in `run-all-tests.js`
5. Document test purpose in this README
