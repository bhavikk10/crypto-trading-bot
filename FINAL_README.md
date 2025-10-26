# 🚀 Crypto Trading Bot Dashboard - Complete Setup Guide

## 📋 Overview

This is a complete **Crypto Trading Bot Dashboard** with:
- **FastAPI Backend** - Real-time crypto data processing
- **React Frontend** - Beautiful white-themed dashboard
- **Hybrid Architecture** - Integrates with existing Clojure system
- **Vercel Deployment** - Production-ready serverless deployment
- **Real API Integration** - Coinbase, Twilio, Redis

## 🎯 Quick Start (For Your Partner)

### Option 1: Local Development
```bash
# 1. Clone the repository
git clone https://github.com/bhavikk10/crypto-trading-bot.git
cd crypto-trading-bot

# 2. Start the dashboard locally
python -m http.server 3000

# 3. Open your browser
# Go to: http://localhost:3000/dashboard.html
```

### Option 2: Vercel Deployment (Recommended)
```bash
# 1. Go to https://vercel.com
# 2. Sign in with GitHub
# 3. Click "New Project"
# 4. Import: bhavikk10/crypto-trading-bot
# 5. Add environment variables (see below)
# 6. Deploy!
```

## 🔧 Complete Setup Instructions

### Prerequisites
- **Python 3.9+** (for backend)
- **Node.js 18+** (for frontend)
- **Git** (for version control)
- **Vercel Account** (for deployment)

### Step 1: Clone Repository
```bash
git clone https://github.com/bhavikk10/crypto-trading-bot.git
cd crypto-trading-bot
```

### Step 2: Backend Setup (Python)
```bash
# Navigate to backend
cd crypto-bot-mvp/backend

# Install Python dependencies
pip install -r requirements.txt

# Create environment file
cp env.template .env

# Edit .env with your API keys (see Environment Variables section)
```

### Step 3: Frontend Setup (React)
```bash
# Navigate to frontend
cd crypto-bot-mvp/frontend

# Install Node.js dependencies
npm install

# Build the React app
npm run build
```

### Step 4: Environment Variables Setup

Create a `.env` file in `crypto-bot-mvp/backend/` with:

```env
# Coinbase API (Required for real trading data)
COINBASE_API_KEY=your_coinbase_api_key_here
COINBASE_API_SECRET=your_coinbase_api_secret_here

# Twilio (Optional - for SMS notifications)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# Redis (Optional - for data caching)
REDIS_URL=redis://localhost:6379

# Additional APIs (Optional)
LUNARCRASH_API_KEY=your_lunarcrash_key
MARKETSAI_API_KEY=your_marketsai_key
```

### Step 5: Start the System

#### Option A: Standalone Dashboard (Easiest)
```bash
# From project root
python -m http.server 3000

# Open browser: http://localhost:3000/dashboard.html
```

#### Option B: Full Backend + Frontend
```bash
# Terminal 1: Start FastAPI backend
cd crypto-bot-mvp/backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Start React frontend
cd crypto-bot-mvp/frontend
npm start

# Open browser: http://localhost:3000
```

#### Option C: Hybrid System (Advanced)
```bash
# Start Clojure system first
cd crypto
lein run

# Then start Python backend
cd crypto-bot-mvp/backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Start frontend
cd crypto-bot-mvp/frontend
npm start
```

## 🌐 Vercel Deployment (Production)

