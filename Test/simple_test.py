#!/usr/bin/env python3
"""
Simple API v2 Test Script
=========================

Quick and simple script to test the API v2 endpoint.
"""

import requests
import json
import time

def test_api_v2():
    """Simple test for API v2 endpoint"""
    
    # API endpoint
    url = "http://localhost:8000/api/v2/hackrx/run"
    
    # Request payload
    payload = {
        "documents": "http://localhost:8000/api/hostfile/download_pdf/515f4f14a724226a7fb15e44f7d8f32c.pdf",
        "questions": [
            "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
            "What is the waiting period for pre-existing diseases (PED) to be covered?",
            "Does this policy cover maternity expenses, and what are the conditions?",
            "What is the waiting period for cataract surgery?",
            "Are the medical expenses for an organ donor covered under this policy?",
            "What is the No Claim Discount (NCD) offered in this policy?",
            "Is there a benefit for preventive health check-ups?",
            "How does the policy define a 'Hospital'?",
            "What is the extent of coverage for AYUSH treatments?",
            "Are there any sub-limits on room rent and ICU charges for Plan A?"
        ]
    }
    
    # API Key - using a random string as requested
    api_key = "hackrx_api_key_abc123xyz789_random_string_for_testing"
    
    # Headers
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    print("🚀 Testing HackRX API")
    print("=" * 30)
    print(f"📡 Endpoint: {url}")
    print(f"📄 Document: {payload['documents'][:80]}...")
    print(f"🔑 API Key: {api_key[:20]}...")
    
    total_questions = len(payload['questions'])
    print(f"❓ Questions: {total_questions}")
    print("")
    
    try:
        print("📤 Sending request...")
        start_time = time.time()
        
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=300  # 5 minutes timeout
        )
        
        end_time = time.time()
        response_time = round(end_time - start_time, 2)
        
        print(f"⏱️  Response time: {response_time}s")
        print(f"📊 Status code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Success!")
            
            try:
                result = response.json()
                
                if 'answers' in result:
                    answers = result['answers']
                    print(f"📝 Received {len(answers)} answers")
                    print("")
                    
                    # Show all answers
                    for i, answer in enumerate(answers, 1):
                        print(f"Answer {i}:")
                        if isinstance(answer, str):
                            print(f"  {answer}")
                        else:
                            print(f"  {json.dumps(answer, indent=2)}")
                        print("")
                else:
                    print("📋 Full response:")
                    print(json.dumps(result, indent=2))
                    
            except json.JSONDecodeError:
                print("⚠️  Response is not valid JSON:")
                print(response.text)
        
        elif response.status_code == 401:
            print("❌ Authentication error (401)")
            print("💡 You may need an API key")
            
        elif response.status_code == 422:
            print("❌ Validation error (422)")
            print("💡 Check your request format")
            try:
                error_details = response.json()
                print("📋 Error details:")
                print(json.dumps(error_details, indent=2))
            except:
                print(response.text)
                
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(response.text)
    
    except requests.exceptions.Timeout:
        print("⏰ Request timed out")
        
    except requests.exceptions.ConnectionError:
        print("🌐 Connection error - is the server running?")
        print("💡 Try: python main.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api_v2()
