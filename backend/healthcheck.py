#!/usr/bin/env python3
"""
Health check script for monitoring
Returns exit code 0 if healthy, 1 if unhealthy
"""
import sys
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def check_health():
    try:
        port = os.getenv('PORT', '8000')
        response = requests.get(f'http://localhost:{port}/system/health', timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') in ['healthy', 'degraded']:
                print(f"✅ Health check passed: {data.get('status')}")
                return 0
            else:
                print(f"❌ Health check failed: {data.get('status')}")
                return 1
        else:
            print(f"❌ Health check failed: HTTP {response.status_code}")
            return 1
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed: {str(e)}")
        return 1
    except Exception as e:
        print(f"❌ Health check failed: {str(e)}")
        return 1

if __name__ == '__main__':
    sys.exit(check_health())
