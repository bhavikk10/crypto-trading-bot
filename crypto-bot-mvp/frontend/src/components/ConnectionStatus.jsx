import React from 'react';
import { useWebSocket } from '../contexts';

const ConnectionStatus = () => {
  const { connectionStatus, reconnectAttempts, maxReconnectAttempts } = useWebSocket();

  const getStatusInfo = () => {
    switch (connectionStatus) {
      case 'connected':
        return {
          text: 'Connected',
          className: 'status-connected',
          icon: '🟢'
        };
      case 'connecting':
        return {
          text: 'Connecting...',
          className: 'status-connecting',
          icon: '🟡'
        };
      case 'disconnected':
        return {
          text: 'Disconnected',
          className: 'status-disconnected',
          icon: '🔴'
        };
      case 'error':
        return {
          text: 'Connection Error',
          className: 'status-disconnected',
          icon: '🔴'
        };
      default:
        return {
          text: 'Unknown',
          className: 'status-disconnected',
          icon: '⚪'
        };
    }
  };

  const statusInfo = getStatusInfo();

  return (
    <div className="flex items-center space-x-2">
      <span className="text-lg">{statusInfo.icon}</span>
      <span className={`status-indicator ${statusInfo.className}`}>
        {statusInfo.text}
      </span>
      {connectionStatus === 'disconnected' && reconnectAttempts > 0 && (
        <span className="text-xs text-gray-500">
          ({reconnectAttempts}/{maxReconnectAttempts})
        </span>
      )}
    </div>
  );
};

export default ConnectionStatus;
