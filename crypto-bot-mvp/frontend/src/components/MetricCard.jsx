import React from 'react';

const MetricCard = ({ 
  title, 
  value, 
  subtitle, 
  change, 
  changePercentage, 
  direction, 
  icon, 
  loading = false 
}) => {
  const getChangeColor = (direction) => {
    switch (direction) {
      case 'positive':
        return 'text-success-600';
      case 'negative':
        return 'text-danger-600';
      default:
        return 'text-gray-600';
    }
  };

  const getChangeIcon = (direction) => {
    switch (direction) {
      case 'positive':
        return '↗';
      case 'negative':
        return '↘';
      default:
        return '→';
    }
  };

  if (loading) {
    return (
      <div className="metric-card">
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <h3 className="metric-label">{title}</h3>
            <div className="mt-2">
              <div className="h-6 bg-gray-200 rounded animate-pulse"></div>
              {subtitle && (
                <div className="h-4 bg-gray-200 rounded animate-pulse mt-2"></div>
              )}
            </div>
          </div>
          <div className="text-3xl text-gray-300">{icon}</div>
        </div>
      </div>
    );
  }

  return (
    <div className="metric-card">
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <h3 className="metric-label">{title}</h3>
          <p className="metric-value mt-2">{value}</p>
          {subtitle && (
            <p className="text-sm text-gray-600 mt-1">{subtitle}</p>
          )}
          {change !== undefined && changePercentage !== undefined && (
            <div className="flex items-center mt-2">
              <span className={`metric-change ${direction}`}>
                {getChangeIcon(direction)} {changePercentage.toFixed(2)}%
              </span>
            </div>
          )}
        </div>
        <div className="text-3xl">{icon}</div>
      </div>
    </div>
  );
};

export default MetricCard;
