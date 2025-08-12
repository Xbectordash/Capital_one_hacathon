import React, { useState, useEffect, useRef } from 'react';
import io from 'socket.io-client';
import './App.css';

const BACKEND_URL = 'http://localhost:5000';

function App() {
  const [socket, setSocket] = useState(null);
  const [connected, setConnected] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: '🤖 AI Assistant',
      message: 'नमस्ते! मैं आपका कृषि सहायक हूँ। आप मुझसे फसल, मौसम, मिट्टी, बाजार की कीमतें, और सरकारी योजनाओं के बारे में पूछ सकते हैं।',
      type: 'ai'
    }
  ]);
  const [query, setQuery] = useState('');
  const [language, setLanguage] = useState('hi');
  const [isProcessing, setIsProcessing] = useState(false);
  const chatContainerRef = useRef(null);

  // Initialize socket connection
  useEffect(() => {
    const newSocket = io(BACKEND_URL);
    setSocket(newSocket);

    newSocket.on('connect', () => {
      setConnected(true);
      console.log('Connected to server');
    });

    newSocket.on('disconnect', () => {
      setConnected(false);
      console.log('Disconnected from server');
    });

    newSocket.on('ai_response', (response) => {
      setIsProcessing(false);
      addMessage(
        '🤖 AI Assistant',
        response.message || response.response || JSON.stringify(response),
        'ai'
      );
    });

    newSocket.on('error', (error) => {
      setIsProcessing(false);
      addMessage('❌ Error', error.message, 'ai');
    });

    return () => {
      newSocket.close();
    };
  }, []);

  // Auto scroll to bottom
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  const addMessage = (sender, message, type) => {
    setMessages(prev => [
      ...prev,
      {
        id: Date.now(),
        sender,
        message,
        type,
        timestamp: new Date().toLocaleTimeString()
      }
    ]);
  };

  const sendQuery = () => {
    if (!query.trim() || !socket || !connected || isProcessing) return;

    // Add user message
    addMessage('👤 You', query, 'user');

    // Send to server
    socket.emit('user_query', {
      query: query.trim(),
      language: language,
      userId: socket.id
    });

    setQuery('');
    setIsProcessing(true);
    
    // Add processing message
    setTimeout(() => {
      addMessage('🔄 Processing', 'आपका प्रश्न संसाधित हो रहा है...', 'ai');
    }, 100);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendQuery();
    }
  };

  return (
    <div className="App">
      <div className="container">
        <h1>🌾 Agricultural AI Assistant</h1>
        
        <div className={`status ${connected ? 'connected' : 'disconnected'}`}>
          {connected ? '✅ Connected to server' : '🔌 Connecting to server...'}
        </div>
        
        <div className="language-selector">
          <label>Language: </label>
          <select 
            value={language} 
            onChange={(e) => setLanguage(e.target.value)}
            disabled={isProcessing}
          >
            <option value="en">English</option>
            <option value="hi">हिंदी</option>
            <option value="mr">मराठी</option>
            <option value="pa">ਪੰਜਾਬੀ</option>
            <option value="gu">ગુજરાતી</option>
          </select>
        </div>
        
        <div className="chat-container" ref={chatContainerRef}>
          {messages.map((msg) => (
            <div key={msg.id} className={`message ${msg.type}-message`}>
              <div className="message-header">
                <strong>{msg.sender}</strong>
                {msg.timestamp && <span className="timestamp">{msg.timestamp}</span>}
              </div>
              <div className="message-content">{msg.message}</div>
            </div>
          ))}
        </div>
        
        <div className="input-container">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="अपना प्रश्न यहाँ लिखें... (जैसे: आज सिंचाई करूं क्या?)"
            disabled={!connected || isProcessing}
          />
          <button 
            onClick={sendQuery}
            disabled={!connected || !query.trim() || isProcessing}
          >
            {isProcessing ? '⏳' : 'Send'}
          </button>
        </div>
        
        <div className="features-info">
          <h3>🔧 Available Features:</h3>
          <div className="feature-list">
            <span className="feature-tag">🌾 Crop Management</span>
            <span className="feature-tag">💰 Market Prices</span>
            <span className="feature-tag">🌡️ Weather Info</span>
            <span className="feature-tag">🔬 Soil Analysis</span>
            <span className="feature-tag">🏛️ Government Schemes</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
