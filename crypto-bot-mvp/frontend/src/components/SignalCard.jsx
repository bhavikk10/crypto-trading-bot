import React from 'react';
import { useData } from '../contexts';

const SignalCard = () => {
  const { marketData, getSignalStrength, formatTimestamp } = useData();

  const getSignalColor = (signal) => {
    if (!signal) return 'signal-hold';
    
    switch (signal.signal) {
      case 'BUY':
        return 'signal-buy';
      case 'SELL':
        return 'signal-sell';
      default:
        return 'signal-hold';
    }
  };

  const getSignalIcon = (signal) => {
    if (!signal) return '⏸️';
    
    switch (signal.signal) {
      case 'BUY':
        return '📈';
      case 'SELL':
        return '📉';
      default:
        return '⏸️';
    }
  };

  const getConfidenceColor = (confidence) => {
    if (!confidence) return 'text-gray-600';
    
    if (confidence >= 0.8) return 'text-success-600';
    if (confidence >= 0.6) return 'text-warning-600';
    return 'text-danger-600';
  };

  if (!marketData.signal) {
    return (
      <div className="card">
        <div className="card-header">
          <h2 className="text-lg font-semibold text-gray-900">
            Trading Signal
          </h2>
        </div>
        <div className="card-body">
          <div className="text-center py-8">
            <div className="loading-spinner mx-auto mb-4"></div>
            <p className="text-gray-500">Loading signal...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="card-header">
        <h2 className="text-lg font-semibold text-gray-900">
          Trading Signal
        </h2>
        <p className="text-sm text-gray-500 mt-1">
          AI-powered trading recommendations
        </p>
      </div>
      <div className="card-body">
        {/* Main Signal */}
        <div className={`p-4 rounded-lg border-2 ${getSignalColor(marketData.signal)} mb-6`}>
          <div className="flex items-center justify-between">
            <div>
              <div className="flex items-center">
                <span className="text-2xl mr-3">
                  {getSignalIcon(marketData.signal)}
                </span>
                <div>
                  <h3 className="text-xl font-bold">
                    {marketData.signal.signal}
                  </h3>
                  <p className="text-sm opacity-75">
                    {marketData.signal.signal_strength}
                  </p>
                </div>
              </div>
            </div>
            <div className="text-right">
              <p className={`text-sm font-medium ${getConfidenceColor(marketData.signal.confidence)}`}>
                {(marketData.signal.confidence * 100).toFixed(1)}% Confidence
              </p>
            </div>
          </div>
        </div>

        {/* Signal Details */}
        <div className="space-y-4">
          <div>
            <h4 className="text-sm font-medium text-gray-700 mb-2">Signal Breakdown</h4>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-gray-500">Momentum:</span>
                <span className="ml-2 font-medium">
                  {(marketData.signal.momentum_score * 100).toFixed(1)}%
                </span>
              </div>
              <div>
                <span className="text-gray-500">Sentiment:</span>
                <span className="ml-2 font-medium">
                  {(marketData.signal.sentiment_score * 100).toFixed(1)}%
                </span>
              </div>
            </div>
          </div>

          <div>
            <h4 className="text-sm font-medium text-gray-700 mb-2">Reasoning</h4>
            <p className="text-sm text-gray-600 bg-gray-50 p-3 rounded-lg">
              {marketData.signal.reasoning || 'No reasoning available'}
            </p>
          </div>

          {/* Risk Management Info */}
          {marketData.risk && (
            <div>
              <h4 className="text-sm font-medium text-gray-700 mb-2">Risk Management</h4>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-500">Stop Loss:</span>
                  <span className="font-medium">
                    ${marketData.risk.stop_loss?.toFixed(2)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Take Profit:</span>
                  <span className="font-medium">
                    ${marketData.risk.take_profit?.toFixed(2)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Risk/Reward:</span>
                  <span className="font-medium">
                    {marketData.risk.risk_reward_ratio?.toFixed(2)}:1
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* Timestamp */}
          <div className="pt-4 border-t border-gray-200">
            <p className="text-xs text-gray-500">
              Last Updated: {formatTimestamp(marketData.signal.timestamp)}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SignalCard;
