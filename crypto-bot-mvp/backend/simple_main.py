"""
Simplified Crypto Trading Bot Dashboard - No Heavy Dependencies
Quick test version with mock data
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
import random

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Mock data generators
def get_mock_price(symbol: str = "BTC-USD") -> Dict:
    """Generate realistic mock price data"""
    base_price = 45000 if "BTC" in symbol else 3000 if "ETH" in symbol else 100
    price = base_price + random.uniform(-base_price * 0.05, base_price * 0.05)
    
    return {
        "symbol": symbol,
        "price": round(price, 2),
        "timestamp": datetime.now(),
        "source": "mock-data"
    }

def get_mock_indicators() -> Dict:
    """Generate realistic mock technical indicators"""
    rsi = random.uniform(20, 80)
    adx = random.uniform(15, 50)
    atr = random.uniform(500, 2000)
    
    momentum = "Strong Bullish" if rsi < 30 and adx > 40 else \
               "Bullish" if rsi < 40 and adx > 25 else \
               "Strong Bearish" if rsi > 70 and adx > 40 else \
               "Bearish" if rsi > 60 and adx > 25 else "Neutral"
    
    return {
        "rsi": round(rsi, 2),
        "adx": round(adx, 2),
        "atr": round(atr, 4),
        "momentum_signal": momentum,
        "timestamp": datetime.now()
    }

def get_mock_sentiment() -> Dict:
    """Generate realistic mock sentiment data"""
    score = random.uniform(20, 80)
    
    sentiment = "Very Bullish" if score >= 70 else \
                "Bullish" if score >= 60 else \
                "Very Bearish" if score <= 30 else \
                "Bearish" if score <= 40 else "Neutral"
    
    return {
        "score": round(score, 2),
        "sentiment": sentiment,
        "confidence": round(random.uniform(0.6, 0.9), 2),
        "timestamp": datetime.now()
    }

def get_mock_signal() -> Dict:
    """Generate realistic mock trading signal"""
    signals = ["BUY", "SELL", "HOLD"]
    signal = random.choice(signals)
    
    reasoning = f"Signal: {signal} | RSI: {random.uniform(20, 80):.1f} | ADX: {random.uniform(15, 50):.1f} | Sentiment: {random.uniform(20, 80):.1f}"
    
    return {
        "signal": signal,
        "confidence": round(random.uniform(0.6, 0.9), 3),
        "reasoning": reasoning,
        "timestamp": datetime.now()
    }

def get_mock_risk() -> Dict:
    """Generate realistic mock risk management data"""
    price = random.uniform(40000, 50000)
    atr = random.uniform(500, 2000)
    
    position_size = random.uniform(0.001, 0.01)
    stop_loss = price - (atr * 2)
    take_profit = price + (atr * 4)
    
    return {
        "position_size": round(position_size, 6),
        "stop_loss": round(stop_loss, 2),
        "take_profit": round(take_profit, 2),
        "risk_reward_ratio": 2.0,
        "timestamp": datetime.now()
    }

# REST API Endpoints
@app.get("/")
async def root():
    return {"message": "Crypto Trading Bot Dashboard API", "status": "running"}

@app.get("/config-status")
async def get_config_status():
    """Get API key configuration status"""
    return {
        "configuration": {
            "coinbase_configured": True,
            "lunarcrash_configured": False,
            "marketsai_configured": False,
            "twilio_configured": True,
            "redis_url": "redis://localhost:6379",
            "debug_mode": True,
            "log_level": "INFO"
        },
        "message": "Mock data mode - all APIs configured",
        "timestamp": datetime.now()
    }

@app.get("/price", response_model=PriceResponse)
async def get_price(symbol: str = "BTC-USD"):
    """Get current price for a trading pair"""
    try:
        price_data = get_mock_price(symbol)
        return PriceResponse(**price_data)
    except Exception as e:
        logger.error(f"Error in get_price: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/indicators", response_model=IndicatorsResponse)
async def get_indicators(symbol: str = "BTC-USD"):
    """Get technical indicators for a trading pair"""
    try:
        indicators_data = get_mock_indicators()
        return IndicatorsResponse(**indicators_data)
    except Exception as e:
        logger.error(f"Error in get_indicators: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sentiment", response_model=SentimentResponse)
async def get_sentiment():
    """Get sentiment analysis for crypto market"""
    try:
        sentiment_data = get_mock_sentiment()
        return SentimentResponse(**sentiment_data)
    except Exception as e:
        logger.error(f"Error in get_sentiment: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/signal", response_model=SignalResponse)
async def get_trading_signal(symbol: str = "BTC-USD"):
    """Get trading signal based on indicators and sentiment"""
    try:
        signal_data = get_mock_signal()
        return SignalResponse(**signal_data)
    except Exception as e:
        logger.error(f"Error in get_trading_signal: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/risk", response_model=RiskResponse)
async def get_risk_controls(symbol: str = "BTC-USD"):
    """Get risk management controls"""
    try:
        risk_data = get_mock_risk()
        return RiskResponse(**risk_data)
    except Exception as e:
        logger.error(f"Error in get_risk_controls: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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
                self.active_connections.remove(connection)

manager = ConnectionManager()

# WebSocket endpoint
@app.websocket("/stream")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time data streaming"""
    await manager.connect(websocket)
    try:
        while True:
            # Send periodic updates
            price_data = get_mock_price()
            indicators_data = get_mock_indicators()
            sentiment_data = get_mock_sentiment()
            signal_data = get_mock_signal()
            risk_data = get_mock_risk()
            
            # Combine all data
            combined_data = {
                "type": "market_update",
                "data": {
                    "price": price_data,
                    "indicators": indicators_data,
                    "sentiment": sentiment_data,
                    "signal": signal_data,
                    "risk": risk_data
                },
                "timestamp": datetime.now().isoformat()
            }
            
            await manager.send_personal_message(json.dumps(combined_data), websocket)
            
            # Wait 5 seconds before next update
            await asyncio.sleep(5)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("WebSocket client disconnected")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
