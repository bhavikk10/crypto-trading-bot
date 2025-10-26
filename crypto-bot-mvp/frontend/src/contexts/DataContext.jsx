import React, { createContext, useContext, useState, useEffect } from 'react';
import { useWebSocket } from './WebSocketContext';

const DataContext = createContext();

export const useData = () => {
  const context = useContext(DataContext);
  if (!context) {
    throw new Error('useData must be used within a DataProvider');
  }
  return context;
};

export const DataProvider = ({ children }) => {
  const { lastMessage } = useWebSocket();
  const [marketData, setMarketData] = useState({
    price: null,
    indicators: null,
    sentiment: null,
    signal: null,
    risk: null,
    lastUpdate: null
  });

  const [priceHistory, setPriceHistory] = useState([]);
  const [maxHistoryLength] = useState(100);

  useEffect(() => {
    if (lastMessage && lastMessage.type === 'market_update') {
      const data = lastMessage.data;
      
      setMarketData(prev => ({
        price: data.price || prev.price,
        indicators: data.indicators || prev.indicators,
        sentiment: data.sentiment || prev.sentiment,
        signal: data.signal || prev.signal,
        risk: data.risk || prev.risk,
        lastUpdate: new Date().toISOString()
      }));

      // Update price history for chart
      if (data.price) {
        setPriceHistory(prev => {
          const newHistory = [...prev, {
            timestamp: new Date().toISOString(),
            price: data.price.price,
            symbol: data.price.symbol
          }];
          
          // Keep only the last maxHistoryLength entries
          return newHistory.slice(-maxHistoryLength);
        });
      }
    }
  }, [lastMessage, maxHistoryLength]);

  const getPriceChange = () => {
    if (priceHistory.length < 2) return { change: 0, percentage: 0, direction: 'neutral' };
    
    const current = priceHistory[priceHistory.length - 1].price;
    const previous = priceHistory[priceHistory.length - 2].price;
    
    const change = current - previous;
    const percentage = (change / previous) * 100;
    
    return {
      change: change,
      percentage: percentage,
      direction: change > 0 ? 'positive' : change < 0 ? 'negative' : 'neutral'
    };
  };

  const getSignalStrength = (signal) => {
    if (!signal) return 'neutral';
    
    const strength = signal.signal_strength || 'Neutral';
    return strength.toLowerCase();
  };

  const getSentimentColor = (sentiment) => {
    if (!sentiment) return 'text-gray-600';
    
    const score = sentiment.score || 50;
    if (score >= 70) return 'text-success-600';
    if (score >= 60) return 'text-success-500';
    if (score <= 30) return 'text-danger-600';
    if (score <= 40) return 'text-danger-500';
    return 'text-gray-600';
  };

  const getIndicatorStatus = (indicators) => {
    if (!indicators) return { rsi: 'neutral', adx: 'neutral', atr: 'neutral' };
    
    const rsi = indicators.rsi || 50;
    const adx = indicators.adx || 25;
    const atr = indicators.atr || 0;
    
    return {
      rsi: rsi < 30 ? 'oversold' : rsi > 70 ? 'overbought' : 'neutral',
      adx: adx > 40 ? 'strong' : adx > 25 ? 'moderate' : 'weak',
      atr: atr > 0 ? 'active' : 'inactive'
    };
  };

  const formatPrice = (price) => {
    if (!price) return '$0.00';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(price);
  };

  const formatPercentage = (percentage) => {
    if (percentage === null || percentage === undefined) return '0.00%';
    return new Intl.NumberFormat('en-US', {
      style: 'percent',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(percentage / 100);
  };

  const formatTimestamp = (timestamp) => {
    if (!timestamp) return 'N/A';
    return new Date(timestamp).toLocaleTimeString();
  };

  const value = {
    marketData,
    priceHistory,
    getPriceChange,
    getSignalStrength,
    getSentimentColor,
    getIndicatorStatus,
    formatPrice,
    formatPercentage,
    formatTimestamp
  };

  return (
    <DataContext.Provider value={value}>
      {children}
    </DataContext.Provider>
  );
};
