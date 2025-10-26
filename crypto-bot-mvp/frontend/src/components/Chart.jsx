import React from 'react';
import { useData } from '../contexts';

const Chart = () => {
  const { marketData } = useData();

  // Mock chart data for demonstration
  const chartData = [
    { time: '09:00', price: 45200 },
    { time: '10:00', price: 45450 },
    { time: '11:00', price: 45600 },
    { time: '12:00', price: 45500 },
    { time: '13:00', price: 45750 },
    { time: '14:00', price: 45599 },
  ];

  const currentPrice = marketData?.price?.price || 45599;
  const minPrice = Math.min(...chartData.map(d => d.price));
  const maxPrice = Math.max(...chartData.map(d => d.price));
  const priceRange = maxPrice - minPrice;

  return (
    <div className="space-y-4">
      {/* Price Display */}
      <div className="text-center">
        <div className="text-4xl font-bold text-white mb-2">
          ${currentPrice.toLocaleString()}
        </div>
        <div className="text-green-400 text-sm">
          Live Price • Updated just now
        </div>
      </div>

      {/* Simple Chart Visualization */}
      <div className="bg-white/5 rounded-xl p-4">
        <div className="h-48 relative">
          <svg width="100%" height="100%" className="absolute inset-0">
            {/* Grid lines */}
            {[0, 0.25, 0.5, 0.75, 1].map((ratio, i) => (
              <line
                key={i}
                x1="0"
                y1={ratio * 192}
                x2="100%"
                y2={ratio * 192}
                stroke="rgba(255,255,255,0.1)"
                strokeWidth="1"
              />
            ))}
            
            {/* Price line */}
            <polyline
              points={chartData.map((point, i) => {
                const x = (i / (chartData.length - 1)) * 100;
                const y = ((maxPrice - point.price) / priceRange) * 192;
                return `${x}%,${y}`;
              }).join(' ')}
              fill="none"
              stroke="#10b981"
              strokeWidth="3"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            
            {/* Data points */}
            {chartData.map((point, i) => {
              const x = (i / (chartData.length - 1)) * 100;
              const y = ((maxPrice - point.price) / priceRange) * 192;
              return (
                <circle
                  key={i}
                  cx={`${x}%`}
                  cy={y}
                  r="4"
                  fill="#10b981"
                  className="hover:r-6 transition-all duration-300"
                />
              );
            })}
          </svg>
          
          {/* Price labels */}
          <div className="absolute right-0 top-0 text-xs text-gray-400">
            <div>${maxPrice.toLocaleString()}</div>
          </div>
          <div className="absolute right-0 bottom-0 text-xs text-gray-400">
            <div>${minPrice.toLocaleString()}</div>
          </div>
        </div>
        
        {/* Time labels */}
        <div className="flex justify-between mt-2 text-xs text-gray-400">
          {chartData.map((point, i) => (
            <span key={i}>{point.time}</span>
          ))}
        </div>
      </div>

      {/* Chart Info */}
      <div className="grid grid-cols-3 gap-4 text-center">
        <div className="bg-white/5 rounded-lg p-3">
          <div className="text-white font-semibold">24h High</div>
          <div className="text-green-400">${maxPrice.toLocaleString()}</div>
        </div>
        <div className="bg-white/5 rounded-lg p-3">
          <div className="text-white font-semibold">24h Low</div>
          <div className="text-red-400">${minPrice.toLocaleString()}</div>
        </div>
        <div className="bg-white/5 rounded-lg p-3">
          <div className="text-white font-semibold">Volume</div>
          <div className="text-blue-400">1.2B</div>
        </div>
      </div>
    </div>
  );
};

export default Chart;