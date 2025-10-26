# 🚀 Hybrid Crypto Trading Bot Dashboard MVP

A complete MVP for a **Crypto Trading Bot Dashboard** that integrates existing **Clojure crypto infrastructure** with a **Python (FastAPI + WebSocket)** backend and **React + Tailwind** frontend.

## 🏗️ Hybrid Architecture

This system leverages the existing Clojure crypto infrastructure while providing a modern Python/React interface:

```
┌─────────────────────────────────────────────────────────────────┐
│                    HYBRID CRYPTO TRADING SYSTEM                 │
├─────────────────────────────────────────────────────────────────┤
│  React Frontend (Port 3000)                                     │
│  ├── Real-time Dashboard                                        │
│  ├── Price Charts & Indicators                                  │
│  └── Trading Signals & Risk Controls                           │
├─────────────────────────────────────────────────────────────────┤
│  Python FastAPI Backend (Port 8000)                             │
│  ├── REST API Endpoints                                         │
│  ├── WebSocket Streaming                                        │
│  ├── Technical Analysis (RSI, ADX, ATR)                        │
│  ├── Sentiment Analysis (FinBERT)                               │
│  ├── Risk Management                                            │
│  └── Trading Strategy Engine                                    │
├─────────────────────────────────────────────────────────────────┤
│  Clojure HTTP API (Port 8080)                                   │
│  ├── GDAX/Coinbase Integration                                  │
│  ├── Binance Integration                                        │
│  ├── WebSocket Data Collection                                  │
│  ├── Historical Data Storage                                    │
│  └── Twilio Alert System                                        │
├─────────────────────────────────────────────────────────────────┤
│  Redis Database (Port 6379)                                    │
│  ├── Live Market Data Cache                                     │
│  ├── Historical Price Data                                      │
│  ├── Order Book Data                                            │
│  └── Alert History                                              │
└─────────────────────────────────────────────────────────────────┘
```

## ✨ Features

### **Hybrid Data Integration**
- **Clojure System**: Existing GDAX/Binance WebSocket feeds, Redis storage, Twilio alerts
- **Python System**: Technical analysis, sentiment analysis, risk management, trading signals
- **React Frontend**: Real-time dashboard with live updates

### **Data Flow**
1. **Clojure** collects live market data via WebSockets
2. **Python** consumes data via HTTP API or direct Redis access
3. **Python** performs technical analysis and generates trading signals
4. **React** displays real-time dashboard with WebSocket updates

## 🚀 Quick Start

### Prerequisites
- **Java 8+** (for Clojure system)
- **Leiningen** (Clojure build tool)
- **Python 3.8+**
- **Node.js 16+**
- **Redis Server**

### One-Command Startup

**Windows:**
```bash
start-hybrid-dashboard.bat
```

**Linux/macOS:**
```bash
./start-hybrid-dashboard.sh
```

### Manual Setup

#### 1. Start Redis
```bash
# macOS
brew services start redis

# Ubuntu
sudo systemctl start redis

# Windows
# Download and run Redis from: https://github.com/microsoftarchive/redis/releases
```

#### 2. Start Clojure HTTP API
```bash
cd crypto
lein run -m crypto.api.http/start-api-server!
```

#### 3. Start Python FastAPI Backend
```bash
cd crypto-bot-mvp/backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 4. Start React Frontend
```bash
cd crypto-bot-mvp/frontend
npm install
npm start
```

### Access Points
- **React Frontend**: http://localhost:3000
- **Python FastAPI**: http://localhost:8000
- **Python API Docs**: http://localhost:8000/docs
- **Clojure HTTP API**: http://localhost:8080

## 📊 API Endpoints

### Python FastAPI (Port 8000)
- `GET /price` - Get current BTC/USD price (hybrid Clojure/Python)
- `GET /indicators` - Get technical indicators (RSI, ADX, ATR)
- `GET /sentiment` - Get market sentiment analysis
- `GET /signal` - Get trading signal recommendation
- `GET /risk` - Get risk management controls
- `GET /system-status` - Get hybrid system status
- `WS /stream` - Real-time market data stream

### Clojure HTTP API (Port 8080)
- `GET /health` - Health check
- `GET /gdax/price/{product-id}` - GDAX price data
- `GET /gdax/history/{product-id}` - GDAX historical data
- `GET /binance/price/{symbol}` - Binance price data
- `GET /twilio/alerts` - Twilio alerts
- `GET /system/status` - Clojure system status

## 🎯 Trading Strategy

The hybrid system combines data from multiple sources:

### **Data Sources**
- **Clojure**: Live GDAX/Binance WebSocket feeds
- **Python**: Coinbase REST API (fallback)
- **Mock Data**: For testing when APIs unavailable

### **Strategy Components**
- **Momentum Signals** (60% weight): RSI + ADX analysis
- **Sentiment Signals** (40% weight): FinBERT crypto news analysis
- **Risk Management**: ATR-based position sizing, 1% risk per trade

### **Signal Generation**
1. **Clojure** provides live market data
2. **Python** calculates technical indicators
3. **Python** analyzes sentiment from news
4. **Python** combines signals with confidence scoring
5. **React** displays real-time recommendations

## 🔧 Configuration

### Environment Variables
```bash
# Copy template
cp env.template .env

