import React from 'react';
import { useWebSocket, useData } from '../contexts';
import Chart from './Chart';
import SignalCard from './SignalCard';
import MetricCard from './MetricCard';
import ConnectionStatus from './ConnectionStatus';

const Dashboard = () => {
  const { connectionStatus } = useWebSocket();
  const { marketData, getPriceChange, formatPrice, formatPercentage, formatTimestamp } = useData();

  const priceChange = getPriceChange();

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">
                🚀 Crypto Bot MVP
              </h1>
              <span className="ml-3 px-2 py-1 text-xs font-medium bg-primary-100 text-primary-800 rounded-full">
                Live Trading Dashboard
              </span>
            </div>
            <ConnectionStatus />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Top Metrics Row */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* Price Card */}
          <MetricCard
            title="BTC/USD Price"
            value={marketData.price ? formatPrice(marketData.price.price) : 'Loading...'}
            change={priceChange.change}
            changePercentage={priceChange.percentage}
            direction={priceChange.direction}
            icon="💰"
            loading={!marketData.price}
          />

          {/* RSI Card */}
          <MetricCard
            title="RSI"
            value={marketData.indicators ? `${marketData.indicators.rsi?.toFixed(1)}` : 'Loading...'}
            subtitle={marketData.indicators ? 
              (marketData.indicators.rsi < 30 ? 'Oversold' : 
               marketData.indicators.rsi > 70 ? 'Overbought' : 'Neutral') : 
              'Loading...'}
            icon="📊"
            loading={!marketData.indicators}
          />

          {/* Sentiment Card */}
          <MetricCard
            title="Market Sentiment"
            value={marketData.sentiment ? `${marketData.sentiment.score?.toFixed(1)}` : 'Loading...'}
            subtitle={marketData.sentiment ? marketData.sentiment.sentiment : 'Loading...'}
            icon="😊"
            loading={!marketData.sentiment}
          />

          {/* Signal Card */}
          <MetricCard
            title="Trading Signal"
            value={marketData.signal ? marketData.signal.signal : 'Loading...'}
            subtitle={marketData.signal ? marketData.signal.signal_strength : 'Loading...'}
            icon="🎯"
            loading={!marketData.signal}
          />
        </div>

        {/* Chart and Signal Panel */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Chart Section */}
          <div className="lg:col-span-2">
            <div className="card">
              <div className="card-header">
                <h2 className="text-lg font-semibold text-gray-900">
                  Price Chart & Momentum
                </h2>
                <p className="text-sm text-gray-500 mt-1">
                  Real-time BTC/USD price with technical indicators
                </p>
              </div>
              <div className="card-body">
                <Chart />
              </div>
            </div>
          </div>

          {/* Signal Panel */}
          <div className="lg:col-span-1">
            <SignalCard />
          </div>
        </div>

        {/* Technical Indicators Row */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
          {/* ADX Card */}
          <div className="card">
            <div className="card-body">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide">
                    ADX (Trend Strength)
                  </h3>
                  <p className="text-2xl font-bold text-gray-900 mt-2">
                    {marketData.indicators ? marketData.indicators.adx?.toFixed(1) : 'Loading...'}
                  </p>
                  <p className="text-sm text-gray-600 mt-1">
                    {marketData.indicators ? 
                      (marketData.indicators.adx > 40 ? 'Strong Trend' : 
                       marketData.indicators.adx > 25 ? 'Moderate Trend' : 'Weak Trend') : 
                      'Loading...'}
                  </p>
                </div>
                <div className="text-3xl">📈</div>
              </div>
            </div>
          </div>

          {/* ATR Card */}
          <div className="card">
            <div className="card-body">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide">
                    ATR (Volatility)
                  </h3>
                  <p className="text-2xl font-bold text-gray-900 mt-2">
                    {marketData.indicators ? formatPrice(marketData.indicators.atr) : 'Loading...'}
                  </p>
                  <p className="text-sm text-gray-600 mt-1">
                    {marketData.indicators ? 'Average True Range' : 'Loading...'}
                  </p>
                </div>
                <div className="text-3xl">📊</div>
              </div>
            </div>
          </div>

          {/* Risk Management Card */}
          <div className="card">
            <div className="card-body">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide">
                    Position Size
                  </h3>
                  <p className="text-2xl font-bold text-gray-900 mt-2">
                    {marketData.risk ? marketData.risk.position_size?.toFixed(6) : 'Loading...'}
                  </p>
                  <p className="text-sm text-gray-600 mt-1">
                    {marketData.risk ? `Risk: ${marketData.risk.risk_percentage?.toFixed(2)}%` : 'Loading...'}
                  </p>
                </div>
                <div className="text-3xl">⚖️</div>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-12 py-8 border-t border-gray-200">
          <div className="flex justify-between items-center">
            <div className="text-sm text-gray-500">
              Last Update: {marketData.lastUpdate ? formatTimestamp(marketData.lastUpdate) : 'N/A'}
            </div>
            <div className="text-sm text-gray-500">
              Crypto Trading Bot Dashboard v1.0.0
            </div>
          </div>
        </footer>
      </main>
    </div>
  );
};

export default Dashboard;
