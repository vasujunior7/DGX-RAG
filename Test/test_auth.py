import requests
import json

# Test 1: Check authentication status
print("=== Testing Authentication Status ===")
try:
    response = requests.get("http://localhost:8000/api/v1/auth/status")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

print("\n=== Testing API without Authentication ===")
# Test 2: Try to access protected endpoint without API key
try:
    test_data = {
        "documents": "https://example.com/test.pdf",
        "questions": ["What is this about?"]
    }
    response = requests.post("http://localhost:8000/api/v1/hackrx/run", json=test_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

print("\n=== Testing API with Valid Authentication ===")
# Test 3: Try to access protected endpoint with valid API key
try:
    headers = {
        "Authorization": "Bearer hackrx_2025_dev_key_123456789",
        "Content-Type": "application/json"
    }
    test_data = {
        "documents": "https://example.com/test.pdf",
        "questions": ["What is this about?"]
    }
    response = requests.post("http://localhost:8000/api/v1/hackrx/run", json=test_data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

print("\n=== Testing API Key Validation ===")
# Test 4: Validate API key
try:
    headers = {
        "Authorization": "Bearer hackrx_2025_dev_key_123456789"
    }
    response = requests.get("http://localhost:8000/api/v1/auth/validate", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

print("\n=== Testing Invalid API Key ===")
# Test 5: Try with invalid API key
try:
    headers = {
        "Authorization": "Bearer invalid_key_12345"
    }
    response = requests.get("http://localhost:8000/api/v1/auth/validate", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
