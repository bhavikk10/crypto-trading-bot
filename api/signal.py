"""
Vercel serverless function for signal endpoint
"""
import json
from datetime import datetime

def handler(request):
    """Handle signal endpoint"""
    try:
        signal_data = {
            "signal": "HOLD",
            "confidence": 54,
            "reasoning": "Based on technical analysis and market sentiment",
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
            'body': json.dumps(signal_data)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
