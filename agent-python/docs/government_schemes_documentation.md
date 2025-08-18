# 🏛️ Government Schemes Agent - Complete Documentation

## Overview

The Government Schemes Agent is an AI-powered system that helps farmers discover, understand, and apply for various government schemes available at central and state levels. It provides personalized recommendations based on farmer profiles, location, and specific needs.

## 🌟 Key Features

### 1. Comprehensive Scheme Database

- **Central Government Schemes**: PM-KISAN, PMFBY, KCC, Soil Health Card
- **State-Specific Schemes**: Maharashtra, Karnataka, Punjab, and more
- **Real-time Updates**: Integration with government APIs (planned)
- **Eligibility Matching**: Automatic filtering based on farmer profile

### 2. Intelligent Recommendation System

- **Profile-Based Filtering**: Matches schemes to farmer type, land size, crops
- **Priority Ranking**: Orders schemes by relevance and benefit amount
- **Need-Based Suggestions**: Credit, insurance, subsidy-specific recommendations
- **AI-Powered Guidance**: Rule-based recommendations with LLM enhancement capability

### 3. Comprehensive Application Support

- **Document Checklists**: Complete list of required documents
- **Step-by-Step Guidance**: Detailed application processes
- **Timeline Management**: Application deadlines and renewal reminders
- **Benefit Calculations**: Estimated annual benefits from schemes

## 🏗️ Architecture

### Core Components

```
government_schemes_agent.py
├── Profile Extraction
├── Scheme Fetching & Filtering
├── AI-Powered Recommendations
└── Comprehensive Guidance Generation

government_schemes_plugin.py
├── Central Scheme Database
├── State Scheme Integration
├── Eligibility Assessment
└── Benefit Calculations
```

### Data Flow

```
User Query → Profile Extraction → Scheme Fetching → AI Analysis → Personalized Recommendations
     ↓              ↓                    ↓              ↓              ↓
Location & Need → Farmer Type → Applicable Schemes → Priority Ranking → Application Guidance
```

## 📋 Scheme Categories

### Central Government Schemes

#### 1. PM-KISAN Samman Nidhi Yojana

- **Type**: Income Support
- **Benefit**: ₹6,000 per year (3 installments of ₹2,000)
- **Eligibility**: Small and marginal farmers (up to 2 hectares)
- **Application**: Online at pmkisan.gov.in or through CSCs

#### 2. Pradhan Mantri Fasal Bima Yojana (PMFBY)

- **Type**: Crop Insurance
- **Benefit**: Comprehensive crop coverage at low premium
- **Premium**: 2% for Kharif, 1.5% for Rabi crops
- **Coverage**: Pre-sowing to post-harvest losses

#### 3. Kisan Credit Card (KCC) Scheme

- **Type**: Credit Support
- **Benefit**: Flexible agricultural credit with personal accident insurance
- **Coverage**: Up to ₹50,000 accident insurance
- **Features**: Conversion facility for term loans

#### 4. Soil Health Card Scheme

- **Type**: Soil Management
- **Benefit**: Free soil testing every 3 years
- **Services**: Fertilizer recommendations, organic matter guidance

### State Government Schemes

#### Maharashtra

- **Mahatma Jyotirao Phule Jan Arogya Yojana**: Health insurance (₹1.5 lakh)
- **Maharashtra Krishi Sanjeevani Yojana**: Climate-resilient agriculture support

#### Karnataka

- **Raitha Bandhu Scheme**: ₹4,000 per acre per season
- **Yashaswini Scheme**: ₹2 lakh health coverage for cooperative members

#### Punjab

- **Punjab Mera Kisan Mitra Scheme**: Digital platform for farmer services
- **Smart Village Programme**: Comprehensive village development

## 🔧 Technical Implementation

### API Integration Framework

