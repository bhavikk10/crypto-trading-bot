"""
Vercel serverless function for sentiment endpoint
"""
import json
from datetime import datetime

def handler(request):
    """Handle sentiment endpoint"""
    try:
        sentiment_data = {
            "score": 54.7,
            "sentiment": "Neutral",
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
            'body': json.dumps(sentiment_data)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
