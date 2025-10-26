import React, { useState, useEffect } from 'react';
import { useWebSocket, useData } from '../contexts';
import Chart from './Chart';
import SignalCard from './SignalCard';
import MetricCard from './MetricCard';
import ConnectionStatus from './ConnectionStatus';

const Dashboard = () => {
  const { connectionStatus } = useWebSocket();
  const { marketData, getPriceChange, formatPrice, formatPercentage, formatTimestamp } = useData();
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const priceChange = getPriceChange();

  const formatTime = (date) => {
    return date.toLocaleTimeString('en-US', { 
      hour12: true, 
      hour: '2-digit', 
      minute: '2-digit',
      second: '2-digit'
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <header className="bg-black/30 backdrop-blur-md border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center space-x-4">
              <div className="w-16 h-16 bg-gradient-to-r from-yellow-400 via-orange-500 to-red-500 rounded-2xl flex items-center justify-center shadow-lg">
                <span className="text-3xl font-bold text-white">₿</span>
              </div>
              <div>
                <h1 className="text-4xl font-bold text-white">Crypto Trading Bot</h1>
                <p className="text-blue-200 text-lg">Professional Trading Dashboard</p>
              </div>
            </div>
            <div className="text-right">
              <div className="text-white text-xl font-semibold">{formatTime(currentTime)}</div>
              <ConnectionStatus />
            </div>
          </div>
        </div>
      </header>

      {/* Status Banner */}
      <div className="bg-gradient-to-r from-green-500/20 to-emerald-500/20 border border-green-500/30 mx-4 mt-6 rounded-xl p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-4 h-4 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-green-100 font-semibold text-lg">Live Market Data Active</span>
          </div>
          <div className="text-green-200 text-sm">
            Connected to Coinbase API • Real-time Updates
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Key Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* Bitcoin Price */}
          <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all duration-300">
            <div className="flex items-center justify-between mb-4">
              <div className="text-3xl">💰</div>
              <div className="text-green-400 text-sm font-semibold">LIVE</div>
            </div>
            <h3 className="text-white font-semibold text-lg mb-2">Bitcoin Price</h3>
            <div className="text-3xl font-bold text-white mb-2">
              {marketData.price ? formatPrice(marketData.price.price) : 'Loading...'}
            </div>
            <div className="flex items-center space-x-2">
              <span className={`text-sm font-semibold ${priceChange.direction === 'up' ? 'text-green-400' : 'text-red-400'}`}>
                {priceChange.change}
              </span>
              <span className={`text-sm font-semibold ${priceChange.direction === 'up' ? 'text-green-400' : 'text-red-400'}`}>
                ({priceChange.percentage})
              </span>
            </div>
          </div>

          {/* Market Sentiment */}
          <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all duration-300">
            <div className="flex items-center justify-between mb-4">
              <div className="text-3xl">📊</div>
              <div className="text-blue-400 text-sm font-semibold">ANALYSIS</div>
            </div>
            <h3 className="text-white font-semibold text-lg mb-2">Market Sentiment</h3>
            <div className="text-3xl font-bold text-white mb-2">
              {marketData.sentiment ? `${marketData.sentiment.score?.toFixed(1)}%` : 'Loading...'}
            </div>
            <div className="text-blue-200 text-sm">
              {marketData.sentiment ? marketData.sentiment.sentiment : 'Loading...'}
            </div>
          </div>

          {/* Trading Signal */}
          <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all duration-300">
            <div className="flex items-center justify-between mb-4">
              <div className="text-3xl">🎯</div>
              <div className="text-purple-400 text-sm font-semibold">SIGNAL</div>
            </div>
            <h3 className="text-white font-semibold text-lg mb-2">Trading Signal</h3>
            <div className="text-3xl font-bold text-white mb-2">
              {marketData.signal ? marketData.signal.signal : 'Loading...'}
            </div>
            <div className="text-purple-200 text-sm">
              {marketData.signal ? `${marketData.signal.confidence}% confidence` : 'Loading...'}
            </div>
          </div>

          {/* Risk Level */}
          <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all duration-300">
            <div className="flex items-center justify-between mb-4">
              <div className="text-3xl">🛡️</div>
              <div className="text-green-400 text-sm font-semibold">SAFE</div>
            </div>
            <h3 className="text-white font-semibold text-lg mb-2">Risk Level</h3>
            <div className="text-3xl font-bold text-green-400 mb-2">LOW</div>
            <div className="text-green-200 text-sm">
              Position: {marketData.risk ? `${marketData.risk.position_size?.toFixed(4)} BTC` : 'Loading...'}
            </div>
          </div>
        </div>

        {/* Charts and Analysis */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Price Chart */}
          <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20">
            <h3 className="text-xl font-semibold text-white mb-4 flex items-center">
              <span className="mr-2">📈</span>
              Price Movement & Trends
            </h3>
            <Chart />
          </div>

          {/* Trading Signals */}
          <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20">
            <h3 className="text-xl font-semibold text-white mb-4 flex items-center">
              <span className="mr-2">🎯</span>
              Trading Recommendations
            </h3>
            <SignalCard />
          </div>
        </div>

        {/* Technical Indicators */}
        <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20 mb-8">
          <h3 className="text-xl font-semibold text-white mb-6 flex items-center">
            <span className="mr-2">⚡</span>
            Technical Analysis
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-4xl font-bold text-blue-400 mb-2">
                {marketData.indicators ? marketData.indicators.rsi?.toFixed(1) : 'Loading...'}
              </div>
              <div className="text-white font-semibold text-lg">RSI</div>
              <div className="text-gray-400 text-sm">Relative Strength Index</div>
              <div className="text-blue-200 text-sm mt-1">
                {marketData.indicators ? 
                  (marketData.indicators.rsi < 30 ? 'Oversold' : 
                   marketData.indicators.rsi > 70 ? 'Overbought' : 'Neutral') : 
                  'Loading...'}
              </div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-green-400 mb-2">
                {marketData.indicators ? marketData.indicators.adx?.toFixed(1) : 'Loading...'}
              </div>
              <div className="text-white font-semibold text-lg">ADX</div>
              <div className="text-gray-400 text-sm">Trend Strength</div>
              <div className="text-green-200 text-sm mt-1">
                {marketData.indicators ? 
                  (marketData.indicators.adx > 40 ? 'Strong Trend' : 
                   marketData.indicators.adx > 25 ? 'Moderate Trend' : 'Weak Trend') : 
                  'Loading...'}
              </div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-purple-400 mb-2">
                {marketData.indicators ? formatPrice(marketData.indicators.atr) : 'Loading...'}
              </div>
              <div className="text-white font-semibold text-lg">ATR</div>
              <div className="text-gray-400 text-sm">Average True Range</div>
              <div className="text-purple-200 text-sm mt-1">Volatility Measure</div>
            </div>
          </div>
        </div>

        {/* Risk Management */}
        <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20">
          <h3 className="text-xl font-semibold text-white mb-6 flex items-center">
            <span className="mr-2">🛡️</span>
            Risk Management
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="text-2xl font-bold text-green-400 mb-2">
                {marketData.risk ? marketData.risk.position_size?.toFixed(6) : 'Loading...'}
              </div>
              <div className="text-white font-semibold">Position Size</div>
              <div className="text-gray-400 text-sm">Recommended BTC</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-red-400 mb-2">
                {marketData.risk ? formatPrice(marketData.risk.stop_loss) : 'Loading...'}
              </div>
              <div className="text-white font-semibold">Stop Loss</div>
              <div className="text-gray-400 text-sm">Risk Limit</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-400 mb-2">
                {marketData.risk ? formatPrice(marketData.risk.take_profit) : 'Loading...'}
              </div>
              <div className="text-white font-semibold">Take Profit</div>
              <div className="text-gray-400 text-sm">Target Price</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-yellow-400 mb-2">
                {marketData.risk ? `${marketData.risk.risk_reward_ratio}:1` : 'Loading...'}
              </div>
              <div className="text-white font-semibold">Risk/Reward</div>
              <div className="text-gray-400 text-sm">Ratio</div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-black/30 backdrop-blur-md border-t border-white/10 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex justify-between items-center">
            <div className="text-gray-400 text-sm">
              Last Update: {marketData.lastUpdate ? formatTimestamp(marketData.lastUpdate) : 'N/A'}
            </div>
            <div className="flex items-center space-x-4 text-sm text-gray-400">
              <span>🔗 Coinbase API</span>
              <span>📊 FinBERT Analysis</span>
              <span>⚡ WebSocket Live</span>
              <span>🛡️ Risk Management</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Dashboard;