"""
Risk management module for crypto trading
Implements ATR-based position sizing and stop-loss calculations
"""

import logging
from datetime import datetime
from typing import Dict, Tuple
import numpy as np

logger = logging.getLogger(__name__)

class RiskManager:
    """Risk management for crypto trading positions"""
    
    def __init__(self):
        # Risk management parameters
        self.max_position_size = 0.02  # 2% of portfolio per trade
        self.risk_per_trade = 0.01     # 1% risk per trade
        self.atr_multiplier = 2.0      # ATR multiplier for stop loss
        self.risk_reward_ratio = 2.0   # Minimum risk:reward ratio
        self.max_portfolio_risk = 0.05 # 5% maximum portfolio risk
        
    def calculate_risk_controls(self, current_price: float, atr: float, portfolio_value: float = 10000.0) -> Dict:
        """
        Calculate risk management controls for a position
        
        Args:
            current_price: Current price of the asset
            atr: Average True Range for volatility measurement
            portfolio_value: Total portfolio value
            
        Returns:
            Dict with position size, stop loss, take profit, and risk metrics
        """
        try:
            # Calculate position size based on risk per trade
            risk_amount = portfolio_value * self.risk_per_trade
            
            # Calculate stop loss distance using ATR
            stop_loss_distance = atr * self.atr_multiplier
            
            # Calculate stop loss price
            stop_loss_price = current_price - stop_loss_distance
            
            # Calculate position size based on risk amount and stop loss distance
            position_size = risk_amount / stop_loss_distance
            
            # Apply maximum position size limit
            max_position_value = portfolio_value * self.max_position_size
            max_position_size_by_value = max_position_value / current_price
            
            position_size = min(position_size, max_position_size_by_value)
            
            # Calculate take profit based on risk:reward ratio
            take_profit_distance = stop_loss_distance * self.risk_reward_ratio
            take_profit_price = current_price + take_profit_distance
            
            # Calculate actual risk metrics
            actual_risk_amount = position_size * stop_loss_distance
            actual_risk_percentage = (actual_risk_amount / portfolio_value) * 100
            
            # Calculate potential profit
            potential_profit = position_size * take_profit_distance
            potential_profit_percentage = (potential_profit / portfolio_value) * 100
            
            # Calculate actual risk:reward ratio
            actual_risk_reward_ratio = take_profit_distance / stop_loss_distance
            
            result = {
                "position_size": round(position_size, 6),
                "position_value": round(position_size * current_price, 2),
                "stop_loss": round(stop_loss_price, 2),
                "take_profit": round(take_profit_price, 2),
                "risk_amount": round(actual_risk_amount, 2),
                "risk_percentage": round(actual_risk_percentage, 2),
                "potential_profit": round(potential_profit, 2),
                "potential_profit_percentage": round(potential_profit_percentage, 2),
                "risk_reward_ratio": round(actual_risk_reward_ratio, 2),
                "atr_multiplier": self.atr_multiplier,
                "timestamp": datetime.now()
            }
            
            logger.info(f"Risk controls calculated: Position size {position_size:.6f}, Risk {actual_risk_percentage:.2f}%")
            return result
            
        except Exception as e:
            logger.error(f"Error calculating risk controls: {e}")
            return self._get_default_risk_controls(current_price)
    
    def calculate_position_size(self, current_price: float, stop_loss_price: float, portfolio_value: float, risk_percentage: float = None) -> float:
        """
        Calculate position size based on stop loss and risk percentage
        
        Args:
            current_price: Current price of the asset
            stop_loss_price: Stop loss price
            portfolio_value: Total portfolio value
            risk_percentage: Risk percentage (default: self.risk_per_trade)
            
        Returns:
            Position size in units
        """
        try:
            if risk_percentage is None:
                risk_percentage = self.risk_per_trade
            
            # Calculate risk amount
            risk_amount = portfolio_value * risk_percentage
            
            # Calculate stop loss distance
            stop_loss_distance = current_price - stop_loss_price
            
            if stop_loss_distance <= 0:
                logger.warning("Invalid stop loss price")
                return 0.0
            
            # Calculate position size
            position_size = risk_amount / stop_loss_distance
            
            # Apply maximum position size limit
            max_position_value = portfolio_value * self.max_position_size
            max_position_size_by_value = max_position_value / current_price
            
            return min(position_size, max_position_size_by_value)
            
        except Exception as e:
            logger.error(f"Error calculating position size: {e}")
            return 0.0
    
    def calculate_stop_loss(self, current_price: float, atr: float, multiplier: float = None) -> float:
        """
        Calculate stop loss price using ATR
        
        Args:
            current_price: Current price of the asset
            atr: Average True Range
            multiplier: ATR multiplier (default: self.atr_multiplier)
            
        Returns:
            Stop loss price
        """
        try:
            if multiplier is None:
                multiplier = self.atr_multiplier
            
            stop_loss_distance = atr * multiplier
            stop_loss_price = current_price - stop_loss_distance
            
            return round(stop_loss_price, 2)
            
        except Exception as e:
            logger.error(f"Error calculating stop loss: {e}")
            return current_price * 0.95  # 5% stop loss fallback
    
    def calculate_take_profit(self, current_price: float, stop_loss_price: float, risk_reward_ratio: float = None) -> float:
        """
        Calculate take profit price based on risk:reward ratio
        
        Args:
            current_price: Current price of the asset
            stop_loss_price: Stop loss price
            risk_reward_ratio: Risk:reward ratio (default: self.risk_reward_ratio)
            
        Returns:
            Take profit price
        """
        try:
            if risk_reward_ratio is None:
                risk_reward_ratio = self.risk_reward_ratio
            
            stop_loss_distance = current_price - stop_loss_price
            take_profit_distance = stop_loss_distance * risk_reward_ratio
            take_profit_price = current_price + take_profit_distance
            
            return round(take_profit_price, 2)
            
        except Exception as e:
            logger.error(f"Error calculating take profit: {e}")
            return current_price * 1.10  # 10% take profit fallback
    
    def calculate_portfolio_risk(self, positions: list) -> Dict:
        """
        Calculate total portfolio risk
        
        Args:
            positions: List of position dictionaries
            
        Returns:
            Dict with portfolio risk metrics
        """
        try:
            total_risk = 0.0
            total_value = 0.0
            position_count = len(positions)
            
            for position in positions:
                total_risk += position.get('risk_amount', 0)
                total_value += position.get('position_value', 0)
            
            portfolio_risk_percentage = (total_risk / total_value) * 100 if total_value > 0 else 0
            
            risk_status = "Low"
            if portfolio_risk_percentage > self.max_portfolio_risk * 100:
                risk_status = "High"
            elif portfolio_risk_percentage > self.max_portfolio_risk * 50:
                risk_status = "Medium"
            
            result = {
                "total_risk_amount": round(total_risk, 2),
                "total_portfolio_value": round(total_value, 2),
                "portfolio_risk_percentage": round(portfolio_risk_percentage, 2),
                "position_count": position_count,
                "risk_status": risk_status,
                "max_allowed_risk": self.max_portfolio_risk * 100,
                "timestamp": datetime.now()
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error calculating portfolio risk: {e}")
            return {
                "total_risk_amount": 0.0,
                "total_portfolio_value": 0.0,
                "portfolio_risk_percentage": 0.0,
                "position_count": 0,
                "risk_status": "Unknown",
                "max_allowed_risk": self.max_portfolio_risk * 100,
                "timestamp": datetime.now()
            }
    
    def validate_risk_parameters(self, risk_controls: Dict) -> Dict:
        """
        Validate risk management parameters
        
        Args:
            risk_controls: Risk controls dictionary
            
        Returns:
            Dict with validation results
        """
        try:
            warnings = []
            errors = []
            
            # Check position size
            position_size = risk_controls.get('position_size', 0)
            if position_size <= 0:
                errors.append("Position size must be positive")
            
            # Check risk percentage
            risk_percentage = risk_controls.get('risk_percentage', 0)
            if risk_percentage > self.max_portfolio_risk * 100:
                errors.append(f"Risk percentage ({risk_percentage:.2f}%) exceeds maximum allowed ({self.max_portfolio_risk * 100:.2f}%)")
            
            # Check risk:reward ratio
            risk_reward_ratio = risk_controls.get('risk_reward_ratio', 0)
            if risk_reward_ratio < 1.0:
                warnings.append(f"Risk:reward ratio ({risk_reward_ratio:.2f}) is below recommended minimum (1.0)")
            
            # Check stop loss
            stop_loss = risk_controls.get('stop_loss', 0)
            current_price = risk_controls.get('current_price', 0)
            if stop_loss >= current_price:
                errors.append("Stop loss must be below current price")
            
            validation_result = {
                "is_valid": len(errors) == 0,
                "warnings": warnings,
                "errors": errors,
                "timestamp": datetime.now()
            }
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error validating risk parameters: {e}")
            return {
                "is_valid": False,
                "warnings": [],
                "errors": [f"Validation error: {str(e)}"],
                "timestamp": datetime.now()
            }
    
    def _get_default_risk_controls(self, current_price: float) -> Dict:
        """Get default risk controls when calculation fails"""
        return {
            "position_size": 0.001,
            "position_value": current_price * 0.001,
            "stop_loss": current_price * 0.95,
            "take_profit": current_price * 1.10,
            "risk_amount": current_price * 0.001 * 0.05,
            "risk_percentage": 0.5,
            "potential_profit": current_price * 0.001 * 0.10,
            "potential_profit_percentage": 1.0,
            "risk_reward_ratio": 2.0,
            "atr_multiplier": self.atr_multiplier,
            "timestamp": datetime.now()
        }
    
    def update_risk_parameters(self, **kwargs):
        """Update risk management parameters"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                logger.info(f"Updated {key} to {value}")
    
    def get_risk_parameters(self) -> Dict:
        """Get current risk management parameters"""
        return {
            "max_position_size": self.max_position_size,
            "risk_per_trade": self.risk_per_trade,
            "atr_multiplier": self.atr_multiplier,
            "risk_reward_ratio": self.risk_reward_ratio,
            "max_portfolio_risk": self.max_portfolio_risk
        }
