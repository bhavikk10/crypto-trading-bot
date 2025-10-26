"""
Enhanced sentiment analysis with multiple sources
Adds LunarCrash and MarketSai integration
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional
import numpy as np
import aiohttp

# Existing FinBERT implementation
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

logger = logging.getLogger(__name__)

class EnhancedSentimentAnalyzer:
    """Enhanced sentiment analysis with multiple sources"""
    
    def __init__(self):
        self.finbert_analyzer = None
        self.lunarcrash_api_key = None
        self.marketsai_api_key = None
        
    async def initialize(self, lunarcrash_key: str = None, marketsai_key: str = None):
        """Initialize all sentiment sources"""
        self.lunarcrash_api_key = lunarcrash_key
        self.marketsai_api_key = marketsai_key
        
        # Initialize FinBERT
        if TRANSFORMERS_AVAILABLE:
            try:
                model_name = "ProsusAI/finbert"
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                model = AutoModelForSequenceClassification.from_pretrained(model_name)
                self.finbert_analyzer = pipeline(
                    "sentiment-analysis",
                    model=model,
                    tokenizer=tokenizer,
                    return_all_scores=True
                )
                logger.info("FinBERT initialized successfully")
            except Exception as e:
                logger.error(f"FinBERT initialization failed: {e}")
    
    async def get_lunarcrash_sentiment(self) -> Dict:
        """Get sentiment from LunarCrash API"""
        if not self.lunarcrash_api_key:
            return {"error": "LunarCrash API key not provided"}
        
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://api.lunarcrash.com/v1/sentiment"
                headers = {"Authorization": f"Bearer {self.lunarcrash_api_key}"}
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "source": "lunarcrash",
                            "score": data.get("sentiment_score", 50),
                            "confidence": data.get("confidence", 0.5),
                            "timestamp": datetime.now()
                        }
                    else:
                        return {"error": f"LunarCrash API error: {response.status}"}
        except Exception as e:
            logger.error(f"LunarCrash API error: {e}")
            return {"error": str(e)}
    
    async def get_marketsai_sentiment(self) -> Dict:
        """Get sentiment from MarketSai API"""
        if not self.marketsai_api_key:
            return {"error": "MarketSai API key not provided"}
        
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://api.marketsai.com/v1/sentiment/crypto"
                headers = {"X-API-Key": self.marketsai_api_key}
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "source": "marketsai",
                            "score": data.get("sentiment_score", 50),
                            "confidence": data.get("confidence", 0.5),
                            "timestamp": datetime.now()
                        }
                    else:
                        return {"error": f"MarketSai API error: {response.status}"}
        except Exception as e:
            logger.error(f"MarketSai API error: {e}")
            return {"error": str(e)}
    
    async def get_finbert_sentiment(self, headlines: List[str]) -> Dict:
        """Get sentiment from FinBERT"""
        if not self.finbert_analyzer:
            return {"error": "FinBERT not initialized"}
        
        try:
            sentiment_scores = []
            for headline in headlines:
                result = self.finbert_analyzer(headline)
                for score_dict in result[0]:
                    if score_dict['label'] == 'positive':
                        sentiment_scores.append(score_dict['score'])
                    elif score_dict['label'] == 'negative':
                        sentiment_scores.append(-score_dict['score'])
            
            if sentiment_scores:
                avg_sentiment = np.mean(sentiment_scores)
                confidence = np.std(sentiment_scores)
                score = (avg_sentiment + 1) * 50  # Convert to 0-100 scale
                
                return {
                    "source": "finbert",
                    "score": max(0, min(100, score)),
                    "confidence": max(0, min(1, confidence)),
                    "timestamp": datetime.now()
                }
            else:
                return {"error": "No sentiment scores generated"}
                
        except Exception as e:
            logger.error(f"FinBERT analysis error: {e}")
            return {"error": str(e)}
    
    async def get_combined_sentiment(self, headlines: List[str] = None) -> Dict:
        """Get combined sentiment from all available sources"""
        if headlines is None:
            headlines = [
                "Bitcoin reaches new all-time high as institutional adoption grows",
                "Crypto market shows signs of recovery after recent dip",
                "Major banks announce cryptocurrency trading services"
            ]
        
        results = []
        
        # Get FinBERT sentiment
        finbert_result = await self.get_finbert_sentiment(headlines)
        if "error" not in finbert_result:
            results.append(finbert_result)
        
        # Get LunarCrash sentiment (if API key provided)
        if self.lunarcrash_api_key:
            lunarcrash_result = await self.get_lunarcrash_sentiment()
            if "error" not in lunarcrash_result:
                results.append(lunarcrash_result)
        
        # Get MarketSai sentiment (if API key provided)
        if self.marketsai_api_key:
            marketsai_result = await self.get_marketsai_sentiment()
            if "error" not in marketsai_result:
                results.append(marketsai_result)
        
        if not results:
            # Fallback to mock sentiment
            return {
                "score": 50.0,
                "sentiment": "Neutral",
                "confidence": 0.5,
                "sources": ["mock"],
                "timestamp": datetime.now()
            }
        
        # Combine results (weighted average)
        total_score = 0
        total_weight = 0
        sources = []
        
        for result in results:
            weight = result.get("confidence", 0.5)
            total_score += result["score"] * weight
            total_weight += weight
            sources.append(result["source"])
        
        combined_score = total_score / total_weight if total_weight > 0 else 50
        
        # Determine sentiment label
        if combined_score >= 70:
            sentiment_label = "Very Bullish"
        elif combined_score >= 60:
            sentiment_label = "Bullish"
        elif combined_score >= 40:
            sentiment_label = "Neutral"
        elif combined_score >= 30:
            sentiment_label = "Bearish"
        else:
            sentiment_label = "Very Bearish"
        
        return {
            "score": round(combined_score, 2),
            "sentiment": sentiment_label,
            "confidence": round(total_weight / len(results), 2),
            "sources": sources,
            "timestamp": datetime.now()
        }
