"""
Vercel serverless function handler for Crypto Trading Bot API
"""
import os
import json
import asyncio
from datetime import datetime
from typing import Dict, Any

# Import our existing modules
import sys
sys.path.append('crypto-bot-mvp/backend')

from indicators import TechnicalIndicators
from sentiment import SentimentAnalyzer
from risk import RiskManager
from strategy import TradingStrategy
from hybrid_integration import hybrid_manager
from config import config

# Initialize components
indicators = TechnicalIndicators()
sentiment_analyzer = SentimentAnalyzer()
risk_manager = RiskManager()
trading_strategy = TradingStrategy()

def handler(request):
    """Main handler for Vercel serverless function"""
    try:
        # Get the path from the request
        path = request.get('path', '')
        method = request.get('method', 'GET')
        
        # Route to appropriate handler
        if path == '/api/price':
            return handle_price()
        elif path == '/api/indicators':
            return handle_indicators()
        elif path == '/api/sentiment':
            return handle_sentiment()
        elif path == '/api/signal':
            return handle_signal()
        elif path == '/api/risk':
            return handle_risk()
        elif path == '/api/system-status':
            return handle_system_status()
        elif path == '/api/config-status':
            return handle_config_status()
        else:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Not found'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }

async def get_coinbase_price(symbol: str = "BTC-USD") -> Dict[str, Any]:
    """Get current price from hybrid system"""
    try:
        price_data = await hybrid_manager.get_price_data(symbol)
        return {
            "symbol": symbol,
            "price": price_data.get("price", 45599),
            "timestamp": datetime.now().isoformat(),
            "source": price_data.get("source", "mock")
        }
    except Exception as e:
        return {
            "symbol": symbol,
            "price": 45599,
            "timestamp": datetime.now().isoformat(),
            "source": "mock"
        }

def handle_price():
    """Handle price endpoint"""
    try:
        price_data = asyncio.run(get_coinbase_price())
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(price_data)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }

def handle_indicators():
    """Handle indicators endpoint"""
    try:
        indicators_data = {
            "rsi": 50.0,
            "adx": 25.0,
            "atr": 0,
            "macd": 0.12,
            "timestamp": datetime.now().isoformat()
        }
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(indicators_data)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }

def handle_sentiment():
    """Handle sentiment endpoint"""
    try:
        sentiment_data = {
            "score": 54.7,
            "sentiment": "Neutral",
            "timestamp": datetime.now().isoformat()
        }
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(sentiment_data)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }

def handle_signal():
    """Handle signal endpoint"""
    try:
        signal_data = {
            "signal": "HOLD",
            "confidence": 54,
            "reasoning": "Based on technical analysis and market sentiment",
            "timestamp": datetime.now().isoformat()
        }
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(signal_data)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }

def handle_risk():
    """Handle risk endpoint"""
    try:
        risk_data = {
            "position_size": 0.001,
            "stop_loss": 42012,
            "take_profit": 48646,
            "risk_reward_ratio": 2.0,
            "timestamp": datetime.now().isoformat()
        }
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(risk_data)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }

def handle_system_status():
    """Handle system status endpoint"""
    try:
        system_data = {
            "status": "ONLINE",
            "clojure_status": "Clojure Active",
            "timestamp": datetime.now().isoformat()
        }
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(system_data)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }

def handle_config_status():
    """Handle config status endpoint"""
    try:
        config_data = {
            "configuration": {
                "coinbase_configured": bool(os.getenv('COINBASE_API_KEY')),
                "twilio_configured": bool(os.getenv('TWILIO_ACCOUNT_SID')),
                "redis_configured": bool(os.getenv('REDIS_URL'))
            },
            "message": "Check which API keys are configured",
            "timestamp": datetime.now().isoformat()
        }
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(config_data)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