```python
# Central Government APIs (Template)
CENTRAL_SCHEME_APIS = {
    "pm_kisan": {
        "url": "https://pmkisan.gov.in/api/schemes",
        "description": "PM-KISAN Samman Nidhi Yojana"
    },
    "pmfby": {
        "url": "https://pmfby.gov.in/api/schemes",
        "description": "Pradhan Mantri Fasal Bima Yojana"
    }
}

# State APIs
STATE_SCHEME_APIS = {
    "maharashtra": "https://agriculture.maharashtra.gov.in/api/schemes",
    "karnataka": "https://agriculture.karnataka.gov.in/api/schemes"
}
```

### Farmer Profile Structure

```python
farmer_profile = {
    "farmer_type": "small",      # small, marginal, medium, large
    "crop_type": "rice",         # specific crop or all
    "land_size": 2.5,            # in acres
    "annual_income": 50000,      # estimated annual income
    "primary_need": "credit",    # credit, insurance, subsidy, general
    "state": "Maharashtra",      # for state-specific schemes
    "education_level": "primary" # for appropriate communication
}
```

### Eligibility Scoring Algorithm

```python
def calculate_eligibility_score(scheme: dict, farmer_profile: dict) -> float:
    score = 5.0  # Base score

    # Farmer type match bonus
    if farmer_type in scheme["farmer_category"]:
        score += 2.0

    # Land size compatibility
    if land_size <= 2 and "small" in scheme["farmer_category"]:
        score += 1.5

    # Scheme type relevance
    if "income" in scheme["scheme_type"].lower():
        score += 1.0

    return min(score, 10.0)
```

## 🎯 Usage Examples

### Basic Usage

```python
from graph_arc.state import GlobalState
from graph_arc.agents_node.government_schemes_agent import government_schemes_agent

# Create state with user query and location
state = GlobalState(
    user_query="What government schemes are available for small farmers?",
    location="Mumbai",
    entities={"farmer_type": "small", "crop": "rice"},
    weather_data={"temperature": 28, "humidity": 75}
)

# Get scheme recommendations
result = government_schemes_agent(state)

# Access results
schemes = result["relevant_schemes"]
eligibility = result["eligibility"]
guidance = result["application_steps"]
```

### Direct Plugin Usage

```python
from plugins.government_schemes_plugin import get_schemes_by_location_and_profile

farmer_profile = {
    "farmer_type": "marginal",
    "crop_type": "cotton",
    "land_size": 1.8,
    "primary_need": "insurance"
}

schemes_data = get_schemes_by_location_and_profile("Bangalore", farmer_profile)

print(f"Total schemes: {schemes_data['total_schemes']}")
print(f"Estimated benefits: ₹{schemes_data['estimated_benefits']['estimated_annual_benefit']}")
```

## 📊 Testing Framework

### Comprehensive Test Suite

```bash
# Run all tests
python tests/test_government_schemes.py

# Run with real API tests (when available)
RUN_REAL_API_TESTS=1 python tests/test_government_schemes.py

# Test flow demonstration
python test_government_schemes_flow.py
```

### Test Categories

1. **Unit Tests**: Individual function testing
2. **Integration Tests**: Complete workflow testing
3. **Mock Tests**: Simulated API responses
4. **Real API Tests**: Live government portal integration (when available)

## 💰 Benefit Calculations

### Estimated Annual Benefits

The system calculates estimated benefits based on:

- **PM-KISAN**: ₹6,000 for eligible farmers
- **State Income Schemes**: ₹3,000 average per scheme
- **Land-based Benefits**: ₹1,000 per acre from various schemes
- **Insurance Coverage**: Risk mitigation value
- **Credit Access**: Interest savings and loan availability

### Example Calculations

```
Small Farmer (2 acres, Maharashtra):
- PM-KISAN: ₹6,000
- State schemes: ₹6,000 (2 schemes × ₹3,000)
- Land-based: ₹2,000 (2 acres × ₹1,000)
- Total Estimated: ₹14,000 per year
```

## 🌍 Multi-State Support

### Supported States

