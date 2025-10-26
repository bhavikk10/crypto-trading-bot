"""
Vercel serverless function for indicators endpoint
"""
import json
from datetime import datetime

def handler(request):
    """Handle indicators endpoint"""
    try:
        indicators_data = {
            "rsi": 50.0,
            "adx": 25.0,
            "atr": 0,
            "macd": 0.12,
            "timestamp": datetime.now().isoformat()
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(indicators_data)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
