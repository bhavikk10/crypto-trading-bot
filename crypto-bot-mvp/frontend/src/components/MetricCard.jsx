import React from 'react';

const MetricCard = ({ title, value, change, changeType, icon, loading, subtitle }) => {
  if (loading) {
    return (
      <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20 animate-pulse">
        <div className="flex items-center justify-between mb-4">
          <div className="w-8 h-8 bg-gray-400 rounded"></div>
          <div className="w-16 h-4 bg-gray-400 rounded"></div>
        </div>
        <div className="w-24 h-6 bg-gray-400 rounded mb-2"></div>
        <div className="w-32 h-8 bg-gray-400 rounded mb-2"></div>
        <div className="w-20 h-4 bg-gray-400 rounded"></div>
      </div>
    );
  }

  const getChangeColor = () => {
    switch (changeType) {
      case 'positive':
        return 'text-green-400';
      case 'negative':
        return 'text-red-400';
      default:
        return 'text-blue-400';
    }
  };

  return (
    <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all duration-300 hover:scale-105">
      <div className="flex items-center justify-between mb-4">
        <div className="text-3xl">{icon}</div>
        <div className={`text-sm font-semibold ${getChangeColor()}`}>
          {changeType === 'positive' ? 'UP' : changeType === 'negative' ? 'DOWN' : 'NEUTRAL'}
        </div>
      </div>
      <h3 className="text-white font-semibold text-lg mb-2">{title}</h3>
      <div className="text-3xl font-bold text-white mb-2">{value}</div>
      {change && (
        <div className={`text-sm font-semibold ${getChangeColor()}`}>
          {change}
        </div>
      )}
      {subtitle && (
        <div className="text-gray-300 text-sm mt-1">{subtitle}</div>
      )}
    </div>
  );
};

export default MetricCard;