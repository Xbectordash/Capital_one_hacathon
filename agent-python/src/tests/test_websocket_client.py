#!/usr/bin/env python3
"""
Test Client for Agricultural AI Assistant WebSocket
"""
import asyncio
import json
import websockets
import uuid

class AgriculturalChatClient:
    def __init__(self, server_url="ws://localhost:8000"):
        self.server_url = server_url
        self.user_id = f"test-user-{uuid.uuid4().hex[:8]}"
        self.websocket = None

    async def connect(self):
        """Connect to the WebSocket server"""
        try:
            self.websocket = await websockets.connect(f"{self.server_url}/ws/{self.user_id}")
            print(f"🔗 Connected to server as user: {self.user_id}")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False

    async def send_query(self, query: str, language: str = "hi", location: str = None):
        """Send agricultural query to the server"""
        if not self.websocket:
            print("❌ Not connected to server")
            return

        message = {
            "raw_query": query,
            "language": language
        }
        
        if location:
            message["location"] = location

        try:
            await self.websocket.send(json.dumps(message))
            print(f"📤 Sent query: {query}")
        except Exception as e:
            print(f"❌ Failed to send message: {e}")

    async def listen_for_responses(self):
        """Listen for responses from the server"""
        if not self.websocket:
            return

        try:
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    self.handle_response(data)
                except json.JSONDecodeError:
                    print(f"❌ Invalid JSON received: {message}")
        except websockets.exceptions.ConnectionClosed:
            print("🔌 Connection closed by server")
        except Exception as e:
            print(f"❌ Error receiving messages: {e}")

    def handle_response(self, data):
        """Handle different types of responses from server"""
        message_type = data.get("type", "unknown")
        
        if message_type == "connection_established":
            print(f"✅ {data.get('message', 'Connected')}")
            
        elif message_type == "message_received":
            print(f"📨 Server acknowledged: {data.get('message', 'Message received')}")
            
        elif message_type == "status_update":
            status = data.get("status", "unknown")
            stage = data.get("details", {}).get("stage", "")
            print(f"⏳ Status: {status} - {stage}")
            
        elif message_type == "agricultural_response":
            print(f"\n🌾 Agricultural Response:")
            print(f"   Success: {data.get('success', False)}")
            print(f"   Processing Time: {data.get('processing_time', 0):.2f}s")
            
            if data.get("success"):
                response_data = data.get("data", {})
                print(f"   Query: {response_data.get('query', 'N/A')}")
                print(f"   Location: {response_data.get('location', 'N/A')}")
                print(f"   Detected Intents: {', '.join(response_data.get('detected_intents', []))}")
                
                # Show final advice
                if response_data.get("translated_response"):
                    print(f"\n   💡 सलाह: {response_data.get('translated_response', 'N/A')[:200]}...")
                elif response_data.get("final_advice"):
                    print(f"\n   💡 Advice: {response_data.get('final_advice', 'N/A')[:200]}...")
                    
            else:
                print(f"   Error: {data.get('error', 'Unknown error')}")
                
        elif message_type == "error":
            print(f"❌ Error: {data.get('message', 'Unknown error')}")
            
        else:
            print(f"📩 Received: {data}")

    async def close(self):
        """Close the WebSocket connection"""
        if self.websocket:
            await self.websocket.close()
            print("🔌 Disconnected from server")

async def run_interactive_client():
    """Run interactive client for testing"""
    client = AgriculturalChatClient()
    
    # Connect to server
    if not await client.connect():
        return

    print("\n🌾 Agricultural AI Assistant - Interactive Test Client")
    print("=" * 60)
    print("Type your agricultural queries in Hindi or English.")
    print("Examples:")
    print("  - What is the weather forecast for next week?")
    print("  - मिट्टी का विश्लेषण कैसे करें?")
    print("  - What government schemes are available for farmers?")
    print("Type 'quit' to exit.")
    print("=" * 60)

    # Start listening for responses in background
    response_task = asyncio.create_task(client.listen_for_responses())

    try:
        while True:
            # Get user input
            query = input("\n🌱 Your Query: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                break
                
            if query:
                await client.send_query(query)
            
            # Small delay to see responses
            await asyncio.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n\n⚡ Interrupted by user")
    
    finally:
        response_task.cancel()
        await client.close()

async def run_sample_queries():
    """Run predefined sample queries for testing"""
    client = AgriculturalChatClient()
    
    if not await client.connect():
        return

    # Start listening for responses
    response_task = asyncio.create_task(client.listen_for_responses())

    sample_queries = [
        "What is the weather forecast for the next week?",
        "मिट्टी का विश्लेषण कैसे करें?",
        "What government schemes are available for small farmers?",
        "My wheat crop has yellow leaves, what should I do?",
        "What are current market prices for rice?"
    ]

    print("\n🧪 Running Sample Queries...")
    print("=" * 50)

    for i, query in enumerate(sample_queries, 1):
        print(f"\n📝 Query {i}: {query}")
        await client.send_query(query)
        await asyncio.sleep(15)  # Wait for response

    print("\n✅ Sample queries completed!")
    response_task.cancel()
    await client.close()

if __name__ == "__main__":
    print("🌾 Agricultural AI Assistant - Test Client")
    print("Choose mode:")
    print("1. Interactive mode")
    print("2. Sample queries")
    
    try:
        choice = input("Enter choice (1/2): ").strip()
        
        if choice == "1":
            asyncio.run(run_interactive_client())
        elif choice == "2":
            asyncio.run(run_sample_queries())
        else:
            print("Invalid choice. Running interactive mode...")
            asyncio.run(run_interactive_client())
            
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
