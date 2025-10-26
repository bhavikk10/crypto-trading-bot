"""
Trading strategy module combining momentum and sentiment signals
Implements signal generation logic for crypto trading decisions
"""

import logging
from datetime import datetime
from typing import Dict, Tuple
import numpy as np

logger = logging.getLogger(__name__)

class TradingStrategy:
    """Trading strategy combining technical indicators and sentiment analysis"""
    
    def __init__(self):
        # Strategy parameters
        self.momentum_weight = 0.6      # Weight for momentum signals
        self.sentiment_weight = 0.4     # Weight for sentiment signals
        
        # Signal thresholds
        self.buy_threshold = 0.6        # Minimum score for buy signal
        self.sell_threshold = 0.4       # Maximum score for sell signal
        self.confidence_threshold = 0.7  # Minimum confidence for signal
        
        # Technical indicator thresholds
        self.rsi_oversold = 30
        self.rsi_overbought = 70
        self.adx_trend_threshold = 25
        self.adx_strong_trend = 40
        
        # Sentiment thresholds
        self.sentiment_bullish = 60
        self.sentiment_bearish = 40
        
    def generate_signal(self, price: float, rsi: float, adx: float, atr: float, sentiment_score: float) -> Dict:
        """
        Generate trading signal based on technical indicators and sentiment
        
        Args:
            price: Current price
            rsi: RSI value (0-100)
            adx: ADX value (0-100)
            atr: ATR value
            sentiment_score: Sentiment score (0-100)
            
        Returns:
            Dict with signal, confidence, and reasoning
        """
        try:
            # Calculate momentum signal
            momentum_signal, momentum_confidence = self._calculate_momentum_signal(rsi, adx)
            
            # Calculate sentiment signal
            sentiment_signal, sentiment_confidence = self._calculate_sentiment_signal(sentiment_score)
            
            # Combine signals with weights
            combined_signal = (momentum_signal * self.momentum_weight + 
                             sentiment_signal * self.sentiment_weight)
            
            # Calculate combined confidence
            combined_confidence = (momentum_confidence * self.momentum_weight + 
                                 sentiment_confidence * self.sentiment_weight)
            
            # Determine final signal
            if combined_signal >= self.buy_threshold and combined_confidence >= self.confidence_threshold:
                signal = "BUY"
                signal_strength = "Strong" if combined_signal >= 0.8 else "Moderate"
            elif combined_signal <= self.sell_threshold and combined_confidence >= self.confidence_threshold:
                signal = "SELL"
                signal_strength = "Strong" if combined_signal <= 0.2 else "Moderate"
            else:
                signal = "HOLD"
                signal_strength = "Neutral"
            
            # Generate reasoning
            reasoning = self._generate_reasoning(
                signal, signal_strength, momentum_signal, sentiment_signal,
                rsi, adx, sentiment_score, combined_confidence
            )
            
            result = {
                "signal": signal,
                "signal_strength": signal_strength,
                "confidence": round(combined_confidence, 3),
                "momentum_score": round(momentum_signal, 3),
                "sentiment_score": round(sentiment_signal, 3),
                "combined_score": round(combined_signal, 3),
                "reasoning": reasoning,
                "timestamp": datetime.now()
            }
            
            logger.info(f"Trading signal generated: {signal} ({signal_strength}) - Confidence: {combined_confidence:.3f}")
            return result
            
        except Exception as e:
            logger.error(f"Error generating trading signal: {e}")
            return self._get_default_signal()
    
    def _calculate_momentum_signal(self, rsi: float, adx: float) -> Tuple[float, float]:
        """
        Calculate momentum signal based on RSI and ADX
        
        Args:
            rsi: RSI value (0-100)
            adx: ADX value (0-100)
            
        Returns:
            Tuple of (momentum_signal, confidence)
        """
        try:
            momentum_score = 0.5  # Start neutral
            confidence = 0.5
            
            # RSI analysis
            if rsi < self.rsi_oversold:
                momentum_score += 0.3  # Oversold - bullish
                confidence += 0.2
            elif rsi > self.rsi_overbought:
                momentum_score -= 0.3  # Overbought - bearish
                confidence += 0.2
            elif 40 <= rsi <= 60:
                momentum_score += 0.1  # Neutral zone - slightly bullish
                confidence += 0.1
            
            # ADX analysis (trend strength)
            if adx > self.adx_strong_trend:
                confidence += 0.3  # Strong trend
            elif adx > self.adx_trend_threshold:
                confidence += 0.2  # Moderate trend
            else:
                confidence -= 0.1  # Weak trend
            
            # Normalize scores
            momentum_score = max(0, min(1, momentum_score))
            confidence = max(0, min(1, confidence))
            
            return momentum_score, confidence
            
        except Exception as e:
            logger.error(f"Error calculating momentum signal: {e}")
            return 0.5, 0.5
    
    def _calculate_sentiment_signal(self, sentiment_score: float) -> Tuple[float, float]:
        """
        Calculate sentiment signal
        
        Args:
            sentiment_score: Sentiment score (0-100)
            
        Returns:
            Tuple of (sentiment_signal, confidence)
        """
        try:
            # Convert sentiment score to 0-1 scale
            sentiment_signal = sentiment_score / 100.0
            
            # Calculate confidence based on how extreme the sentiment is
            if sentiment_score >= 80 or sentiment_score <= 20:
                confidence = 0.9  # Very high confidence for extreme sentiment
            elif sentiment_score >= 70 or sentiment_score <= 30:
                confidence = 0.8  # High confidence for strong sentiment
            elif sentiment_score >= 60 or sentiment_score <= 40:
                confidence = 0.7  # Moderate confidence for moderate sentiment
            else:
                confidence = 0.6  # Lower confidence for neutral sentiment
            
            return sentiment_signal, confidence
            
        except Exception as e:
            logger.error(f"Error calculating sentiment signal: {e}")
            return 0.5, 0.5
    
    def _generate_reasoning(self, signal: str, strength: str, momentum_score: float, 
                          sentiment_score: float, rsi: float, adx: float, 
                          sentiment_value: float, confidence: float) -> str:
        """
        Generate human-readable reasoning for the trading signal
        
        Args:
            signal: Trading signal (BUY/SELL/HOLD)
            strength: Signal strength (Strong/Moderate/Neutral)
            momentum_score: Momentum score (0-1)
            sentiment_score: Sentiment score (0-1)
            rsi: RSI value
            adx: ADX value
            sentiment_value: Raw sentiment value
            confidence: Combined confidence
            
        Returns:
            Reasoning string
        """
        try:
            reasoning_parts = []
            
            # Add signal and strength
            reasoning_parts.append(f"Signal: {signal} ({strength})")
            
            # Add momentum analysis
            if momentum_score > 0.6:
                reasoning_parts.append("Momentum: Bullish")
            elif momentum_score < 0.4:
                reasoning_parts.append("Momentum: Bearish")
            else:
                reasoning_parts.append("Momentum: Neutral")
            
            # Add RSI analysis
            if rsi < self.rsi_oversold:
                reasoning_parts.append(f"RSI: Oversold ({rsi:.1f})")
            elif rsi > self.rsi_overbought:
                reasoning_parts.append(f"RSI: Overbought ({rsi:.1f})")
            else:
                reasoning_parts.append(f"RSI: Neutral ({rsi:.1f})")
            
            # Add ADX analysis
            if adx > self.adx_strong_trend:
                reasoning_parts.append(f"Trend: Strong ({adx:.1f})")
            elif adx > self.adx_trend_threshold:
                reasoning_parts.append(f"Trend: Moderate ({adx:.1f})")
            else:
                reasoning_parts.append(f"Trend: Weak ({adx:.1f})")
            
            # Add sentiment analysis
            if sentiment_value >= self.sentiment_bullish:
                reasoning_parts.append(f"Sentiment: Bullish ({sentiment_value:.1f})")
            elif sentiment_value <= self.sentiment_bearish:
                reasoning_parts.append(f"Sentiment: Bearish ({sentiment_value:.1f})")
            else:
                reasoning_parts.append(f"Sentiment: Neutral ({sentiment_value:.1f})")
            
            # Add confidence
            reasoning_parts.append(f"Confidence: {confidence:.1%}")
            
            return " | ".join(reasoning_parts)
            
        except Exception as e:
            logger.error(f"Error generating reasoning: {e}")
            return f"Signal: {signal} | Error generating detailed reasoning"
    
    def calculate_signal_strength(self, combined_score: float) -> str:
        """
        Calculate signal strength based on combined score
        
        Args:
            combined_score: Combined signal score (0-1)
            
        Returns:
            Signal strength string
        """
        if combined_score >= 0.8:
            return "Very Strong"
        elif combined_score >= 0.6:
            return "Strong"
        elif combined_score >= 0.4:
            return "Moderate"
        else:
            return "Weak"
    
    def validate_signal(self, signal_data: Dict) -> Dict:
        """
        Validate trading signal data
        
        Args:
            signal_data: Signal data dictionary
            
        Returns:
            Dict with validation results
        """
        try:
            warnings = []
            errors = []
            
            # Check signal validity
            signal = signal_data.get('signal', '')
            if signal not in ['BUY', 'SELL', 'HOLD']:
                errors.append(f"Invalid signal: {signal}")
            
            # Check confidence
            confidence = signal_data.get('confidence', 0)
            if confidence < 0 or confidence > 1:
                errors.append(f"Invalid confidence: {confidence}")
            elif confidence < 0.5:
                warnings.append(f"Low confidence signal: {confidence:.3f}")
            
            # Check scores
            momentum_score = signal_data.get('momentum_score', 0)
            sentiment_score = signal_data.get('sentiment_score', 0)
            
            if momentum_score < 0 or momentum_score > 1:
                errors.append(f"Invalid momentum score: {momentum_score}")
            
            if sentiment_score < 0 or sentiment_score > 1:
                errors.append(f"Invalid sentiment score: {sentiment_score}")
            
            validation_result = {
                "is_valid": len(errors) == 0,
                "warnings": warnings,
                "errors": errors,
                "timestamp": datetime.now()
            }
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error validating signal: {e}")
            return {
                "is_valid": False,
                "warnings": [],
                "errors": [f"Validation error: {str(e)}"],
                "timestamp": datetime.now()
            }
    
    def _get_default_signal(self) -> Dict:
        """Get default signal when calculation fails"""
        return {
            "signal": "HOLD",
            "signal_strength": "Neutral",
            "confidence": 0.5,
            "momentum_score": 0.5,
            "sentiment_score": 0.5,
            "combined_score": 0.5,
            "reasoning": "Default signal due to calculation error",
            "timestamp": datetime.now()
        }
    
    def update_strategy_parameters(self, **kwargs):
        """Update strategy parameters"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                logger.info(f"Updated strategy parameter {key} to {value}")
    
    def get_strategy_parameters(self) -> Dict:
        """Get current strategy parameters"""
        return {
            "momentum_weight": self.momentum_weight,
            "sentiment_weight": self.sentiment_weight,
            "buy_threshold": self.buy_threshold,
            "sell_threshold": self.sell_threshold,
            "confidence_threshold": self.confidence_threshold,
            "rsi_oversold": self.rsi_oversold,
            "rsi_overbought": self.rsi_overbought,
            "adx_trend_threshold": self.adx_trend_threshold,
            "adx_strong_trend": self.adx_strong_trend,
            "sentiment_bullish": self.sentiment_bullish,
            "sentiment_bearish": self.sentiment_bearish
        }
