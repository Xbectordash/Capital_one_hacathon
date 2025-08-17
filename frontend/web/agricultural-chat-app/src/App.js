import React, { useState, useEffect, useRef } from 'react';
import io from 'socket.io-client';
import { useLanguage } from './contexts/LanguageContext';
import LanguageSelector from './components/LanguageSelector';
import './App.css';

// Use environment variables for production deployment
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || process.env.REACT_APP_SOCKET_URL || 'http://localhost:5000';

// Debug logging
console.log('🔍 Debug Info:');
console.log('REACT_APP_BACKEND_URL:', process.env.REACT_APP_BACKEND_URL);
console.log('REACT_APP_SOCKET_URL:', process.env.REACT_APP_SOCKET_URL);
console.log('Final BACKEND_URL:', BACKEND_URL);
console.log('NODE_ENV:', process.env.NODE_ENV);

function App() {
  const { currentLanguage, changeLanguage, t, isRTL } = useLanguage();
  const [socket, setSocket] = useState(null);
  const [connected, setConnected] = useState(false);
  const [messages, setMessages] = useState([]);
  const [query, setQuery] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const chatContainerRef = useRef(null);

  // Initialize welcome message based on current language
  useEffect(() => {
    setMessages([
      {
        id: 1,
        sender: t('aiAssistant'),
        message: t('welcomeMessage'),
        type: 'ai',
        timestamp: new Date().toLocaleTimeString()
      }
    ]);
  }, [currentLanguage, t]);

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
      
      // Enhanced response handling for comprehensive format
      let displayMessage = response.message || response.response || JSON.stringify(response);
      
      // Check if it's a comprehensive response
      if (response.comprehensive) {
        console.log('📊 Received comprehensive agricultural response');
        // The message is already formatted from the backend, display as-is
        addMessage(
          t('aiAssistant'),
          displayMessage,
          'ai-comprehensive'
        );
      } else {
        // Regular response handling
        addMessage(
          t('aiAssistant'),
          displayMessage,
          'ai'
        );
      }
    });

    newSocket.on('ai_status', (statusData) => {
      // Handle status updates from the server
      addMessage(
        t('aiAssistant'),
        statusData.message,
        'status'
      );
    });

    newSocket.on('error', (error) => {
      setIsProcessing(false);
      addMessage(t('error'), error.message || t('errors.serverError'), 'ai');
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
    addMessage(t('user'), query, 'user');

    // Send to server
    socket.emit('user_query', {
      query: query.trim(),
      language: currentLanguage,
      userId: socket.id
    });

    setQuery('');
    setIsProcessing(true);
    
    // Add processing message
    setTimeout(() => {
      addMessage(t('processing'), t('processingMessage'), 'ai');
    }, 100);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendQuery();
    }
  };

  return (
    <div className={`App ${isRTL() ? 'rtl' : 'ltr'}`} dir={isRTL() ? 'rtl' : 'ltr'}>
      <div className="container">
        <h1>{t('appTitle')}</h1>
        
        <div className={`status ${connected ? 'connected' : 'disconnected'}`}>
          {connected ? t('connected') : t('connecting')}
        </div>
        
        <LanguageSelector disabled={isProcessing} />
        
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
            placeholder={t('inputPlaceholder')}
            disabled={!connected || isProcessing}
          />
          <button 
            onClick={sendQuery}
            disabled={!connected || !query.trim() || isProcessing}
          >
            {isProcessing ? t('sendingButton') : t('sendButton')}
          </button>
        </div>
        
        <div className="features-info">
          <h3>{t('featuresTitle')}</h3>
          <div className="feature-list">
            <span className="feature-tag">{t('features.cropManagement')}</span>
            <span className="feature-tag">{t('features.marketPrices')}</span>
            <span className="feature-tag">{t('features.weatherInfo')}</span>
            <span className="feature-tag">{t('features.soilAnalysis')}</span>
            <span className="feature-tag">{t('features.governmentSchemes')}</span>
          </div>
        </div>

        <div className="sample-questions">
          <h3>{t('sampleQuestions.title')}</h3>
          <div className="questions-list">
            {t('sampleQuestions.questions').map((question, index) => (
              <button
                key={index}
                className="sample-question-btn"
                onClick={() => setQuery(question)}
                disabled={isProcessing || !connected}
              >
                {question}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
