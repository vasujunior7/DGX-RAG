import requests
import time

# Wait a moment for server to fully start
time.sleep(2)

print("Testing Authentication System...")
print("=" * 50)

# Test authentication status
try:
    response = requests.get("http://localhost:8000/api/v1/auth/status", timeout=10)
    print(f"✅ Auth Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"❌ Auth Status Error: {e}")

# Test with valid API key
try:
    headers = {"Authorization": "Bearer hackrx_2025_dev_key_123456789"}
    response = requests.get("http://localhost:8000/api/v1/auth/validate", headers=headers, timeout=10)
    print(f"✅ Valid Key Test: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"❌ Valid Key Error: {e}")

print("=" * 50)
print("Authentication system verification complete!")
