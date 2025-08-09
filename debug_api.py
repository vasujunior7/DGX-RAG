#!/usr/bin/env python3
"""
Debug script to test the API with minimal requests
"""

import requests
import json

# Test configuration
API_BASE_URL = "http://localhost:8000"
API_ENDPOINT = f"{API_BASE_URL}/api/v2/hackrx/run"

# Simple test data - using a more substantial PDF for testing
TEST_REQUEST = {
    "documents": "https://arxiv.org/pdf/1706.03762.pdf",  # Attention is All You Need paper
    "questions": ["What is the main contribution of this paper?", "What is the Transformer architecture?"]
}

def test_single_request():
    """Test a single request to debug the issue"""
    print("🔧 DEBUG: Testing single API request")
    print(f"🎯 Endpoint: {API_ENDPOINT}")
    print(f"📄 Request: {json.dumps(TEST_REQUEST, indent=2)}")
    
    try:
        response = requests.post(API_ENDPOINT, json=TEST_REQUEST, timeout=60)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ ERROR: {response.text}")
            
    except Exception as e:
        print(f"💥 EXCEPTION: {e}")

if __name__ == "__main__":
    test_single_request() 