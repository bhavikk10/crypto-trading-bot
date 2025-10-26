import React from 'react';
import { useWebSocket } from '../contexts/WebSocketContext';

const ConnectionStatus = () => {
  const { connectionStatus } = useWebSocket();

  const getStatusColor = () => {
    switch (connectionStatus) {
      case 'connected':
        return 'text-green-400 bg-green-500/20 border-green-500/30';
      case 'connecting':
        return 'text-yellow-400 bg-yellow-500/20 border-yellow-500/30';
      case 'error':
        return 'text-red-400 bg-red-500/20 border-red-500/30';
      default:
        return 'text-gray-400 bg-gray-500/20 border-gray-500/30';
    }
  };

  const getStatusIcon = () => {
    switch (connectionStatus) {
      case 'connected':
        return '🟢';
      case 'connecting':
        return '🟡';
      case 'error':
        return '🔴';
      default:
        return '⚪';
    }
  };

  const getStatusText = () => {
    switch (connectionStatus) {
      case 'connected':
        return 'Connected';
      case 'connecting':
        return 'Connecting...';
      case 'error':
        return 'Connection Error';
      default:
        return 'Disconnected';
    }
  };

  return (
    <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold border ${getStatusColor()}`}>
      <span className="mr-2">{getStatusIcon()}</span>
      {getStatusText()}
    </div>
  );
};

export default ConnectionStatus;