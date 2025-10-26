"""
Simple API Keys Setup for Crypto Trading Bot Dashboard
"""

import os

def main():
    print("Crypto Trading Bot Dashboard - API Keys Setup")
    print("=" * 50)
    print()
    
    # Check if .env exists
    env_path = "../.env"
    if os.path.exists(env_path):
        print(f"Found existing .env file at {env_path}")
        print()
        print("To add your API keys, edit the .env file and replace:")
        print("  your_coinbase_api_key_here -> your actual Coinbase API key")
        print("  your_coinbase_api_secret_here -> your actual Coinbase secret")
        print("  your_coinbase_passphrase_here -> your actual Coinbase passphrase")
        print()
        print("REQUIRED for real data:")
        print("  - Coinbase API Key, Secret, Passphrase")
        print()
        print("OPTIONAL for enhanced features:")
        print("  - LunarCrash API Key (sentiment)")
        print("  - MarketSai API Key (sentiment)")
        print("  - Twilio SID, Token, Phone (SMS alerts)")
        print()
        print("After editing .env, restart the backend:")
        print("  uvicorn main:app --reload")
        print()
        print("Check configuration status at:")
        print("  http://localhost:8000/config-status")
    else:
        print(f"No .env file found at {env_path}")
        print("Please copy env.template to .env first")

if __name__ == "__main__":
    main()