"""
Vercel serverless function for price endpoint
"""
import json
import asyncio
from datetime import datetime

def handler(request):
    """Handle price endpoint"""
    try:
        # Mock price data for Vercel deployment
        price_data = {
            "symbol": "BTC-USD",
            "price": 45599 + (hash(str(datetime.now())) % 1000),
            "timestamp": datetime.now().isoformat(),
            "source": "vercel-mock"
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(price_data)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
