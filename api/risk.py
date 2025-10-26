"""
Vercel serverless function for risk endpoint
"""
import json
from datetime import datetime

def handler(request):
    """Handle risk endpoint"""
    try:
        risk_data = {
            "position_size": 0.001,
            "stop_loss": 42012,
            "take_profit": 48646,
            "risk_reward_ratio": 2.0,
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
            'body': json.dumps(risk_data)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
