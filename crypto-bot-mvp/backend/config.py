"""
Environment configuration loader for Crypto Trading Bot Dashboard
Loads API keys and configuration from .env file
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for API keys and settings"""
    
    # Coinbase API Configuration
    COINBASE_API_KEY: Optional[str] = os.getenv('COINBASE_API_KEY')
    COINBASE_API_SECRET: Optional[str] = os.getenv('COINBASE_API_SECRET')
    COINBASE_PASSPHRASE: Optional[str] = os.getenv('COINBASE_PASSPHRASE')
    
    # LunarCrash API Configuration
    LUNARCRASH_API_KEY: Optional[str] = os.getenv('LUNARCRASH_API_KEY')
    
    # MarketSai API Configuration
    MARKETSAI_API_KEY: Optional[str] = os.getenv('MARKETSAI_API_KEY')
    
    # Twilio Configuration
    TWILIO_SID: Optional[str] = os.getenv('TWILIO_SID')
    TWILIO_TOKEN: Optional[str] = os.getenv('TWILIO_TOKEN')
    TWILIO_PHONE_NUMBER: Optional[str] = os.getenv('TWILIO_PHONE_NUMBER')
    
    # Redis Configuration
    REDIS_URL: str = os.getenv('REDIS_URL', 'redis://localhost:6379')
    REDIS_PASSWORD: Optional[str] = os.getenv('REDIS_PASSWORD')
    
    # Application Configuration
    DEBUG: bool = os.getenv('DEBUG', 'True').lower() == 'true'
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    PORT: int = int(os.getenv('PORT', '8000'))
    
    # Trading Bot Configuration
    MAX_POSITION_SIZE: float = float(os.getenv('MAX_POSITION_SIZE', '0.02'))
    RISK_PER_TRADE: float = float(os.getenv('RISK_PER_TRADE', '0.01'))
    ATR_MULTIPLIER: float = float(os.getenv('ATR_MULTIPLIER', '2.0'))
    RISK_REWARD_RATIO: float = float(os.getenv('RISK_REWARD_RATIO', '2.0'))
    
    # Sentiment Analysis Configuration
    SENTIMENT_MODEL: str = os.getenv('SENTIMENT_MODEL', 'ProsusAI/finbert')
    SENTIMENT_CONFIDENCE_THRESHOLD: float = float(os.getenv('SENTIMENT_CONFIDENCE_THRESHOLD', '0.7'))
    
    # WebSocket Configuration
    WS_HEARTBEAT_INTERVAL: int = int(os.getenv('WS_HEARTBEAT_INTERVAL', '30'))
    WS_RECONNECT_ATTEMPTS: int = int(os.getenv('WS_RECONNECT_ATTEMPTS', '5'))
    WS_RECONNECT_DELAY: int = int(os.getenv('WS_RECONNECT_DELAY', '5000'))
    
    # Data Retention
    MAX_REDIS_ENTRIES: int = int(os.getenv('MAX_REDIS_ENTRIES', '1000'))
    BACKUP_INTERVAL: int = int(os.getenv('BACKUP_INTERVAL', '300'))
    MAX_HISTORY_LENGTH: int = int(os.getenv('MAX_HISTORY_LENGTH', '100'))
    
    # Security
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    ALLOWED_HOSTS: str = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1')
    
    # Development
    CORS_ORIGINS: str = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000')
    
    @classmethod
    def get_coinbase_credentials(cls) -> dict:
        """Get Coinbase API credentials"""
        return {
            'api_key': cls.COINBASE_API_KEY,
            'api_secret': cls.COINBASE_API_SECRET,
            'passphrase': cls.COINBASE_PASSPHRASE
        }
    
    @classmethod
    def has_coinbase_credentials(cls) -> bool:
        """Check if Coinbase credentials are available"""
        return all([
            cls.COINBASE_API_KEY,
            cls.COINBASE_API_SECRET
        ])
    
    @classmethod
    def has_lunarcrash_key(cls) -> bool:
        """Check if LunarCrash API key is available"""
        return cls.LUNARCRASH_API_KEY is not None
    
    @classmethod
    def has_marketsai_key(cls) -> bool:
        """Check if MarketSai API key is available"""
        return cls.MARKETSAI_API_KEY is not None
    
    @classmethod
    def has_twilio_credentials(cls) -> bool:
        """Check if Twilio credentials are available"""
        return all([
            cls.TWILIO_SID,
            cls.TWILIO_TOKEN,
            cls.TWILIO_PHONE_NUMBER
        ])
    
    @classmethod
    def get_status(cls) -> dict:
        """Get configuration status"""
        return {
            'coinbase_configured': cls.has_coinbase_credentials(),
            'lunarcrash_configured': cls.has_lunarcrash_key(),
            'marketsai_configured': cls.has_marketsai_key(),
            'twilio_configured': cls.has_twilio_credentials(),
            'redis_url': cls.REDIS_URL,
            'debug_mode': cls.DEBUG,
            'log_level': cls.LOG_LEVEL
        }

# Global config instance
config = Config()
