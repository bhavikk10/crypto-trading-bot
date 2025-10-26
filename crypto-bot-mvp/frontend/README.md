# Crypto Trading Bot Dashboard - Frontend

This is the React frontend for the Crypto Trading Bot Dashboard MVP.

## Features

- Real-time WebSocket connection to backend
- Live price charts with Recharts
- Technical indicators display (RSI, ADX, ATR)
- Sentiment analysis visualization
- Trading signal recommendations
- Risk management controls
- Responsive design with Tailwind CSS

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

## Components

- **Dashboard**: Main dashboard layout
- **Chart**: Price chart with technical indicators
- **SignalCard**: Trading signal display
- **MetricCard**: Reusable metric display component
- **ConnectionStatus**: WebSocket connection indicator

## Contexts

- **WebSocketContext**: Manages WebSocket connection and real-time data
- **DataContext**: Handles market data state and formatting

## Styling

Uses Tailwind CSS with custom crypto-themed colors and components.

## Development

The app connects to the FastAPI backend running on `http://localhost:8000` and expects WebSocket data on `/stream` endpoint.
