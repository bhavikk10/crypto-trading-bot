# 🔑 API Keys Configuration Guide

## Where to Add Your API Keys

### 1. **Create `.env` file in `crypto-bot-mvp/` directory:**

```bash
# Copy the template
cd crypto-bot-mvp
copy env.template .env
```

### 2. **Edit the `.env` file with your actual API keys:**

```bash
# REQUIRED API Keys for Real Data:

# Coinbase API (for real trading data)
COINBASE_API_KEY=your_actual_coinbase_api_key
COINBASE_API_SECRET=your_actual_coinbase_secret
COINBASE_PASSPHRASE=your_actual_coinbase_passphrase

# OPTIONAL API Keys for Enhanced Features:

# LunarCrash API (for enhanced sentiment analysis)
LUNARCRASH_API_KEY=your_actual_lunarcrash_key

# MarketSai API (for enhanced sentiment analysis)  
MARKETSAI_API_KEY=your_actual_marketsai_key

# Twilio API (for SMS alerts)
TWILIO_SID=your_actual_twilio_sid
TWILIO_TOKEN=your_actual_twilio_token
TWILIO_PHONE_NUMBER=+1234567890

# Redis (usually no password needed for local)
REDIS_URL=redis://localhost:6379
REDIS_PASSWORD=
```

## 🔍 How to Get API Keys

### **Coinbase API Keys (REQUIRED for real data):**
1. Go to https://pro.coinbase.com/
2. Sign up/Login to Coinbase Pro
3. Go to **Settings** → **API** → **New API Key**
4. Enable **View** permissions (no trading needed for MVP)
5. Copy: **API Key**, **Secret**, **Passphrase**

### **LunarCrash API (OPTIONAL):**
1. Visit https://lunarcrash.com/
2. Sign up for API access
3. Get your API key from dashboard

### **MarketSai API (OPTIONAL):**
1. Visit https://marketsai.com/
2. Sign up for API access  
3. Get your API key from dashboard

### **Twilio API (OPTIONAL for SMS alerts):**
1. Go to https://console.twilio.com/
2. Sign up for free account
3. Get **Account SID** and **Auth Token**
4. Buy a phone number for SMS

## 🚀 After Adding API Keys

### **Restart the services:**
```bash
# Stop current services (Ctrl+C)
# Then restart:

# Backend
cd crypto-bot-mvp/backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend  
cd crypto-bot-mvp/frontend
npm start
```

### **Verify real data:**
- Check http://localhost:8000/system-status
- Should show "python-coinbase" as data source
- Dashboard should show real BTC/USD prices

## ⚠️ Security Notes

- **Never commit `.env` file to git**
- **Keep API keys secure**
- **Use environment variables in production**
- **Start with Coinbase API only** (others are optional)
