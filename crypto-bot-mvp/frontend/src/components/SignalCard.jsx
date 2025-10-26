import React from 'react';
import { useData } from '../contexts';

const SignalCard = () => {
  const { marketData } = useData();

  const getSignalStrength = (signal) => {
    switch (signal?.toLowerCase()) {
      case 'buy':
        return { color: 'text-green-400', bg: 'bg-green-500/20', border: 'border-green-500/30' };
      case 'sell':
        return { color: 'text-red-400', bg: 'bg-red-500/20', border: 'border-red-500/30' };
      default:
        return { color: 'text-yellow-400', bg: 'bg-yellow-500/20', border: 'border-yellow-500/30' };
    }
  };

  const getSignalIcon = (signal) => {
    switch (signal?.toLowerCase()) {
      case 'buy':
        return '📈';
      case 'sell':
        return '📉';
      default:
        return '⏸️';
    }
  };

  const signal = marketData?.signal;
  const signalStyle = getSignalStrength(signal?.signal);

  return (
    <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20">
      <h3 className="text-xl font-semibold text-white mb-6 flex items-center">
        <span className="mr-2">🎯</span>
        Trading Recommendations
      </h3>
      
      {signal ? (
        <div className="space-y-4">
          {/* Main Signal */}
          <div className={`${signalStyle.bg} ${signalStyle.border} border rounded-xl p-4`}>
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-3">
                <span className="text-2xl">{getSignalIcon(signal.signal)}</span>
                <span className={`text-2xl font-bold ${signalStyle.color}`}>
                  {signal.signal}
                </span>
              </div>
              <div className={`text-sm font-semibold ${signalStyle.color}`}>
                {signal.confidence}% confidence
              </div>
            </div>
            <div className="text-white text-sm">
              {signal.reasoning || 'Based on technical analysis and market sentiment'}
            </div>
          </div>

          {/* Additional Info */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-white/5 rounded-lg p-3">
              <div className="text-gray-400 text-xs uppercase tracking-wide">Signal Strength</div>
              <div className="text-white font-semibold">
                {signal.signal_strength || 'Moderate'}
              </div>
            </div>
            <div className="bg-white/5 rounded-lg p-3">
              <div className="text-gray-400 text-xs uppercase tracking-wide">Timeframe</div>
              <div className="text-white font-semibold">Short-term</div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex space-x-3">
            <button className="flex-1 bg-green-500/20 hover:bg-green-500/30 border border-green-500/30 text-green-400 py-2 px-4 rounded-lg font-semibold transition-all duration-300">
              Execute Trade
            </button>
            <button className="flex-1 bg-blue-500/20 hover:bg-blue-500/30 border border-blue-500/30 text-blue-400 py-2 px-4 rounded-lg font-semibold transition-all duration-300">
              View Details
            </button>
          </div>
        </div>
      ) : (
        <div className="text-center py-8">
          <div className="text-4xl mb-4">⏳</div>
          <div className="text-gray-400">Loading trading signals...</div>
        </div>
      )}
    </div>
  );
};

export default SignalCard;