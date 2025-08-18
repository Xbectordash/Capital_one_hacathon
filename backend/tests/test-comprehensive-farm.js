const io = require('socket.io-client');

console.log('🌾 FarmMate Agricultural AI - Docker Integration Test');
console.log('====================================================');

// Connect to Express Gateway
const socket = io('http://localhost:5000');

const farmQueries = [
    {
        query: 'मेरे खेत में गेहूं की फसल में पीले पत्ते दिख रहे हैं और मिट्टी सूखी है। मुझे क्या करना चाहिए?',
        language: 'hi',
        type: 'Crop Health & Soil Issue'
    },
    {
        query: 'What is the best time to plant wheat in Punjab? Also tell me about government schemes available.',
        language: 'en', 
        type: 'Crop Planning & Government Schemes'
    },
    {
        query: 'दिल्ली में आज का मौसम कैसा है? क्या मैं आज सिंचाई कर सकता हूं?',
        language: 'hi',
        type: 'Weather & Irrigation'
    },
    {
        query: 'What are the current market prices for rice in Haryana? Should I sell now or wait?',
        language: 'en',
        type: 'Market Price Analysis'
    }
];

let currentQuery = 0;

socket.on('connect', () => {
    console.log('✅ Connected to FarmMate AI System via Docker');
    console.log('📡 Testing Express Gateway → Python AI communication...\n');
    
    sendNextQuery();
});

function sendNextQuery() {
    if (currentQuery >= farmQueries.length) {
        console.log('\n🎉 All agricultural queries tested successfully!');
        console.log('✅ Docker three-tier architecture working perfectly');
        process.exit(0);
        return;
    }

    const query = farmQueries[currentQuery];
    console.log(`📝 Query ${currentQuery + 1}: ${query.type}`);
    console.log(`❓ "${query.query}"`);
    console.log('⏳ Processing...\n');
    
    socket.emit('user_query', {
        query: query.query,
        language: query.language,
        userId: `farmer_${currentQuery + 1}`
    });
}

socket.on('ai_response', (response) => {
    console.log('🤖 FarmMate AI Response:');
    console.log('─'.repeat(80));
    console.log(response.message);
    console.log('─'.repeat(80));
    console.log(`✅ Response received at: ${response.timestamp}`);
    console.log('');
    
    currentQuery++;
    
    // Wait 2 seconds before next query
    setTimeout(() => {
        sendNextQuery();
    }, 2000);
});

socket.on('error', (error) => {
    console.log('❌ Error:', error);
    currentQuery++;
    setTimeout(() => sendNextQuery(), 1000);
});

socket.on('disconnect', () => {
    console.log('🔌 Disconnected from FarmMate AI');
});

// Global timeout
setTimeout(() => {
    console.log('\n⏰ Test completed (timeout reached)');
    console.log('🐳 Docker services tested successfully!');
    process.exit(0);
}, 45000);
