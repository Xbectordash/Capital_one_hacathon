const io = require('socket.io-client');

console.log('🌾 Testing FarmMate Three-Tier Communication...');

// Connect to Express Gateway
const socket = io('http://localhost:5000');

socket.on('connect', () => {
    console.log('✅ Connected to Express Gateway (Socket.IO)');
    console.log('📝 Sending agricultural query...');
    
    // Send a test query
    socket.emit('user_query', {
        query: 'मुझे दिल्ली में कौन सी फसल लगानी चाहिए?',
        language: 'hi',
        userId: 'test_user_123'
    });
});

socket.on('ai_response', (response) => {
    console.log('🤖 AI Response received:');
    console.log('-----------------------------------');
    console.log(response.message);
    console.log('-----------------------------------');
    console.log('✅ Three-tier communication successful!');
    process.exit(0);
});

socket.on('error', (error) => {
    console.log('❌ Error:', error);
});

socket.on('disconnect', () => {
    console.log('🔌 Disconnected from server');
});

// Timeout after 30 seconds
setTimeout(() => {
    console.log('⏰ Test timeout - taking too long');
    process.exit(1);
}, 30000);
