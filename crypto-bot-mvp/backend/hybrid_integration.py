"""
Hybrid Crypto Trading Bot Dashboard
Integrates Python FastAPI backend with existing Clojure crypto infrastructure

This module provides Python wrappers to consume data from the existing Clojure system
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
import redis
import aiohttp
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ClojureConfig:
    """Configuration for Clojure system integration"""
    redis_host: str = "127.0.0.1"
    redis_port: int = 6379
    clojure_api_port: int = 8080  # Clojure HTTP API port
    clojure_api_base: str = "http://localhost:8080"
    gdax_products: List[str] = None
    
    def __post_init__(self):
        if self.gdax_products is None:
            self.gdax_products = ["BTC-USD", "ETH-USD", "LTC-USD"]

class ClojureDataConsumer:
    """Consumes data from existing Clojure crypto system"""
    
    def __init__(self, config: ClojureConfig):
        self.config = config
        self.redis_client = redis.Redis(
            host=config.redis_host, 
            port=config.redis_port, 
            decode_responses=True
        )
        
    async def get_gdax_price_data(self, product_id: str = "BTC-USD") -> Dict:
        """
        Get price data from Clojure GDAX integration via HTTP API
        """
        try:
            # Try HTTP API first
            async with aiohttp.ClientSession() as session:
                url = f"{self.config.clojure_api_base}/gdax/price/{product_id}"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if "error" not in data:
                            return {
                                "symbol": product_id,
                                "price": float(data.get("price", 0)),
                                "timestamp": datetime.now(),
                                "source": "clojure-gdax-http"
                            }
            
            # Fallback to Redis direct access
            price_key = f"gdax:price:{product_id}"
            price_data = self.redis_client.get(price_key)
            
            if price_data:
                data = json.loads(price_data)
                return {
                    "symbol": product_id,
                    "price": float(data.get("price", 0)),
                    "timestamp": datetime.now(),
                    "source": "clojure-gdax-redis"
                }
            else:
                # Fallback to mock data if no Clojure data available
                return await self._get_mock_price_data(product_id)
                
        except Exception as e:
            logger.error(f"Error getting GDAX price data: {e}")
            return await self._get_mock_price_data(product_id)
    
    async def get_gdax_order_book(self, product_id: str = "BTC-USD") -> Dict:
        """Get order book data from Clojure system"""
        try:
            book_key = f"gdax:book:{product_id}"
            book_data = self.redis_client.get(book_key)
            
            if book_data:
                return json.loads(book_data)
            else:
                return {"bids": [], "asks": [], "timestamp": datetime.now()}
                
        except Exception as e:
            logger.error(f"Error getting order book: {e}")
            return {"bids": [], "asks": [], "timestamp": datetime.now()}
    
    async def get_gdax_history(self, product_id: str = "BTC-USD", limit: int = 100) -> List[Dict]:
        """Get historical data from Clojure system via HTTP API"""
        try:
            # Try HTTP API first
            async with aiohttp.ClientSession() as session:
                url = f"{self.config.clojure_api_base}/gdax/history/{product_id}/{limit}"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if isinstance(data, list) and len(data) > 0:
                            return data
            
            # Fallback to Redis direct access
            history_key = f"gdax:history:{product_id}"
            history_data = self.redis_client.lrange(history_key, -limit, -1)
            
            if history_data:
                return [json.loads(entry) for entry in history_data]
            else:
                return await self._get_mock_history_data(product_id, limit)
                
        except Exception as e:
            logger.error(f"Error getting history data: {e}")
            return await self._get_mock_history_data(product_id, limit)
    
    async def get_binance_data(self, symbol: str = "BTCUSDT") -> Dict:
        """Get Binance data from Clojure system"""
        try:
            binance_key = f"binance:price:{symbol}"
            binance_data = self.redis_client.get(binance_key)
            
            if binance_data:
                data = json.loads(binance_data)
                return {
                    "symbol": symbol,
                    "price": float(data.get("price", 0)),
                    "timestamp": datetime.now(),
                    "source": "clojure-binance"
                }
            else:
                return await self._get_mock_price_data(symbol.replace("USDT", "-USD"))
                
        except Exception as e:
            logger.error(f"Error getting Binance data: {e}")
            return await self._get_mock_price_data(symbol.replace("USDT", "-USD"))
    
    async def get_twilio_alerts(self) -> List[Dict]:
        """Get Twilio alerts from Clojure system"""
        try:
            alerts_key = "twilio:alerts"
            alerts_data = self.redis_client.lrange(alerts_key, -50, -1)  # Last 50 alerts
            
            if alerts_data:
                return [json.loads(alert) for alert in alerts_data]
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error getting Twilio alerts: {e}")
            return []
    
    async def _get_mock_price_data(self, symbol: str) -> Dict:
        """Fallback mock price data"""
        import random
        base_price = 45000 if "BTC" in symbol else 3000 if "ETH" in symbol else 100
        price = base_price + random.uniform(-base_price * 0.05, base_price * 0.05)
        
        return {
            "symbol": symbol,
            "price": round(price, 2),
            "timestamp": datetime.now(),
            "source": "mock-fallback"
        }
    
    async def _get_mock_history_data(self, symbol: str, limit: int) -> List[Dict]:
        """Fallback mock history data"""
        import random
        base_price = 45000 if "BTC" in symbol else 3000 if "ETH" in symbol else 100
        
        history = []
        current_price = base_price
        
        for i in range(limit):
            # Generate realistic price movement
            change = random.uniform(-0.02, 0.02)  # ±2% change
            current_price *= (1 + change)
            
            history.append({
                "timestamp": datetime.now().isoformat(),
                "open": round(current_price * 0.999, 2),
                "high": round(current_price * 1.001, 2),
                "low": round(current_price * 0.998, 2),
                "close": round(current_price, 2),
                "volume": random.uniform(100, 1000)
            })
        
        return history
    
    def get_redis_status(self) -> Dict:
        """Get Redis connection status"""
        try:
            info = self.redis_client.info()
            return {
                "connected": True,
                "redis_version": info.get("redis_version", "Unknown"),
                "used_memory": info.get("used_memory_human", "Unknown"),
                "connected_clients": info.get("connected_clients", 0),
                "uptime": info.get("uptime_in_seconds", 0),
                "keyspace": info.get("db0", {})
            }
        except Exception as e:
            return {
                "connected": False,
                "error": str(e)
            }

class HybridDataManager:
    """Manages data from both Clojure and Python systems"""
    
    def __init__(self, clojure_config: ClojureConfig):
        self.clojure_consumer = ClojureDataConsumer(clojure_config)
        self.data_cache = {}
        self.last_update = {}
        
    async def get_hybrid_price_data(self, symbol: str = "BTC-USD") -> Dict:
        """
        Get price data prioritizing Clojure system, falling back to Python
        """
        try:
            # Try Clojure system first
            clojure_data = await self.clojure_consumer.get_gdax_price_data(symbol)
            
            if clojure_data.get("source") == "clojure-gdax":
                logger.info(f"Using Clojure GDAX data for {symbol}")
                return clojure_data
            else:
                # Fallback to Python Coinbase API
                logger.info(f"Falling back to Python Coinbase API for {symbol}")
                return await self._get_python_price_data(symbol)
                
        except Exception as e:
            logger.error(f"Error in hybrid price data: {e}")
            return await self._get_python_price_data(symbol)
    
    async def get_hybrid_history_data(self, symbol: str = "BTC-USD", limit: int = 100) -> List[Dict]:
        """Get historical data from both systems"""
        try:
            # Try Clojure system first
            clojure_history = await self.clojure_consumer.get_gdax_history(symbol, limit)
            
            if clojure_history and len(clojure_history) > 0:
                logger.info(f"Using Clojure history data for {symbol}")
                return clojure_history
            else:
                # Fallback to Python Coinbase API
                logger.info(f"Falling back to Python Coinbase API history for {symbol}")
                return await self._get_python_history_data(symbol, limit)
                
        except Exception as e:
            logger.error(f"Error in hybrid history data: {e}")
            return await self._get_python_history_data(symbol, limit)
    
    async def _get_python_price_data(self, symbol: str) -> Dict:
        """Fallback to Python Coinbase Advanced Trade API"""
        try:
            async with aiohttp.ClientSession() as session:
                # Use Coinbase Advanced Trade API (newer API)
                url = f"https://api.coinbase.com/api/v3/brokerage/market/products/{symbol}/ticker"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "symbol": symbol,
                            "price": float(data["price"]),
                            "timestamp": datetime.now(),
                            "source": "python-coinbase-advanced"
                        }
                    else:
                        # Fallback to public API
                        url_fallback = f"https://api.exchange.coinbase.com/products/{symbol}/ticker"
                        async with session.get(url_fallback) as response_fallback:
                            if response_fallback.status == 200:
                                data = await response_fallback.json()
                                return {
                                    "symbol": symbol,
                                    "price": float(data["price"]),
                                    "timestamp": datetime.now(),
                                    "source": "python-coinbase-public"
                                }
                            else:
                                raise Exception(f"Coinbase API error: {response.status}")
        except Exception as e:
            logger.error(f"Python Coinbase API error: {e}")
            return await self.clojure_consumer._get_mock_price_data(symbol)
    
    async def _get_python_history_data(self, symbol: str, limit: int) -> List[Dict]:
        """Fallback to Python Coinbase API for history"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"https://api.exchange.coinbase.com/products/{symbol}/candles"
                params = {
                    "granularity": 3600,  # 1 hour candles
                    "start": datetime.now().isoformat()
                }
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return [{
                            "timestamp": datetime.fromtimestamp(candle[0]).isoformat(),
                            "low": candle[1],
                            "high": candle[2],
                            "open": candle[3],
                            "close": candle[4],
                            "volume": candle[5]
                        } for candle in data[-limit:]]
                    else:
                        raise Exception(f"Coinbase API error: {response.status}")
        except Exception as e:
            logger.error(f"Python Coinbase API history error: {e}")
            return await self.clojure_consumer._get_mock_history_data(symbol, limit)
    
    async def get_system_status(self) -> Dict:
        """Get status of both Clojure and Python systems"""
        redis_status = self.clojure_consumer.get_redis_status()
        
        return {
            "clojure_system": {
                "redis_connected": redis_status.get("connected", False),
                "redis_info": redis_status,
                "available_data": await self._check_clojure_data_availability()
            },
            "python_system": {
                "status": "running",
                "fallback_available": True
            },
            "hybrid_mode": "active",
            "timestamp": datetime.now()
        }
    
    async def _check_clojure_data_availability(self) -> Dict:
        """Check what data is available from Clojure system"""
        try:
            available_data = {}
            
            # Check for GDAX data
            gdax_keys = self.clojure_consumer.redis_client.keys("gdax:*")
            available_data["gdax"] = len(gdax_keys) > 0
            
            # Check for Binance data
            binance_keys = self.clojure_consumer.redis_client.keys("binance:*")
            available_data["binance"] = len(binance_keys) > 0
            
            # Check for Twilio alerts
            twilio_keys = self.clojure_consumer.redis_client.keys("twilio:*")
            available_data["twilio"] = len(twilio_keys) > 0
            
            return available_data
            
        except Exception as e:
            logger.error(f"Error checking Clojure data availability: {e}")
            return {"error": str(e)}

# Global instance
clojure_config = ClojureConfig()
hybrid_manager = HybridDataManager(clojure_config)
