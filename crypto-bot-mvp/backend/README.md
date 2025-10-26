# Crypto Trading Bot Dashboard - Backend

This is the FastAPI backend for the Crypto Trading Bot Dashboard MVP.

## Features

- Real-time market data from Coinbase API
- Technical analysis (RSI, ADX, ATR)
- Sentiment analysis with FinBERT
- Risk management calculations
- Trading signal generation
- WebSocket streaming
- Redis data persistence

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

- `GET /price` - Current BTC/USD price
- `GET /indicators` - Technical indicators
- `GET /sentiment` - Market sentiment
- `GET /signal` - Trading signal
- `GET /risk` - Risk controls
- `WS /stream` - Real-time data stream

## Modules

- **main.py**: FastAPI application and endpoints
- **indicators.py**: Technical analysis calculations
- **sentiment.py**: FinBERT sentiment analysis
- **risk.py**: Risk management and position sizing
- **strategy.py**: Trading signal generation
- **redis_logger.py**: Data persistence and caching

## Configuration

Copy `env.template` to `.env` and configure your API keys and settings.

## Development

The backend provides both REST API endpoints and WebSocket streaming for real-time data updates.