### Step 1: Deploy to Vercel
1. **Go to [vercel.com](https://vercel.com)**
2. **Sign in with GitHub**
3. **Click "New Project"**
4. **Import repository:** `bhavikk10/crypto-trading-bot`
5. **Click "Deploy"**

### Step 2: Add Environment Variables
In Vercel dashboard → Settings → Environment Variables:

```
COINBASE_API_KEY = your_coinbase_api_key
COINBASE_API_SECRET = your_coinbase_api_secret
TWILIO_ACCOUNT_SID = your_twilio_sid
TWILIO_AUTH_TOKEN = your_twilio_token
TWILIO_PHONE_NUMBER = +1234567890
REDIS_URL = your_redis_url
```

### Step 3: Access Your Live Dashboard
- **URL:** `https://your-project-name.vercel.app`
- **API:** `https://your-project-name.vercel.app/api/`

## 📊 Dashboard Features

### 🎨 Visual Design
- **Clean white theme** with professional glassmorphism
- **4x2 grid layout** for organized metrics display
- **Responsive design** - works on all devices
- **Real-time updates** every 10 seconds

### 📈 Key Metrics (8 Cards)
1. **₿ Bitcoin Price** - Live BTC/USD price
2. **Ξ Ethereum Price** - Live ETH/USD price
3. **📊 Market Sentiment** - FinBERT analysis
4. **🎯 Trading Signal** - BUY/SELL/HOLD recommendations
5. **📈 24h Volume** - Trading volume data
6. **🌍 Market Cap** - Total market value
7. **⚙️ System Status** - Hybrid system health
8. **🔑 API Config** - Connection status

### 💎 Additional Sections
- **Top Cryptocurrencies** - BTC, ETH, BNB, LINK
- **Technical Analysis** - RSI, ADX, ATR, MACD
- **Risk Management** - Position sizing, stop-loss, take-profit
- **Trading Recommendations** - Action buttons

## 🔌 API Endpoints

All endpoints available at `/api/`:

- `GET /api/price` - Current BTC price
- `GET /api/indicators` - Technical indicators (RSI, ADX, ATR, MACD)
- `GET /api/sentiment` - Market sentiment analysis
- `GET /api/signal` - Trading signals
- `GET /api/risk` - Risk management data
- `GET /api/system-status` - System health
- `GET /api/config-status` - API configuration status

## 🛠️ Project Structure

```
crypto-trading-bot/
├── vercel.json                 # Vercel deployment config
├── dashboard.html              # Standalone dashboard
├── VERCEL_DEPLOYMENT.md        # Vercel deployment guide
├── api/                        # Serverless functions
│   ├── price.py               # Price endpoint
│   ├── indicators.py          # Technical indicators
│   ├── sentiment.py           # Sentiment analysis
│   ├── signal.py              # Trading signals
│   ├── risk.py                # Risk management
│   ├── system-status.py       # System status
│   ├── config-status.py       # Config status
│   └── requirements.txt       # Python dependencies
├── crypto-bot-mvp/
│   ├── backend/               # FastAPI backend
│   │   ├── main.py           # Main application
│   │   ├── config.py         # Configuration
│   │   ├── hybrid_integration.py # Clojure integration
│   │   ├── indicators.py     # Technical analysis
│   │   ├── sentiment.py      # FinBERT sentiment
│   │   ├── risk.py           # Risk management
│   │   ├── strategy.py       # Trading strategy
│   │   ├── redis_logger.py   # Data persistence
│   │   ├── requirements.txt   # Dependencies
│   │   └── .env              # Environment variables
│   └── frontend/             # React frontend
│       ├── src/
│       ├── public/
│       └── package.json
└── crypto/                   # Existing Clojure system
    ├── src/crypto/
    └── project.clj
```

## 🔐 Security & API Keys

### Required API Keys
- **Coinbase API** - For real trading data
- **Twilio** - For SMS notifications (optional)
- **Redis** - For data caching (optional)

### How to Get API Keys

#### Coinbase API
1. Go to [pro.coinbase.com](https://pro.coinbase.com)
2. Sign in → Settings → API
3. Create new API key
4. Enable "View" permissions
5. Copy API Key and Secret

#### Twilio (Optional)
1. Go to [twilio.com](https://twilio.com)
2. Sign up for free account
3. Get Account SID and Auth Token
4. Buy a phone number for SMS

## 🚀 Deployment Options

### 1. Vercel (Recommended)
- **Free tier:** 100GB bandwidth, 1000 function calls
- **Automatic scaling**
- **Global CDN**
- **Easy environment variables**

### 2. Local Development
- **Full control**
- **Real-time debugging**
- **All features available**

### 3. Hybrid Deployment
- **Clojure system** on your server
- **Python API** on Vercel
- **Frontend** on Vercel

## 🔧 Troubleshooting

### Common Issues

#### 1. "Module not found" errors
```bash
# Reinstall dependencies
pip install -r requirements.txt
npm install
```

#### 2. API connection errors
- Check your `.env` file has correct API keys
- Verify API keys are active
- Check internet connection

#### 3. Frontend not loading
```bash
# Clear browser cache
# Try different browser
# Check console for errors
```

#### 4. Vercel deployment fails
- Check `vercel.json` syntax
- Verify environment variables
- Check build logs in Vercel dashboard

## 📞 Support

### Documentation
- **Vercel Guide:** `VERCEL_DEPLOYMENT.md`
- **API Keys Guide:** `API_KEYS_GUIDE.md`
- **Backend README:** `crypto-bot-mvp/backend/README.md`

### Quick Commands
```bash
# Check system status
curl http://localhost:8000/system-status

# Check API configuration
curl http://localhost:8000/config-status

# Get current price
curl http://localhost:8000/price
```

## 🎉 Success!

Once deployed, your crypto trading bot dashboard will provide:
- ✅ **Real-time crypto data** from Coinbase
- ✅ **Professional trading interface**
- ✅ **Technical analysis** with multiple indicators
- ✅ **Risk management** recommendations
- ✅ **SMS notifications** (if Twilio configured)
- ✅ **Global accessibility** via Vercel

**Your partner can now access a fully functional crypto trading dashboard! 🚀📈**

---

**Repository:** https://github.com/bhavikk10/crypto-trading-bot  
**Live Demo:** https://your-project-name.vercel.app  
**Support:** Check the troubleshooting section above