# Edit with your settings
COINBASE_API_KEY=your_api_key
COINBASE_API_SECRET=your_secret
REDIS_URL=redis://localhost:6379
```

### Clojure Configuration
The Clojure system uses existing configuration in `crypto/src/crypto/infra/config.clj`:
- Redis connection settings
- GDAX/Binance API credentials
- Twilio alert settings

## 📈 Dashboard Components

### **Left Panel**
- **Live Price**: Real-time BTC/USD with change indicators
- **RSI**: Relative Strength Index with oversold/overbought levels
- **Sentiment**: Market sentiment score and label

### **Center Chart**
- **Price Chart**: Real-time price with area chart
- **Technical Indicators**: RSI, ADX, ATR overlays

### **Right Panel**
- **Trading Signal**: BUY/SELL/HOLD with confidence
- **Risk Controls**: Position size, stop loss, take profit
- **Signal Reasoning**: Human-readable explanation

## 🛠️ Development

### **Hybrid Development Workflow**
1. **Clojure**: Modify data collection in `crypto/src/crypto/services/`
2. **Python**: Update analysis in `crypto-bot-mvp/backend/`
3. **React**: Enhance UI in `crypto-bot-mvp/frontend/src/`

### **Adding New Data Sources**
1. Add WebSocket listener in Clojure (`crypto/src/crypto/services/`)
2. Add HTTP endpoint in Clojure API (`crypto/src/crypto/api/http.clj`)
3. Add consumer in Python (`crypto-bot-mvp/backend/hybrid_integration.py`)
4. Add display in React frontend

### **Testing**
```bash
# Test Clojure API
curl http://localhost:8080/health

# Test Python API
curl http://localhost:8000/system-status

# Test React frontend
open http://localhost:3000
```

## 📝 Data Storage

### **Redis Keys (Clojure System)**
- `gdax:price:BTC-USD` - Latest GDAX prices
- `gdax:history:BTC-USD` - Historical GDAX data
- `binance:price:BTCUSDT` - Latest Binance prices
- `twilio:alerts` - Alert history

### **Local Files (Python System)**
- `data/prices.json` - Price history backup
- `data/signals.json` - Trading signals
- `data/risk.json` - Risk management data

## 🔮 Future Enhancements

### **Phase 2: Enhanced Integration**
- **Real-time Order Execution**: Connect to Clojure trading systems
- **Multi-Exchange Support**: Leverage existing Binance integration
- **Advanced Alerts**: Use existing Twilio infrastructure
- **Portfolio Management**: Multi-asset support

### **Phase 3: Production Features**
- **Authentication**: User management and API keys
- **Backtesting**: Historical strategy validation
- **Paper Trading**: Simulated trading mode
- **Mobile App**: React Native dashboard

## 🚨 Important Notes

### **Hybrid System Benefits**
- **Leverages Existing Infrastructure**: Uses proven Clojure crypto systems
- **Modern Interface**: Python/React for rapid development
- **Fallback Systems**: Multiple data sources for reliability
- **Scalable Architecture**: Easy to extend and modify

### **MVP Limitations**
- **No Live Trading**: Dashboard only, no order execution
- **Single Asset Focus**: BTC/USD primary (extensible)
- **Basic Sentiment**: Simplified news analysis
- **Mock Data Fallbacks**: For testing without API keys

## 🤝 Contributing

1. **Clojure Changes**: Modify existing crypto system
2. **Python Changes**: Enhance analysis and API
3. **React Changes**: Improve UI and UX
4. **Integration**: Add new data sources or features

## 📄 License

This project integrates with existing Clojure crypto system and is licensed under the Eclipse Public License.

## 🆘 Support

### **Troubleshooting**
1. **Redis Connection**: Ensure Redis is running on port 6379
2. **Clojure API**: Check `lein run -m crypto.api.http/start-api-server!`
3. **Python API**: Verify `uvicorn main:app --reload`
4. **React Frontend**: Confirm `npm start` is running

### **System Status**
- Check hybrid system status: `GET /system-status`
- Monitor Clojure system: `GET http://localhost:8080/system/status`
- View Redis data: `redis-cli keys "*"`

---

**⚠️ Disclaimer**: This is a demo/educational project integrating existing systems. Do not use for live trading without proper testing and risk management.
