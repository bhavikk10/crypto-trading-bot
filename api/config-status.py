"""
Vercel serverless function for config status endpoint
"""
import json
import os
from datetime import datetime

def handler(request):
    """Handle config status endpoint"""
    try:
        config_data = {
            "configuration": {
                "coinbase_configured": bool(os.getenv('COINBASE_API_KEY')),
                "twilio_configured": bool(os.getenv('TWILIO_ACCOUNT_SID')),
                "redis_configured": bool(os.getenv('REDIS_URL'))
            },
            "message": "Check which API keys are configured",
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
            'body': json.dumps(config_data)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
