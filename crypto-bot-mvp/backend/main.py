"""
FastAPI main application for Crypto Trading Bot Dashboard
Provides REST endpoints and WebSocket streaming for real-time crypto data
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

import aiohttp
import redis
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from indicators import TechnicalIndicators
from sentiment import SentimentAnalyzer
from risk import RiskManager
from strategy import TradingStrategy
from redis_logger import RedisLogger
from hybrid_integration import hybrid_manager, clojure_config
from config import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration constants
COINBASE_API_BASE = "https://api.exchange.coinbase.com"
COINBASE_WS_URL = "wss://ws-feed.exchange.coinbase.com"
REDIS_URL = config.REDIS_URL

# Initialize FastAPI app
app = FastAPI(title="Crypto Trading Bot Dashboard", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
redis_client = redis.from_url(REDIS_URL)
indicators = TechnicalIndicators()
sentiment_analyzer = SentimentAnalyzer()
risk_manager = RiskManager()
trading_strategy = TradingStrategy()
redis_logger = RedisLogger(redis_client)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # Remove disconnected connections
                self.active_connections.remove(connection)

manager = ConnectionManager()

# Pydantic models
class PriceResponse(BaseModel):
    symbol: str
    price: float
    timestamp: datetime

class IndicatorsResponse(BaseModel):
    rsi: float
    adx: float
    atr: float
    momentum_signal: str
    timestamp: datetime

class SentimentResponse(BaseModel):
    score: float
    sentiment: str
    confidence: float
    timestamp: datetime

class SignalResponse(BaseModel):
    signal: str
    confidence: float
    reasoning: str
    timestamp: datetime

class RiskResponse(BaseModel):
    position_size: float
    stop_loss: float
    take_profit: float
    risk_reward_ratio: float
    timestamp: datetime

# Hybrid API helper functions
async def get_hybrid_price(symbol: str = "BTC-USD") -> Dict:
    """Fetch current price using hybrid Clojure/Python system"""
    try:
        # Use hybrid manager to get price data
        price_data = await hybrid_manager.get_hybrid_price_data(symbol)
        logger.info(f"Price data source: {price_data.get('source', 'unknown')}")
        return price_data
    except Exception as e:
        logger.error(f"Error fetching hybrid price: {e}")
        raise HTTPException(status_code=500, detail="Price fetch failed")

async def get_coinbase_price(symbol: str = "BTC-USD") -> Dict:
    """Legacy function - now uses hybrid system"""
    return await get_hybrid_price(symbol)

async def get_hybrid_historical_data(symbol: str = "BTC-USD", limit: int = 100) -> List[Dict]:
    """Fetch historical data using hybrid system"""
    try:
        # Use hybrid manager to get historical data
        history_data = await hybrid_manager.get_hybrid_history_data(symbol, limit)
        logger.info(f"History data source: {'clojure' if len(history_data) > 0 else 'python'}")
        return history_data
    except Exception as e:
        logger.error(f"Error fetching hybrid historical data: {e}")
        raise HTTPException(status_code=500, detail="Historical data fetch failed")

async def get_coinbase_historical_data(symbol: str = "BTC-USD", granularity: int = 3600) -> List[Dict]:
    """Legacy function - now uses hybrid system"""
    return await get_hybrid_historical_data(symbol)

# REST API Endpoints
@app.get("/")
async def root():
    return {"message": "Crypto Trading Bot Dashboard API", "status": "running"}

@app.get("/system-status")
async def get_system_status():
    """Get status of hybrid Clojure/Python system"""
    try:
        status = await hybrid_manager.get_system_status()
        return status
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/config-status")
async def get_config_status():
    """Get API key configuration status"""
    try:
        config_status = config.get_status()
        return {
            "configuration": config_status,
            "message": "Check which API keys are configured",
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error(f"Error getting config status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/price", response_model=PriceResponse)
async def get_price(symbol: str = "BTC-USD"):
    """Get current price for a trading pair"""
    try:
        price_data = await get_coinbase_price(symbol)
        
        # Log to Redis
        await redis_logger.log_price(price_data)
        
        return PriceResponse(**price_data)
    except Exception as e:
        logger.error(f"Error in get_price: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/indicators", response_model=IndicatorsResponse)
async def get_indicators(symbol: str = "BTC-USD"):
    """Get technical indicators for a trading pair"""
    try:
        # Fetch historical data
        historical_data = await get_coinbase_historical_data(symbol)
        
        if not historical_data:
            raise HTTPException(status_code=400, detail="No historical data available")
        
        # Calculate indicators
        rsi = indicators.calculate_rsi(historical_data)
        adx = indicators.calculate_adx(historical_data)
        atr = indicators.calculate_atr(historical_data)
        momentum_signal = indicators.get_momentum_signal(rsi, adx)
        
        result = {
            "rsi": rsi,
            "adx": adx,
            "atr": atr,
            "momentum_signal": momentum_signal,
            "timestamp": datetime.now()
        }
        
        # Log to Redis
        await redis_logger.log_indicators(result)
        
        return IndicatorsResponse(**result)
    except Exception as e:
        logger.error(f"Error in get_indicators: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sentiment", response_model=SentimentResponse)
async def get_sentiment():
    """Get sentiment analysis for crypto market"""
    try:
        sentiment_data = await sentiment_analyzer.analyze_crypto_sentiment()
        
        # Log to Redis
        await redis_logger.log_sentiment(sentiment_data)
        
        return SentimentResponse(**sentiment_data)
    except Exception as e:
        logger.error(f"Error in get_sentiment: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/signal", response_model=SignalResponse)
async def get_trading_signal(symbol: str = "BTC-USD"):
    """Get trading signal based on indicators and sentiment"""
    try:
        # Get current price
        price_data = await get_coinbase_price(symbol)
        
        # Get indicators
        indicators_data = await get_indicators(symbol)
        
        # Get sentiment
        sentiment_data = await get_sentiment()
        
        # Generate trading signal
        signal_data = trading_strategy.generate_signal(
            price_data["price"],
            indicators_data.rsi,
            indicators_data.adx,
            indicators_data.atr,
            sentiment_data.score
        )
        
        # Log to Redis
        await redis_logger.log_signal(signal_data)
        
        return SignalResponse(**signal_data)
    except Exception as e:
        logger.error(f"Error in get_trading_signal: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/risk", response_model=RiskResponse)
async def get_risk_controls(symbol: str = "BTC-USD"):
    """Get risk management controls"""
    try:
        # Get current price
        price_data = await get_coinbase_price(symbol)
        
        # Get indicators for ATR
        indicators_data = await get_indicators(symbol)
        
        # Calculate risk controls
        risk_data = risk_manager.calculate_risk_controls(
            price_data["price"],
            indicators_data.atr
        )
        
        # Log to Redis
        await redis_logger.log_risk(risk_data)
        
        return RiskResponse(**risk_data)
    except Exception as e:
        logger.error(f"Error in get_risk_controls: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket endpoint
@app.websocket("/stream")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time data streaming"""
    await manager.connect(websocket)
    try:
        while True:
            # Send periodic updates
            price_data = await get_coinbase_price()
            indicators_data = await get_indicators()
            sentiment_data = await get_sentiment()
            signal_data = await get_trading_signal()
            risk_data = await get_risk_controls()
            
            # Combine all data
            combined_data = {
                "type": "market_update",
                "data": {
                    "price": price_data,
                    "indicators": indicators_data.dict(),
                    "sentiment": sentiment_data.dict(),
                    "signal": signal_data.dict(),
                    "risk": risk_data.dict()
                },
                "timestamp": datetime.now().isoformat()
            }
            
            await manager.send_personal_message(json.dumps(combined_data), websocket)
            
            # Wait 5 seconds before next update
            await asyncio.sleep(5)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("WebSocket client disconnected")

# Background task for continuous data collection
@app.on_event("startup")
async def startup_event():
    """Initialize background tasks on startup"""
    logger.info("Starting Crypto Trading Bot Dashboard...")
    
    # Test Redis connection
    try:
        redis_client.ping()
        logger.info("Redis connection established")
    except Exception as e:
        logger.error(f"Redis connection failed: {e}")
    
    # Initialize sentiment analyzer
    await sentiment_analyzer.initialize()
    logger.info("Sentiment analyzer initialized")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
