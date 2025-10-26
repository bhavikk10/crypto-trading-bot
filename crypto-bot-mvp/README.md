# Crypto Trading Bot Dashboard

A comprehensive crypto trading bot dashboard with real-time market data, sentiment analysis, and risk management.

## 🚀 Features

- **Real-time Market Data**: Live price feeds from Coinbase API
- **Sentiment Analysis**: FinBERT-powered crypto sentiment analysis
- **Technical Indicators**: RSI, ADX, ATR calculations
- **Risk Management**: ATR-based position sizing and stop-loss
- **WebSocket Streaming**: Real-time data updates
- **Modern UI**: React + Tailwind CSS dashboard
- **Hybrid Architecture**: Python FastAPI + Clojure integration

## 🏗️ Architecture

### Backend (Python FastAPI)
- **FastAPI**: Modern, fast web framework
- **WebSocket**: Real-time data streaming
- **Redis**: Caching and data persistence
- **Coinbase API**: Live market data integration
- **FinBERT**: Sentiment analysis model
- **Technical Analysis**: TA-Lib indicators

### Frontend (React)
- **React 18**: Modern React with hooks
- **Tailwind CSS**: Utility-first styling
- **Recharts**: Data visualization
- **WebSocket Client**: Real-time updates
- **Responsive Design**: Mobile-friendly interface

### Integration
- **Hybrid System**: Combines Python FastAPI with existing Clojure services
- **Redis Bridge**: Shared data layer
- **HTTP API**: RESTful endpoints
- **WebSocket**: Real-time communication

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- Redis Server
- Java 8+ (for Clojure integration)
- Leiningen (for Clojure)

## 🛠️ Installation

### Backend Setup

1. **Install Python dependencies**:
   ```bash
   cd crypto-bot-mvp/backend
   pip install -r requirements.txt
   ```

2. **Configure environment variables**:
   ```bash
   cp env.template .env
   # Edit .env with your API keys
   ```

3. **Start the backend**:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Install Node.js dependencies**:
   ```bash
   cd crypto-bot-mvp/frontend
   npm install
   ```

2. **Start the frontend**:
   ```bash
   npm start
   ```

### Clojure Integration (Optional)

1. **Install Java and Leiningen**
2. **Start Clojure services**:
   ```bash
   cd crypto
   lein run
   ```

## 🔑 API Keys Required

- **Coinbase API**: For live market data
- **Twilio**: For notifications (optional)
- **LunarCrash**: For enhanced sentiment (optional)
- **MarketSai**: For market analysis (optional)

## 📊 API Endpoints

- `GET /`: Health check
- `GET /config-status`: API configuration status
- `GET /docs`: Interactive API documentation
- `WS /stream`: WebSocket for real-time data
- `GET /price/{symbol}`: Get current price
- `GET /historical/{symbol}`: Get historical data
- `GET /sentiment`: Get sentiment analysis
- `GET /signals`: Get trading signals

## 🎯 Usage

1. **Start the system**:
   ```bash
   # Backend
   cd crypto-bot-mvp/backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   
   # Frontend
   cd crypto-bot-mvp/frontend
   npm start
   ```

2. **Access the dashboard**: http://localhost:3000
3. **API documentation**: http://localhost:8000/docs

## 🔧 Configuration

Edit `crypto-bot-mvp/backend/.env`:

```env
# Coinbase API
COINBASE_API_KEY=your_api_key
COINBASE_API_SECRET=your_api_secret

# Twilio (optional)
TWILIO_SID=your_twilio_sid
TWILIO_TOKEN=your_twilio_token
TWILIO_PHONE=your_twilio_phone

# Redis
REDIS_URL=redis://localhost:6379

# Debug
DEBUG=true
LOG_LEVEL=INFO
```

## 📈 Features

### Real-time Data
- Live price feeds from Coinbase
- WebSocket streaming
- Historical data analysis

### Sentiment Analysis
- FinBERT model integration
- News headline analysis
- Market sentiment scoring

### Technical Analysis
- RSI (Relative Strength Index)
- ADX (Average Directional Index)
- ATR (Average True Range)

### Risk Management
- Position sizing based on ATR
- Stop-loss calculations
- Risk metrics display

## 🚀 Deployment

### Production Build

1. **Build frontend**:
   ```bash
   cd crypto-bot-mvp/frontend
   npm run build
   ```

2. **Serve static files**:
   ```bash
   npx serve -s build -l 3000
   ```

### Docker (Coming Soon)
- Dockerfile for backend
- Docker Compose for full stack
- Production-ready configuration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: GitHub Issues
- **Documentation**: [README.md](README.md)
- **API Docs**: http://localhost:8000/docs

## 🔮 Roadmap

- [ ] Docker containerization
- [ ] Enhanced sentiment analysis
- [ ] More technical indicators
- [ ] Portfolio management
- [ ] Mobile app
- [ ] Advanced risk metrics
- [ ] Backtesting framework
- [ ] Multi-exchange support

---

**Built with ❤️ for the crypto community**