const io = require('socket.io-client');

console.log('🌾 Testing Agricultural AI Query...');

const socket = io('http://localhost:5000');

socket.on('connect', () => {
    console.log('✅ Connected to FarmMate System');
    console.log('📝 Asking about crop recommendations...');
    
    socket.emit('user_query', {
        query: 'दिल्ली में अभी कौन सी फसल लगाई जा सकती है? मिट्टी का pH 7.2 है।',
        language: 'hi',
        userId: 'farmer_delhi_001'
    });
});

socket.on('ai_response', (response) => {
    console.log('🤖 FarmMate AI Response:');
    console.log('===================================');
    console.log(response.message);
    console.log('===================================');
    console.log('✅ Complete agricultural consultation delivered!');
    process.exit(0);
});

socket.on('error', (error) => {
    console.log('❌ Error:', error);
});

// Timeout after 20 seconds
setTimeout(() => {
    console.log('⏰ Response time exceeded');
    process.exit(1);
}, 20000);
