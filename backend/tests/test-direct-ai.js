const WebSocket = require('ws');

console.log('🐍 Direct Python AI Server Test (via Docker)');
console.log('==========================================');

// Connect directly to Python AI server
const ws = new WebSocket('ws://localhost:8000/ws/direct_test_user');

ws.on('open', () => {
    console.log('✅ Connected directly to Python AI server');
    console.log('📝 Sending agricultural query...');
    
    // Send a detailed agricultural query
    const query = {
        raw_query: 'मेरे खेत में गेहूं की फसल में पीले पत्ते दिख रहे हैं। दिल्ली में मिट्टी काली है। मुझे क्या करना चाहिए?',
        language: 'hi',
        user_id: 'direct_test_user'
    };
    
    ws.send(JSON.stringify(query));
});

ws.on('message', (data) => {
    try {
        const response = JSON.parse(data.toString());
        console.log('🤖 Direct AI Response:');
        console.log('═'.repeat(80));
        
        if (response.type === 'agricultural_response') {
            console.log('📊 Response Type:', response.type);
            console.log('✅ Success:', response.success);
            
            if (response.data) {
                console.log('🌾 Final Advice:', response.data.final_advice || 'N/A');
                console.log('📍 Location:', response.data.location || 'N/A');
                console.log('🎯 Detected Intents:', response.data.detected_intents || []);
                
                if (response.data.translated_response) {
                    console.log('🇮🇳 Hindi Response:', response.data.translated_response);
                }
                
                if (response.data.soil_data) {
                    console.log('🌱 Soil Info:', response.data.soil_data.soil_type || 'N/A');
                }
                
                if (response.data.weather_data) {
                    console.log('🌤️ Weather:', response.data.weather_data.temperature || 'N/A');
                }
            }
        } else {
            console.log('📄 Raw Response:', JSON.stringify(response, null, 2));
        }
        
        console.log('═'.repeat(80));
        console.log('✅ Direct Python AI test completed!');
        
    } catch (error) {
        console.log('❌ Error parsing response:', error.message);
        console.log('Raw data:', data.toString());
    }
    
    ws.close();
});

ws.on('error', (error) => {
    console.log('❌ WebSocket error:', error.message);
});

ws.on('close', () => {
    console.log('🔌 Connection closed');
    process.exit(0);
});

// Timeout after 30 seconds
setTimeout(() => {
    console.log('⏰ Test timeout');
    ws.close();
    process.exit(1);
}, 30000);
