"""
Technical indicators module for crypto trading analysis
Implements RSI, ADX, ATR calculations using ta-lib
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class TechnicalIndicators:
    """Technical analysis indicators for crypto trading"""
    
    def __init__(self):
        self.rsi_period = 14
        self.adx_period = 14
        self.atr_period = 14
        
    def calculate_rsi(self, historical_data: List[List], period: int = None) -> float:
        """
        Calculate Relative Strength Index (RSI)
        
        Args:
            historical_data: List of [timestamp, low, high, open, close, volume]
            period: RSI period (default: 14)
            
        Returns:
            RSI value (0-100)
        """
        if period is None:
            period = self.rsi_period
            
        try:
            # Extract closing prices
            closes = [float(candle[4]) for candle in historical_data[-period-1:]]
            
            if len(closes) < period + 1:
                return 50.0  # Neutral RSI if not enough data
            
            # Calculate price changes
            deltas = np.diff(closes)
            
            # Separate gains and losses
            gains = np.where(deltas > 0, deltas, 0)
            losses = np.where(deltas < 0, -deltas, 0)
            
            # Calculate average gains and losses
            avg_gains = np.mean(gains[-period:])
            avg_losses = np.mean(losses[-period:])
            
            if avg_losses == 0:
                return 100.0
            
            # Calculate RSI
            rs = avg_gains / avg_losses
            rsi = 100 - (100 / (1 + rs))
            
            return round(rsi, 2)
            
        except Exception as e:
            logger.error(f"Error calculating RSI: {e}")
            return 50.0
    
    def calculate_adx(self, historical_data: List[List], period: int = None) -> float:
        """
        Calculate Average Directional Index (ADX)
        
        Args:
            historical_data: List of [timestamp, low, high, open, close, volume]
            period: ADX period (default: 14)
            
        Returns:
            ADX value (0-100)
        """
        if period is None:
            period = self.adx_period
            
        try:
            # Extract high, low, close prices
            highs = [float(candle[2]) for candle in historical_data[-period-1:]]
            lows = [float(candle[1]) for candle in historical_data[-period-1:]]
            closes = [float(candle[4]) for candle in historical_data[-period-1:]]
            
            if len(highs) < period + 1:
                return 25.0  # Neutral ADX if not enough data
            
            # Calculate True Range (TR)
            tr_values = []
            for i in range(1, len(highs)):
                tr1 = highs[i] - lows[i]
                tr2 = abs(highs[i] - closes[i-1])
                tr3 = abs(lows[i] - closes[i-1])
                tr_values.append(max(tr1, tr2, tr3))
            
            # Calculate Directional Movement
            dm_plus = []
            dm_minus = []
            
            for i in range(1, len(highs)):
                high_diff = highs[i] - highs[i-1]
                low_diff = lows[i-1] - lows[i]
                
                if high_diff > low_diff and high_diff > 0:
                    dm_plus.append(high_diff)
                else:
                    dm_plus.append(0)
                    
                if low_diff > high_diff and low_diff > 0:
                    dm_minus.append(low_diff)
                else:
                    dm_minus.append(0)
            
            # Calculate smoothed values
            atr = np.mean(tr_values[-period:])
            di_plus = (np.mean(dm_plus[-period:]) / atr) * 100
            di_minus = (np.mean(dm_minus[-period:]) / atr) * 100
            
            # Calculate ADX
            dx = abs(di_plus - di_minus) / (di_plus + di_minus) * 100
            adx = dx  # Simplified ADX calculation
            
            return round(adx, 2)
            
        except Exception as e:
            logger.error(f"Error calculating ADX: {e}")
            return 25.0
    
    def calculate_atr(self, historical_data: List[List], period: int = None) -> float:
        """
        Calculate Average True Range (ATR)
        
        Args:
            historical_data: List of [timestamp, low, high, open, close, volume]
            period: ATR period (default: 14)
            
        Returns:
            ATR value
        """
        if period is None:
            period = self.atr_period
            
        try:
            # Extract high, low, close prices
            highs = [float(candle[2]) for candle in historical_data[-period-1:]]
            lows = [float(candle[1]) for candle in historical_data[-period-1:]]
            closes = [float(candle[4]) for candle in historical_data[-period-1:]]
            
            if len(highs) < period + 1:
                return 0.0
            
            # Calculate True Range (TR)
            tr_values = []
            for i in range(1, len(highs)):
                tr1 = highs[i] - lows[i]
                tr2 = abs(highs[i] - closes[i-1])
                tr3 = abs(lows[i] - closes[i-1])
                tr_values.append(max(tr1, tr2, tr3))
            
            # Calculate ATR as simple moving average of TR
            atr = np.mean(tr_values[-period:])
            
            return round(atr, 4)
            
        except Exception as e:
            logger.error(f"Error calculating ATR: {e}")
            return 0.0
    
    def get_momentum_signal(self, rsi: float, adx: float) -> str:
        """
        Generate momentum signal based on RSI and ADX
        
        Args:
            rsi: RSI value (0-100)
            adx: ADX value (0-100)
            
        Returns:
            Momentum signal: "Strong Bullish", "Bullish", "Neutral", "Bearish", "Strong Bearish"
        """
        try:
            # RSI thresholds
            rsi_oversold = 30
            rsi_overbought = 70
            rsi_neutral_low = 40
            rsi_neutral_high = 60
            
            # ADX thresholds
            adx_weak = 20
            adx_strong = 40
            
            # Determine momentum based on RSI and ADX
            if rsi < rsi_oversold and adx > adx_strong:
                return "Strong Bullish"
            elif rsi < rsi_neutral_low and adx > adx_weak:
                return "Bullish"
            elif rsi > rsi_overbought and adx > adx_strong:
                return "Strong Bearish"
            elif rsi > rsi_neutral_high and adx > adx_weak:
                return "Bearish"
            else:
                return "Neutral"
                
        except Exception as e:
            logger.error(f"Error generating momentum signal: {e}")
            return "Neutral"
    
    def calculate_bollinger_bands(self, historical_data: List[List], period: int = 20, std_dev: float = 2.0) -> Tuple[float, float, float]:
        """
        Calculate Bollinger Bands
        
        Args:
            historical_data: List of [timestamp, low, high, open, close, volume]
            period: Moving average period
            std_dev: Standard deviation multiplier
            
        Returns:
            Tuple of (upper_band, middle_band, lower_band)
        """
        try:
            closes = [float(candle[4]) for candle in historical_data[-period:]]
            
            if len(closes) < period:
                return 0.0, 0.0, 0.0
            
            middle_band = np.mean(closes)
            std = np.std(closes)
            
            upper_band = middle_band + (std_dev * std)
            lower_band = middle_band - (std_dev * std)
            
            return round(upper_band, 2), round(middle_band, 2), round(lower_band, 2)
            
        except Exception as e:
            logger.error(f"Error calculating Bollinger Bands: {e}")
            return 0.0, 0.0, 0.0
    
    def calculate_macd(self, historical_data: List[List], fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> Tuple[float, float, float]:
        """
        Calculate MACD (Moving Average Convergence Divergence)
        
        Args:
            historical_data: List of [timestamp, low, high, open, close, volume]
            fast_period: Fast EMA period
            slow_period: Slow EMA period
            signal_period: Signal line EMA period
            
        Returns:
            Tuple of (macd_line, signal_line, histogram)
        """
        try:
            closes = [float(candle[4]) for candle in historical_data]
            
            if len(closes) < slow_period:
                return 0.0, 0.0, 0.0
            
            # Calculate EMAs
            fast_ema = self._calculate_ema(closes, fast_period)
            slow_ema = self._calculate_ema(closes, slow_period)
            
            macd_line = fast_ema - slow_ema
            
            # Calculate signal line (EMA of MACD)
            macd_values = [fast_ema - slow_ema for fast_ema, slow_ema in zip(
                self._calculate_ema_series(closes, fast_period),
                self._calculate_ema_series(closes, slow_period)
            )]
            
            signal_line = self._calculate_ema(macd_values, signal_period)
            histogram = macd_line - signal_line
            
            return round(macd_line, 4), round(signal_line, 4), round(histogram, 4)
            
        except Exception as e:
            logger.error(f"Error calculating MACD: {e}")
            return 0.0, 0.0, 0.0
    
    def _calculate_ema(self, prices: List[float], period: int) -> float:
        """Calculate Exponential Moving Average"""
        if len(prices) < period:
            return prices[-1] if prices else 0.0
        
        multiplier = 2 / (period + 1)
        ema = prices[0]
        
        for price in prices[1:]:
            ema = (price * multiplier) + (ema * (1 - multiplier))
        
        return ema
    
    def _calculate_ema_series(self, prices: List[float], period: int) -> List[float]:
        """Calculate EMA series for MACD calculation"""
        if len(prices) < period:
            return prices
        
        multiplier = 2 / (period + 1)
        ema_series = [prices[0]]
        
        for price in prices[1:]:
            ema = (price * multiplier) + (ema_series[-1] * (1 - multiplier))
            ema_series.append(ema)
        
        return ema_series
