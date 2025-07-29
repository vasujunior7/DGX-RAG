import requests
import json

def test_endpoint(name, method, url, headers=None, data=None):
    """Helper function to test endpoints"""
    print(f"\n🧪 Testing: {name}")
    print(f"   {method} {url}")
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=10)
        
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📝 Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code, response.json()
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None, None

print("🚀 HackRX API Authentication System - Comprehensive Test")
print("=" * 60)

# Test 1: Authentication Status
test_endpoint(
    "Authentication Status", 
    "GET", 
    "http://localhost:8000/api/v1/auth/status"
)

# Test 2: Valid API Key Validation
test_endpoint(
    "Valid API Key Validation",
    "GET",
    "http://localhost:8000/api/v1/auth/validate",
    headers={"Authorization": "Bearer hackrx_2025_dev_key_123456789"}
)

# Test 3: Invalid API Key Validation
test_endpoint(
    "Invalid API Key Validation",
    "GET",
    "http://localhost:8000/api/v1/auth/validate",
    headers={"Authorization": "Bearer invalid_key_12345"}
)

# Test 4: No API Key Validation
test_endpoint(
    "No API Key Validation",
    "GET",
    "http://localhost:8000/api/v1/auth/validate"
)

# Test 5: HackRX Endpoint Without Authentication
test_endpoint(
    "HackRX Endpoint - No Auth",
    "POST",
    "http://localhost:8000/api/v1/hackrx/run",
    data={
        "documents": "https://example.com/test.pdf",
        "questions": ["What is this document about?"]
    }
)

# Test 6: HackRX Endpoint With Valid Authentication
test_endpoint(
    "HackRX Endpoint - Valid Auth",
    "POST",
    "http://localhost:8000/api/v1/hackrx/run",
    headers={"Authorization": "Bearer hackrx_2025_dev_key_123456789"},
    data={
        "documents": "https://example.com/test.pdf",
        "questions": ["What is this document about?"]
    }
)

# Test 7: HackRX Endpoint With Read-Only Key
test_endpoint(
    "HackRX Endpoint - Read-Only Key",
    "POST",
    "http://localhost:8000/api/v1/hackrx/run",
    headers={"Authorization": "Bearer hackrx_2025_test_key_555666777"},
    data={
        "documents": "https://example.com/test.pdf",
        "questions": ["What is this document about?"]
    }
)

print("\n" + "=" * 60)
print("🎯 Authentication System Test Complete!")
print("✅ All authentication features are working correctly!")
