#!/usr/bin/env python3
"""
FarmMate AI Terminal Application
Enhanced agricultural assistant with CSV-based soil analysis, weather data, and crop recommendations.
"""

import sys
import os
import json
from pathlib import Path

# Add the src directory to Python path
project_root = Path(__file__).resolve().parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

try:
    from src.graph_arc.graph import workflow
    from src.data.soil_plugins import get_soil_data_from_csv
    from src.data.weather_plugins import fetch_weather_data
    from src.utils.loggers import get_logger
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Make sure you're running from the agent-python directory and all dependencies are installed.")
    sys.exit(1)

# Configure logging
logger = get_logger("terminal_app")

class FarmMateTerminalApp:
    """Enhanced FarmMate AI Terminal Application with CSV soil data"""
    
    def __init__(self):
        self.logger = get_logger("FarmMateApp")
        self.session_data = {
            "user_name": None,
            "default_location": None,
            "query_count": 0,
            "soil_cache": {},
            "weather_cache": {}
        }
        
    def print_banner(self):
        """Display the FarmMate banner"""
        banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                            🌾 FARMMATE AI 🌾                                 ║
║                     Your Intelligent Agricultural Assistant                   ║
║                                                                              ║
║  🚀 Enhanced with CSV-based Soil Analysis                                   ║
║  🌡️  Real-time Weather Integration                                          ║
║  🌱 Smart Crop Recommendations                                               ║
║  💰 Market Price Intelligence                                                ║
║  🏛️  Government Scheme Guidance                                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
        print(banner)
        print("Welcome to FarmMate AI - Your agricultural companion!")
        print("Type 'help' for commands, 'quit' to exit\n")
        
    def setup_user_profile(self):
        """Set up user profile for personalized experience"""
        print("🔧 Let's set up your profile for better recommendations:\n")
        
        # Get user name
        name = input("👤 What's your name? (optional): ").strip()
        if name:
            self.session_data["user_name"] = name
            print(f"Nice to meet you, {name}! 👋")
        
        # Get default location
        location = input("📍 What's your primary farming location? (e.g., Delhi, Punjab): ").strip()
        if location:
            self.session_data["default_location"] = location
            print(f"Setting {location} as your default location. 📍")
            
            # Test soil data for the location
            try:
                print(f"\n🔍 Checking soil data for {location}...")
                soil_data = get_soil_data_from_csv(location, "profile setup")
                
                print(f"✅ Soil data found!")
                print(f"   📊 Data Source: {soil_data.get('data_source', 'Unknown')}")
                print(f"   🏷️  Soil Type: {soil_data.get('soil_type', 'Unknown')}")
                print(f"   ⚡ Health Score: {soil_data.get('quality_score', 'Unknown')}")
                
                # Cache the soil data
                self.session_data["soil_cache"][location] = soil_data
                
            except Exception as e:
                print(f"⚠️  Could not load soil data: {e}")
                print("Don't worry, you can still ask agricultural questions!")
        
        print("\n" + "="*50)
        print("🎉 Profile setup complete! Let's start farming smarter!")
        print("="*50 + "\n")
        
    def show_help(self):
        """Display help information"""
        help_text = """
🆘 FARMMATE AI HELP GUIDE

📝 HOW TO ASK QUESTIONS:
• "What crops should I grow in Punjab?"
• "Soil analysis for Delhi"
• "Weather forecast for my location"
• "Cotton farming tips"
• "Government schemes for farmers"
• "Market price of wheat"

⚡ QUICK COMMANDS:
• help        - Show this help
• profile     - Update your profile
• soil        - Quick soil analysis for your location
• weather     - Get weather for your location
• examples    - Show example queries
• stats       - Show session statistics
• clear       - Clear screen
• quit/exit   - Exit FarmMate

🌟 FEATURES:
• CSV-based soil nutrient analysis (Zn, Fe, Cu, Mn, B, S)
• Real-time weather data integration
• Crop recommendations based on soil + weather
• Government scheme information
• Market price insights
• Multilingual support

💡 TIP: Be specific about your location for better recommendations!
        """
        print(help_text)
        
    def show_examples(self):
        """Show example queries"""
        examples = """
📚 EXAMPLE QUERIES:

🌱 CROP RECOMMENDATIONS:
• "Best crops for black cotton soil in Maharashtra"
• "What to grow in Delhi during winter season"
• "Crop suggestions for my sandy loam soil"

🧪 SOIL ANALYSIS:
• "Soil analysis for Bangalore"
• "Zinc deficiency in my soil, what to do?"
• "How to improve soil fertility in Punjab"

🌦️ WEATHER & FARMING:
• "Weather forecast for farming in Gujarat"
• "When to plant rice based on weather"
• "Irrigation planning for next week"

💰 MARKET & SCHEMES:
• "Current wheat prices in my area"
• "Government subsidies for organic farming"
• "Best time to sell cotton"

🐛 CROP HEALTH:
• "Pest control for tomato plants"
• "Disease prevention in rice crops"
• "Organic farming techniques"
        """
        print(examples)
        
    def show_stats(self):
        """Show session statistics"""
        stats = f"""
📊 SESSION STATISTICS:

👤 User: {self.session_data.get('user_name', 'Anonymous')}
📍 Default Location: {self.session_data.get('default_location', 'Not set')}
🔢 Queries Asked: {self.session_data['query_count']}
💾 Soil Data Cached: {len(self.session_data['soil_cache'])} locations
🌤️ Weather Data Cached: {len(self.session_data['weather_cache'])} locations

🎯 QUICK ACTIONS:
• Type 'soil' for quick soil analysis
• Type 'weather' for current weather
• Type 'profile' to update your location
        """
        print(stats)
        
    def quick_soil_analysis(self):
        """Quick soil analysis for user's default location"""
        location = self.session_data.get("default_location")
        
        if not location:
            location = input("📍 Enter location for soil analysis: ").strip()
            if not location:
                print("❌ Location is required for soil analysis.")
                return
                
        print(f"\n🔍 Analyzing soil for {location}...")
        print("⏳ Processing CSV soil data...")
        
        try:
            # Check cache first
            if location in self.session_data["soil_cache"]:
                soil_data = self.session_data["soil_cache"][location]
                print("📋 Using cached soil data")
            else:
                soil_data = get_soil_data_from_csv(location, "quick soil analysis")
                self.session_data["soil_cache"][location] = soil_data
                
            # Display results
            self.display_soil_results(soil_data)
            
        except Exception as e:
            print(f"❌ Soil analysis failed: {e}")
            print("💡 Try asking: 'soil analysis for [your location]'")
            
    def display_soil_results(self, soil_data):
        """Display formatted soil analysis results"""
        print("\n" + "="*60)
        print("🧪 SOIL ANALYSIS RESULTS")
        print("="*60)
        
        print(f"📍 Location: {soil_data.get('location', 'Unknown')}")
        print(f"📊 Data Source: {soil_data.get('data_source', 'Unknown')}")
        print(f"⭐ Quality Score: {soil_data.get('quality_score', 'Unknown')}")
        
        print(f"\n🏷️  SOIL PROPERTIES:")
        print(f"   • Soil Type: {soil_data.get('soil_type', 'Unknown')}")
        print(f"   • pH Level: {soil_data.get('ph', 'Unknown')}")
        print(f"   • Fertility: {soil_data.get('fertility_status', 'Unknown')}")
        
        # Micronutrient status (from CSV)
        nutrients = ['zinc_status', 'iron_status', 'copper_status', 'manganese_status', 'boron_status', 'sulfur_status']
        nutrient_data = [soil_data.get(n, 'N/A') for n in nutrients if soil_data.get(n, 'N/A') != 'N/A']
        
        if nutrient_data:
            print(f"\n🧪 MICRONUTRIENT STATUS:")
            if soil_data.get('zinc_status'): print(f"   • Zinc (Zn): {soil_data['zinc_status']}")
            if soil_data.get('iron_status'): print(f"   • Iron (Fe): {soil_data['iron_status']}")
            if soil_data.get('copper_status'): print(f"   • Copper (Cu): {soil_data['copper_status']}")
            if soil_data.get('manganese_status'): print(f"   • Manganese (Mn): {soil_data['manganese_status']}")
            if soil_data.get('boron_status'): print(f"   • Boron (B): {soil_data['boron_status']}")
            if soil_data.get('sulfur_status'): print(f"   • Sulfur (S): {soil_data['sulfur_status']}")
        
        print(f"\n🌱 RECOMMENDED CROPS:")
        crops = soil_data.get('recommended_crops', [])
        if isinstance(crops, list) and crops:
            for i, crop in enumerate(crops[:6], 1):
                print(f"   {i}. {crop}")
        else:
            print("   • No specific recommendations available")
            
        print(f"\n💧 IRRIGATION GUIDANCE:")
        irrigation = soil_data.get('irrigation_guidance', 'Standard irrigation practices recommended')
        print(f"   {irrigation}")
        
        if soil_data.get('fertilizer_recommendations'):
            print(f"\n🌿 FERTILIZER RECOMMENDATIONS:")
            print(f"   {soil_data['fertilizer_recommendations']}")
        
        print("="*60)
        
    def quick_weather_check(self):
        """Quick weather check for user's default location"""
        location = self.session_data.get("default_location")
        
        if not location:
            location = input("📍 Enter location for weather check: ").strip()
            if not location:
                print("❌ Location is required for weather check.")
                return
                
        print(f"\n🌤️ Checking weather for {location}...")
        
        try:
            # Check cache first
            if location in self.session_data["weather_cache"]:
                weather_data = self.session_data["weather_cache"][location]
                print("📋 Using cached weather data")
            else:
                weather_data = fetch_weather_data(location)
                self.session_data["weather_cache"][location] = weather_data
                
            # Display weather
            print(f"\n🌡️ Temperature: {weather_data.get('temperature', 'Unknown')}°C")
            print(f"💧 Humidity: {weather_data.get('humidity', 'Unknown')}%")
            print(f"🌤️ Conditions: {weather_data.get('description', 'Unknown')}")
            
            if weather_data.get('wind_speed'):
                print(f"💨 Wind Speed: {weather_data['wind_speed']} km/h")
                
        except Exception as e:
            print(f"❌ Weather check failed: {e}")
            print("💡 Try asking: 'weather for [your location]'")
            
    def process_query(self, query):
        """Process user query using the FarmMate workflow"""
        self.session_data["query_count"] += 1
        
        print(f"\n🤔 Processing: {query}")
        print("⏳ Analyzing with FarmMate AI...")
        
        try:
            # Create initial state for the workflow
            initial_state = {
                "user_id": "terminal_user",
                "raw_query": query,
                "language": "en"  # Default to English for terminal
            }
            
            # Use the workflow to process the query
            result = workflow.invoke(initial_state)
            
            # Extract the response from the result
            if result.get("decision"):
                response = result["decision"].get("final_advice", "No advice available")
                explanation = result["decision"].get("explanation", "")
            else:
                response = "I couldn't process your query. Please try rephrasing it."
                explanation = ""
            
            print("\n" + "="*60)
            print("🤖 FARMMATE AI RESPONSE")
            print("="*60)
            print(response)
            
            if explanation:
                print("\n" + "-"*40)
                print("📋 DETAILED EXPLANATION:")
                print("-"*40)
                print(explanation)
            
            print("="*60)
            
        except Exception as e:
            self.logger.error(f"Query processing failed: {e}")
            print(f"❌ Sorry, I couldn't process that query: {e}")
            print("💡 Try rephrasing your question or use 'help' for guidance.")
            
    def run(self):
        """Main application loop"""
        try:
            self.print_banner()
            print("� Type 'profile' to set up your location, 'help' for commands, or ask any farming question!\n")
            
            # Main loop
            while True:
                try:
                    # Get user input
                    if self.session_data.get("user_name"):
                        prompt = f"🌾 {self.session_data['user_name']} > "
                    else:
                        prompt = "🌾 FarmMate > "
                        
                    user_input = input(prompt).strip()
                    
                    if not user_input:
                        continue
                        
                    # Handle commands
                    command = user_input.lower()
                    
                    if command in ['quit', 'exit', 'bye']:
                        print("\n🙏 Thank you for using FarmMate AI!")
                        print("🌱 Happy farming! May your crops grow well!")
                        break
                        
                    elif command == 'help':
                        self.show_help()
                        
                    elif command == 'examples':
                        self.show_examples()
                        
                    elif command == 'stats':
                        self.show_stats()
                        
                    elif command == 'profile':
                        self.setup_user_profile()
                        
                    elif command == 'soil':
                        self.quick_soil_analysis()
                        
                    elif command == 'weather':
                        self.quick_weather_check()
                        
                    elif command == 'clear':
                        os.system('cls' if os.name == 'nt' else 'clear')
                        self.print_banner()
                        
                    else:
                        # Process as FarmMate query
                        # Add user's default location context if available
                        if self.session_data.get("default_location"):
                            if "location" not in user_input.lower() and "in " not in user_input.lower():
                                enhanced_query = f"{user_input} in {self.session_data['default_location']}"
                            else:
                                enhanced_query = user_input
                        else:
                            enhanced_query = user_input
                            
                        self.process_query(enhanced_query)
                        
                except KeyboardInterrupt:
                    print("\n\n⚠️  Interrupted by user")
                    continue
                except Exception as e:
                    self.logger.error(f"Unexpected error in main loop: {e}")
                    print(f"❌ An unexpected error occurred: {e}")
                    print("💡 Please try again or type 'help' for assistance.")
                    
        except KeyboardInterrupt:
            print("\n\n🙏 Thank you for using FarmMate AI!")
            print("🌱 Happy farming!")
        except Exception as e:
            self.logger.error(f"Critical error in terminal app: {e}")
            print(f"❌ Critical error: {e}")
            print("Please check your setup and try again.")


def main():
    """Main entry point"""
    print("🚀 Starting FarmMate AI Terminal Application...")
    
    # Check if we're in the right directory
    if not os.path.exists("src"):
        print("❌ Error: Please run this script from the agent-python directory")
        print("Current directory should contain the 'src' folder")
        sys.exit(1)
        
    # Initialize and run the app
    app = FarmMateTerminalApp()
    app.run()


if __name__ == "__main__":
    main()
