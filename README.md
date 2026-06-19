# Crypto Trading Bot Dashboard

A crypto trading bot dashboard and market-analysis MVP built as a **freelance project** for a client who needed a prototype platform for crypto market monitoring, signal generation, sentiment analysis, and risk-management visualization.

The project combines a FastAPI backend, a React dashboard, live crypto market data, technical indicators, sentiment analysis, WebSocket streaming, Redis-based logging, and trading-signal logic.

> **Important:** This project is a technical MVP/prototype. It does not provide financial advice, does not guarantee trading performance, and should not be used for live trading without proper testing, compliance review, risk controls, and exchange-side safeguards.

---

## Overview

Crypto Trading Bot Dashboard is a full-stack MVP designed to help users monitor crypto market conditions and evaluate automated trading signals from one interface.

The platform fetches crypto price data, calculates technical indicators, analyzes market sentiment, generates BUY/SELL/HOLD-style signals, and computes basic risk controls such as position size, stop loss, take profit, and risk/reward ratio.

The goal of the project was to create a working proof-of-concept for a larger crypto trading automation platform.

---

## Project Context

This project was built as a freelance MVP for a client exploring a crypto trading bot and dashboard platform.

For public portfolio safety, this repository is presented as a demo/prototype version. Any API keys, private exchange credentials, production deployment configuration, and client-specific business logic should be handled privately and never committed to the repository.

The public version demonstrates:

* Backend market-data API structure
* Technical indicator calculation flow
* Sentiment-analysis integration pattern
* Trading-signal generation logic
* Risk-management calculations
* Real-time dashboard architecture
* Frontend visualization layer
* Hybrid Python/Clojure integration approach

---

## Key Features

### Market Data

* Coinbase API integration
* Current price endpoint
* Historical price data flow
* Symbol-based price lookup
* Hybrid data-fetching architecture

### Technical Indicators

* RSI calculation
* ADX calculation
* ATR calculation
* Momentum signal interpretation
* Indicator endpoint for frontend consumption

### Sentiment Analysis

* Sentiment-analysis module
* Market sentiment score
* Sentiment confidence output
* Sentiment used as part of signal generation

### Trading Signal Engine

* BUY / SELL / HOLD signal generation
* Momentum + sentiment weighted scoring
* Signal confidence calculation
* Human-readable signal reasoning
* Configurable thresholds for:

  * Buy signal
  * Sell signal
  * Confidence
  * RSI overbought/oversold
  * ADX trend strength

### Risk Management

* ATR-based stop-loss calculation
* Take-profit calculation
* Position sizing based on risk per trade
* Risk/reward ratio calculation
* Max position-size control
* Portfolio-risk helper logic

### Real-Time Streaming

* FastAPI WebSocket connection manager
* Real-time message broadcasting
* Dashboard-ready streaming API structure

### Dashboard Frontend

* React dashboard interface
* Recharts-based visualizations
* Axios API communication
* Toast notifications
* Responsive dashboard styling with Tailwind CSS

### Hybrid Architecture

* Python FastAPI backend
* Optional Clojure service integration
* Redis bridge/logging layer
* HTTP and WebSocket communication

---

## Tech Stack

### Backend

* Python
* FastAPI
* Pydantic
* aiohttp
* Redis
* WebSockets
* Coinbase API
* Technical indicator modules
* Sentiment-analysis module
* Risk-management module
* Trading-strategy module

### Frontend

* React
* React Scripts
* Axios
* Recharts
* React Hot Toast
* Tailwind CSS

### Optional / Integration

* Clojure
* Java
* Leiningen
* Redis bridge

---

## Project Structure

```txt id="zh6g7f"
crypto-trading-bot/
├── crypto-bot-mvp/
│   ├── backend/
│   │   ├── main.py
│   │   ├── indicators.py
│   │   ├── sentiment.py
│   │   ├── risk.py
│   │   ├── strategy.py
│   │   ├── redis_logger.py
│   │   ├── hybrid_integration.py
│   │   ├── config.py
│   │   ├── requirements.txt
│   │   └── env.template
│   │
│   └── frontend/
│       ├── src/
│       ├── package.json
│       └── tailwind.config.js
│
├── crypto/
│   └── optional Clojure integration files
│
└── README.md
```

---

## API Overview

| Method | Endpoint         | Description                                                     |
| ------ | ---------------- | --------------------------------------------------------------- |
| `GET`  | `/`              | Health check endpoint                                           |
| `GET`  | `/system-status` | Returns hybrid Python/Clojure system status                     |
| `GET`  | `/config-status` | Shows API key/configuration status                              |
| `GET`  | `/price`         | Returns current price for a trading pair                        |
| `GET`  | `/indicators`    | Returns RSI, ADX, ATR, and momentum signal                      |
| `GET`  | `/sentiment`     | Returns crypto market sentiment                                 |
| `GET`  | `/signal`        | Generates trading signal using price, indicators, and sentiment |
| `WS`   | `/stream`        | WebSocket stream for real-time dashboard updates                |

---

## Trading Signal Logic

The signal engine combines two major components:

1. **Momentum score**

   * Based on RSI and ADX
   * Detects oversold/overbought conditions
   * Considers trend strength

2. **Sentiment score**

   * Converts market sentiment into a normalized signal
   * Higher sentiment contributes to bullish signals
   * Lower sentiment contributes to bearish signals

The final output is a combined weighted score that produces:

* `BUY`
* `SELL`
* `HOLD`

Each signal also includes confidence and reasoning.

---

## Risk Management Logic

The risk module calculates:

* Position size
* Position value
* Stop-loss price
* Take-profit price
* Risk amount
* Risk percentage
* Potential profit
* Potential profit percentage
* Risk/reward ratio

The default configuration uses:

* Maximum position size: 2% of portfolio
* Risk per trade: 1%
* ATR multiplier: 2.0
* Risk/reward ratio: 2.0
* Maximum portfolio risk: 5%

---

## Getting Started

### Prerequisites

Make sure you have the following installed:

* Python 3.8+
* Node.js 18+
* npm
* Redis Server

Optional for hybrid integration:

* Java 8+
* Leiningen

---

## Backend Setup

Navigate to the backend directory:

```bash id="y6ri06"
cd crypto-bot-mvp/backend
```

Create and activate a virtual environment:

```bash id="3dd9wz"
python -m venv venv
```

Windows:

```bash id="gjw39q"
venv\Scripts\activate
```

macOS/Linux:

```bash id="8xm3fg"
source venv/bin/activate
```

Install dependencies:

```bash id="4143di"
pip install -r requirements.txt
```

Create an environment file:

```bash id="c9t4b5"
cp env.template .env
```

Start the backend:

```bash id="xssbpf"
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend API:

```txt id="mwz5m3"
http://localhost:8000
```

Interactive API docs:

```txt id="d0hxx7"
http://localhost:8000/docs
```

---

## Frontend Setup

Navigate to the frontend directory:

```bash id="48tgpm"
cd crypto-bot-mvp/frontend
```

Install dependencies:

```bash id="vtg1z1"
npm install
```

Start the frontend:

```bash id="b2svaj"
npm run dev
```

or, depending on the script being used:

```bash id="3nk5x8"
npm start
```

Frontend app:

```txt id="dsbdcc"
http://localhost:3000
```

---

## Environment Variables

Create a `.env` file inside the backend folder.

Expected configuration may include:

```env id="2x6kjq"
REDIS_URL=redis://localhost:6379
COINBASE_API_KEY=your_coinbase_api_key
COINBASE_API_SECRET=your_coinbase_api_secret
COINBASE_PASSPHRASE=your_coinbase_passphrase
TWILIO_ACCOUNT_SID=optional_twilio_sid
TWILIO_AUTH_TOKEN=optional_twilio_auth_token
LUNARCRUSH_API_KEY=optional_lunarcrush_key
MARKETSAI_API_KEY=optional_marketsai_key
```

Never commit real API keys or exchange credentials.

---

## Optional Clojure Integration

The project includes support for a hybrid Python/Clojure system.

To run the optional Clojure service:

```bash id="0cif7z"
cd crypto
lein run
```

This part is optional and depends on the intended deployment architecture.

---

## Frontend Scripts

| Command                | Description                                          |
| ---------------------- | ---------------------------------------------------- |
| `npm run dev`          | Starts the frontend development server if configured |
| `npm start`            | Starts the React development server                  |
| `npm run build`        | Creates a production build                           |
| `npm test`             | Runs frontend tests                                  |
| `npm run vercel-build` | Runs the frontend build for Vercel-style deployment  |

---

## Backend Modules

| Module                  | Purpose                                                      |
| ----------------------- | ------------------------------------------------------------ |
| `main.py`               | FastAPI app, endpoints, WebSocket manager, API orchestration |
| `indicators.py`         | Technical indicator calculations                             |
| `sentiment.py`          | Sentiment-analysis logic                                     |
| `strategy.py`           | Signal generation using momentum and sentiment               |
| `risk.py`               | Position sizing, stop loss, take profit, and portfolio risk  |
| `redis_logger.py`       | Redis-based logging/data persistence                         |
| `hybrid_integration.py` | Python/Clojure integration layer                             |
| `config.py`             | Environment/configuration management                         |

---

## What I Worked On

* FastAPI backend architecture
* REST API endpoints
* WebSocket streaming structure
* Coinbase market-data integration
* Technical indicator calculation flow
* Sentiment-analysis integration
* Trading-signal generation logic
* ATR-based risk-management module
* Redis logging layer
* React dashboard setup
* Recharts visualizations
* Axios API communication
* Hybrid Python/Clojure integration support
* MVP documentation and setup structure

---

## Future Improvements

* Add exchange paper-trading mode
* Add secure authentication
* Add encrypted API key storage
* Add database-backed trade logs
* Add backtesting engine
* Add strategy configuration dashboard
* Add portfolio tracking
* Add real-time alerts
* Add notification preferences
* Add websocket reconnect handling
* Add Docker Compose setup
* Add deployment documentation
* Add unit tests for strategy and risk modules
* Add integration tests for API endpoints
* Add live-vs-paper trading mode separation
* Add compliance and safety checks before any production usage

---

## Screenshots

Add screenshots or GIFs here:

```md id="s1f1sz"
![Dashboard](./screenshots/dashboard.png)
![Signals](./screenshots/signals.png)
![Risk Management](./screenshots/risk.png)
![Market Data](./screenshots/market-data.png)
```

---

## Disclaimer

This repository is a technical prototype/MVP for educational, portfolio, and demonstration purposes.

It does not provide financial advice. It does not guarantee profitable trading results. Crypto markets are volatile, and automated trading systems can cause financial loss if used without proper safeguards.

Do not use this project with real funds unless it has been professionally reviewed, tested, secured, and connected through a properly controlled paper-trading or production-risk environment.

---

## Author

**Bhavik Malik**

* GitHub: [@bhavikk10](https://github.com/bhavikk10)
* Email: [bhavikmalik100706@gmail.com](mailto:bhavikmalik100706@gmail.com)