- **Maharashtra**: Comprehensive scheme database
- **Karnataka**: Raitha Bandhu and health schemes
- **Punjab**: Digital agriculture initiatives
- **Delhi**: NCR-specific programs
- **Generic**: Fallback schemes for other states

### State-Specific Features

- **Local Language Support**: Regional language content (planned)
- **Cultural Context**: State-specific farming practices
- **Regional Crops**: State-appropriate crop recommendations
- **Local Contacts**: State agriculture department information

## 🚀 Future Enhancements

### Planned Features

1. **Real-time API Integration**

   - Live government portal connections
   - Real-time application status tracking
   - Automatic eligibility verification

2. **Advanced AI Features**

   - ML-based approval prediction
   - Optimal application timing recommendations
   - Fraud detection and prevention

3. **Enhanced User Experience**

   - Multilingual support (Hindi, Telugu, Tamil, etc.)
   - Voice-based assistance
   - WhatsApp/Telegram chatbot integration

4. **Document Management**

   - OCR-based document validation
   - Auto-generation of application forms
   - DigiLocker integration

5. **Monitoring & Analytics**
   - IoT-based farm monitoring
   - Satellite land verification
   - Impact analysis and reporting

## 📱 Integration Points

### Mobile App Integration

```javascript
// React Native / Flutter integration
const getGovernmentSchemes = async (farmerProfile) => {
  const response = await fetch("/api/government-schemes", {
    method: "POST",
    body: JSON.stringify(farmerProfile),
  });
  return response.json();
};
```

### WhatsApp Bot Integration

```python
# WhatsApp webhook for scheme queries
@app.route('/whatsapp-webhook', methods=['POST'])
def handle_whatsapp_message():
    message = request.json['message']
    farmer_location = extract_location(message)
    schemes = get_applicable_schemes(farmer_location)
    return send_whatsapp_response(schemes)
```

## 🔒 Security & Privacy

### Data Protection

- **Farmer Privacy**: Minimal data collection, secure storage
- **Government Compliance**: Adherence to Digital India guidelines
- **Encryption**: All API communications encrypted
- **Access Control**: Role-based access for different user types

### Authentication

- **Aadhaar Integration**: Secure farmer identity verification
- **OTP Verification**: Mobile number validation
- **Document Security**: Encrypted document storage

## 📞 Support & Contacts

### Help Resources

- **CSC Centers**: Common Service Center locations
- **Agriculture Offices**: Local government contacts
- **Helpline Numbers**: State-specific support numbers
- **Online Portals**: Direct links to government websites

### Troubleshooting

- **Application Issues**: Step-by-step resolution guides
- **Document Problems**: Alternative document options
- **Technical Support**: System error handling

## 🏆 Success Metrics

### Key Performance Indicators

- **Scheme Awareness**: Number of farmers informed about schemes
- **Application Success Rate**: Percentage of successful applications
- **Benefit Realization**: Total benefits accessed by farmers
- **User Satisfaction**: Feedback and rating scores

### Impact Measurement

- **Financial Impact**: Total scheme benefits distributed
- **Coverage**: Percentage of eligible farmers reached
- **Efficiency**: Time saved in application processes
- **Transparency**: Reduction in corruption and delays

---

## 🤝 Contributing

### Development Setup

```bash
# Clone repository
git clone <repository-url>
cd agent-python

# Install dependencies
pip install -r requirements.txt

# Run tests
python src/tests/test_government_schemes.py

# Start development server
python src/main.py
```

### Adding New Schemes

1. Update scheme database in `government_schemes_plugin.py`
2. Add eligibility criteria and benefit calculations
3. Include state-specific variations
4. Add comprehensive tests
5. Update documentation

### API Integration

1. Add new API endpoints to `CENTRAL_SCHEME_APIS` or `STATE_SCHEME_APIS`
2. Implement authentication and error handling
3. Add data mapping and validation
4. Include rate limiting and caching
5. Test with mock and real data

---

_Built with 🏛️ for transparent governance and farmer empowerment through technology._
