"""
Redis logger module for data persistence and caching
Handles logging of trades, market data, and system events
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional
import redis
import asyncio

logger = logging.getLogger(__name__)

class RedisLogger:
    """Redis-based logging and data persistence for crypto trading bot"""
    
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client
        self.data_dir = "data"
        self._ensure_data_directory()
        
        # Redis key prefixes
        self.PRICE_PREFIX = "price:"
        self.INDICATORS_PREFIX = "indicators:"
        self.SENTIMENT_PREFIX = "sentiment:"
        self.SIGNAL_PREFIX = "signal:"
        self.RISK_PREFIX = "risk:"
        self.TRADE_PREFIX = "trade:"
        self.ALERT_PREFIX = "alert:"
        
        # Data retention settings
        self.max_redis_entries = 1000
        self.backup_interval = 300  # 5 minutes
        
    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            logger.info(f"Created data directory: {self.data_dir}")
    
    async def log_price(self, price_data: Dict) -> bool:
        """
        Log price data to Redis and local file
        
        Args:
            price_data: Price data dictionary
            
        Returns:
            Success status
        """
        try:
            timestamp = datetime.now()
            key = f"{self.PRICE_PREFIX}{price_data['symbol']}:{timestamp.isoformat()}"
            
            # Add timestamp if not present
            if 'timestamp' not in price_data:
                price_data['timestamp'] = timestamp
            
            # Store in Redis
            self.redis_client.setex(key, 86400, json.dumps(price_data, default=str))  # 24 hour TTL
            
            # Store in local file
            await self._append_to_file("prices.json", price_data)
            
            # Cleanup old entries
            await self._cleanup_old_entries(self.PRICE_PREFIX)
            
            logger.debug(f"Logged price data for {price_data['symbol']}")
            return True
            
        except Exception as e:
            logger.error(f"Error logging price data: {e}")
            return False
    
    async def log_indicators(self, indicators_data: Dict) -> bool:
        """
        Log technical indicators data
        
        Args:
            indicators_data: Indicators data dictionary
            
        Returns:
            Success status
        """
        try:
            timestamp = datetime.now()
            key = f"{self.INDICATORS_PREFIX}{timestamp.isoformat()}"
            
            # Add timestamp if not present
            if 'timestamp' not in indicators_data:
                indicators_data['timestamp'] = timestamp
            
            # Store in Redis
            self.redis_client.setex(key, 86400, json.dumps(indicators_data, default=str))
            
            # Store in local file
            await self._append_to_file("indicators.json", indicators_data)
            
            # Cleanup old entries
            await self._cleanup_old_entries(self.INDICATORS_PREFIX)
            
            logger.debug("Logged indicators data")
            return True
            
        except Exception as e:
            logger.error(f"Error logging indicators data: {e}")
            return False
    
    async def log_sentiment(self, sentiment_data: Dict) -> bool:
        """
        Log sentiment analysis data
        
        Args:
            sentiment_data: Sentiment data dictionary
            
        Returns:
            Success status
        """
        try:
            timestamp = datetime.now()
            key = f"{self.SENTIMENT_PREFIX}{timestamp.isoformat()}"
            
            # Add timestamp if not present
            if 'timestamp' not in sentiment_data:
                sentiment_data['timestamp'] = timestamp
            
            # Store in Redis
            self.redis_client.setex(key, 86400, json.dumps(sentiment_data, default=str))
            
            # Store in local file
            await self._append_to_file("sentiment.json", sentiment_data)
            
            # Cleanup old entries
            await self._cleanup_old_entries(self.SENTIMENT_PREFIX)
            
            logger.debug("Logged sentiment data")
            return True
            
        except Exception as e:
            logger.error(f"Error logging sentiment data: {e}")
            return False
    
    async def log_signal(self, signal_data: Dict) -> bool:
        """
        Log trading signal data
        
        Args:
            signal_data: Signal data dictionary
            
        Returns:
            Success status
        """
        try:
            timestamp = datetime.now()
            key = f"{self.SIGNAL_PREFIX}{timestamp.isoformat()}"
            
            # Add timestamp if not present
            if 'timestamp' not in signal_data:
                signal_data['timestamp'] = timestamp
            
            # Store in Redis
            self.redis_client.setex(key, 86400, json.dumps(signal_data, default=str))
            
            # Store in local file
            await self._append_to_file("signals.json", signal_data)
            
            # Cleanup old entries
            await self._cleanup_old_entries(self.SIGNAL_PREFIX)
            
            logger.debug(f"Logged signal: {signal_data.get('signal', 'UNKNOWN')}")
            return True
            
        except Exception as e:
            logger.error(f"Error logging signal data: {e}")
            return False
    
    async def log_risk(self, risk_data: Dict) -> bool:
        """
        Log risk management data
        
        Args:
            risk_data: Risk data dictionary
            
        Returns:
            Success status
        """
        try:
            timestamp = datetime.now()
            key = f"{self.RISK_PREFIX}{timestamp.isoformat()}"
            
            # Add timestamp if not present
            if 'timestamp' not in risk_data:
                risk_data['timestamp'] = timestamp
            
            # Store in Redis
            self.redis_client.setex(key, 86400, json.dumps(risk_data, default=str))
            
            # Store in local file
            await self._append_to_file("risk.json", risk_data)
            
            # Cleanup old entries
            await self._cleanup_old_entries(self.RISK_PREFIX)
            
            logger.debug("Logged risk data")
            return True
            
        except Exception as e:
            logger.error(f"Error logging risk data: {e}")
            return False
    
    async def log_trade(self, trade_data: Dict) -> bool:
        """
        Log trade execution data
        
        Args:
            trade_data: Trade data dictionary
            
        Returns:
            Success status
        """
        try:
            timestamp = datetime.now()
            trade_id = trade_data.get('trade_id', f"trade_{timestamp.isoformat()}")
            key = f"{self.TRADE_PREFIX}{trade_id}"
            
            # Add timestamp if not present
            if 'timestamp' not in trade_data:
                trade_data['timestamp'] = timestamp
            
            # Store in Redis
            self.redis_client.setex(key, 604800, json.dumps(trade_data, default=str))  # 7 day TTL
            
            # Store in local file
            await self._append_to_file("trades.json", trade_data)
            
            logger.info(f"Logged trade: {trade_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error logging trade data: {e}")
            return False
    
    async def log_alert(self, alert_data: Dict) -> bool:
        """
        Log system alerts and notifications
        
        Args:
            alert_data: Alert data dictionary
            
        Returns:
            Success status
        """
        try:
            timestamp = datetime.now()
            key = f"{self.ALERT_PREFIX}{timestamp.isoformat()}"
            
            # Add timestamp if not present
            if 'timestamp' not in alert_data:
                alert_data['timestamp'] = timestamp
            
            # Store in Redis
            self.redis_client.setex(key, 86400, json.dumps(alert_data, default=str))
            
            # Store in local file
            await self._append_to_file("alerts.json", alert_data)
            
            logger.info(f"Alert logged: {alert_data.get('message', 'Unknown alert')}")
            return True
            
        except Exception as e:
            logger.error(f"Error logging alert data: {e}")
            return False
    
    async def _append_to_file(self, filename: str, data: Dict):
        """Append data to local JSON file"""
        try:
            filepath = os.path.join(self.data_dir, filename)
            
            # Read existing data
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    try:
                        existing_data = json.load(f)
                    except json.JSONDecodeError:
                        existing_data = []
            else:
                existing_data = []
            
            # Append new data
            existing_data.append(data)
            
            # Keep only last 1000 entries
            if len(existing_data) > 1000:
                existing_data = existing_data[-1000:]
            
            # Write back to file
            with open(filepath, 'w') as f:
                json.dump(existing_data, f, indent=2, default=str)
                
        except Exception as e:
            logger.error(f"Error appending to file {filename}: {e}")
    
    async def _cleanup_old_entries(self, prefix: str):
        """Cleanup old Redis entries to prevent memory issues"""
        try:
            # Get all keys with prefix
            keys = self.redis_client.keys(f"{prefix}*")
            
            if len(keys) > self.max_redis_entries:
                # Sort by timestamp and remove oldest entries
                keys_with_timestamps = []
                for key in keys:
                    try:
                        # Extract timestamp from key
                        timestamp_str = key.decode('utf-8').split(':')[-1]
                        timestamp = datetime.fromisoformat(timestamp_str)
                        keys_with_timestamps.append((timestamp, key))
                    except:
                        continue
                
                # Sort by timestamp and remove oldest
                keys_with_timestamps.sort(key=lambda x: x[0])
                keys_to_remove = keys_with_timestamps[:-self.max_redis_entries]
                
                for _, key in keys_to_remove:
                    self.redis_client.delete(key)
                
                logger.debug(f"Cleaned up {len(keys_to_remove)} old entries for {prefix}")
                
        except Exception as e:
            logger.error(f"Error cleaning up old entries: {e}")
    
    async def get_recent_data(self, data_type: str, limit: int = 100) -> List[Dict]:
        """
        Get recent data from Redis
        
        Args:
            data_type: Type of data (price, indicators, sentiment, signal, risk, trade, alert)
            limit: Maximum number of entries to return
            
        Returns:
            List of data dictionaries
        """
        try:
            prefix_map = {
                'price': self.PRICE_PREFIX,
                'indicators': self.INDICATORS_PREFIX,
                'sentiment': self.SENTIMENT_PREFIX,
                'signal': self.SIGNAL_PREFIX,
                'risk': self.RISK_PREFIX,
                'trade': self.TRADE_PREFIX,
                'alert': self.ALERT_PREFIX
            }
            
            if data_type not in prefix_map:
                raise ValueError(f"Invalid data type: {data_type}")
            
            prefix = prefix_map[data_type]
            keys = self.redis_client.keys(f"{prefix}*")
            
            # Sort keys by timestamp (newest first)
            keys_with_timestamps = []
            for key in keys:
                try:
                    timestamp_str = key.decode('utf-8').split(':')[-1]
                    timestamp = datetime.fromisoformat(timestamp_str)
                    keys_with_timestamps.append((timestamp, key))
                except:
                    continue
            
            keys_with_timestamps.sort(key=lambda x: x[0], reverse=True)
            
            # Get data for recent keys
            recent_data = []
            for _, key in keys_with_timestamps[:limit]:
                try:
                    data = self.redis_client.get(key)
                    if data:
                        recent_data.append(json.loads(data))
                except:
                    continue
            
            return recent_data
            
        except Exception as e:
            logger.error(f"Error getting recent data: {e}")
            return []
    
    async def backup_data(self):
        """Backup all data to local files"""
        try:
            data_types = ['price', 'indicators', 'sentiment', 'signal', 'risk', 'trade', 'alert']
            
            for data_type in data_types:
                data = await self.get_recent_data(data_type, 1000)
                if data:
                    filepath = os.path.join(self.data_dir, f"{data_type}_backup.json")
                    with open(filepath, 'w') as f:
                        json.dump(data, f, indent=2, default=str)
            
            logger.info("Data backup completed")
            
        except Exception as e:
            logger.error(f"Error backing up data: {e}")
    
    def get_redis_status(self) -> Dict:
        """Get Redis connection status and info"""
        try:
            info = self.redis_client.info()
            return {
                "connected": True,
                "redis_version": info.get('redis_version', 'Unknown'),
                "used_memory": info.get('used_memory_human', 'Unknown'),
                "connected_clients": info.get('connected_clients', 0),
                "uptime": info.get('uptime_in_seconds', 0)
            }
        except Exception as e:
            return {
                "connected": False,
                "error": str(e)
            }
