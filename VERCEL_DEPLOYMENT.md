# Vercel Deployment Guide for Crypto Trading Bot Dashboard

## 🚀 Quick Deploy to Vercel

### Prerequisites
- Vercel account (free at vercel.com)
- GitHub repository with your code

### Step 1: Prepare Your Repository
Your repository is already configured with:
- ✅ `vercel.json` - Vercel configuration
- ✅ `api/` directory - Serverless functions
- ✅ `crypto-bot-mvp/frontend/` - React frontend
- ✅ Environment variables setup

### Step 2: Deploy to Vercel

1. **Go to [vercel.com](https://vercel.com) and sign in**

2. **Click "New Project"**

3. **Import your GitHub repository:**
   - Select `bhavikk10/crypto-trading-bot`
   - Click "Import"

4. **Configure Environment Variables:**
   ```
   COINBASE_API_KEY=your_coinbase_api_key
   COINBASE_API_SECRET=your_coinbase_api_secret
   TWILIO_ACCOUNT_SID=your_twilio_sid
   TWILIO_AUTH_TOKEN=your_twilio_token
   REDIS_URL=your_redis_url
   ```

5. **Deploy:**
   - Click "Deploy"
   - Wait for deployment to complete

### Step 3: Access Your Dashboard
- Your dashboard will be available at: `https://your-project-name.vercel.app`
- API endpoints will be at: `https://your-project-name.vercel.app/api/`

## 🔧 Project Structure

```
├── vercel.json                 # Vercel configuration
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
│   └── frontend/              # React frontend
│       ├── src/
│       ├── public/
│       └── package.json
└── dashboard.html             # Standalone dashboard
```

## 🌐 API Endpoints

All endpoints are available at `/api/`:

- `GET /api/price` - Current BTC price
- `GET /api/indicators` - Technical indicators (RSI, ADX, ATR, MACD)
- `GET /api/sentiment` - Market sentiment analysis
- `GET /api/signal` - Trading signals
- `GET /api/risk` - Risk management data
- `GET /api/system-status` - System health
- `GET /api/config-status` - API configuration status

## 🔄 Automatic Deployments

- **Push to main branch** → Automatic deployment
- **Pull requests** → Preview deployments
- **Environment variables** → Secure storage in Vercel dashboard

## 📊 Features

✅ **Serverless Backend** - Python functions on Vercel  
✅ **React Frontend** - Static site generation  
✅ **Real-time Data** - Mock data with live timestamps  
✅ **Responsive Design** - Works on all devices  
✅ **CORS Enabled** - Cross-origin requests supported  
✅ **Environment Variables** - Secure API key storage  

## 🛠️ Local Development

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy locally
vercel dev

# Deploy to production
vercel --prod
```

## 🔐 Security

- API keys stored securely in Vercel environment variables
- CORS headers configured for cross-origin requests
- Serverless functions have built-in security
- No database credentials exposed

## 📈 Scaling

- **Automatic scaling** - Vercel handles traffic spikes
- **Global CDN** - Fast loading worldwide
- **Edge functions** - Low latency API responses
- **Free tier** - 100GB bandwidth, 1000 serverless function invocations

Your crypto trading bot dashboard is now ready for production deployment! 🚀
