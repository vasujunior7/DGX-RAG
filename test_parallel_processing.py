#!/usr/bin/env python3
"""
Test script for parallel processing in HackRX API v2
Sends multiple concurrent requests to verify parallel execution
"""

import asyncio
import aiohttp
import json
import time
from datetime import datetime
import sys

# Test configuration
API_BASE_URL = "http://localhost:8000"  # Adjust if your server runs on different port
API_ENDPOINT = f"{API_BASE_URL}/api/v2/hackrx/run"
AUTH_STATUS_ENDPOINT = f"{API_BASE_URL}/api/v2/auth/status"

# Test data - using a real PDF URL for testing
TEST_REQUEST = {
    "documents": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",  # Simple test PDF
    "questions": [
        "What is this document about?",
        "What are the main contents?",
        "Can you describe what you found?"
    ]
}

async def send_request(session, request_id):
    """Send a single request and measure response time"""
    start_time = time.time()
    print(f"🚀 Request {request_id}: Starting at {datetime.now().strftime('%H:%M:%S.%f')[:-3]}")
    
    try:
        async with session.post(API_ENDPOINT, json=TEST_REQUEST) as response:
            end_time = time.time()
            duration = end_time - start_time
            
            if response.status == 200:
                result = await response.json()
                print(f"✅ Request {request_id}: SUCCESS in {duration:.2f}s - Got {len(result.get('answers', []))} answers")
                return {
                    "request_id": request_id,
                    "status": "success",
                    "duration": duration,
                    "answers_count": len(result.get('answers', []))
                }
            else:
                error_text = await response.text()
                print(f"❌ Request {request_id}: FAILED with status {response.status} in {duration:.2f}s")
                print(f"   Error: {error_text}")
                return {
                    "request_id": request_id,
                    "status": "failed",
                    "duration": duration,
                    "error": f"HTTP {response.status}: {error_text}"
                }
                
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        print(f"💥 Request {request_id}: EXCEPTION in {duration:.2f}s - {str(e)}")
        return {
            "request_id": request_id,
            "status": "exception",
            "duration": duration,
            "error": str(e)
        }

async def check_auth_status():
    """Check if authentication is enabled"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(AUTH_STATUS_ENDPOINT) as response:
                if response.status == 200:
                    auth_info = await response.json()
                    print(f"🔐 Auth Status: {json.dumps(auth_info, indent=2)}")
                    return auth_info
                else:
                    print(f"❌ Could not check auth status: HTTP {response.status}")
                    return None
    except Exception as e:
        print(f"💥 Error checking auth status: {e}")
        return None

async def test_parallel_processing(num_requests=5):
    """Test parallel processing with multiple concurrent requests"""
    print(f"\n🧪 PARALLEL PROCESSING TEST")
    print(f"=" * 50)
    print(f"📊 Sending {num_requests} concurrent requests...")
    print(f"🎯 Target endpoint: {API_ENDPOINT}")
    print(f"⏰ Test started at: {datetime.now().strftime('%H:%M:%S')}")
    
    # Check auth status first
    await check_auth_status()
    
    # Create session with timeout
    timeout = aiohttp.ClientTimeout(total=300)  # 5 minute timeout
    
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # Send all requests concurrently
        start_time = time.time()
        tasks = [send_request(session, i+1) for i in range(num_requests)]
        
        print(f"\n🏃‍♂️ All {num_requests} requests launched simultaneously!")
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        total_time = time.time() - start_time
        
        # Analyze results
        print(f"\n📈 RESULTS SUMMARY")
        print(f"=" * 30)
        print(f"⏱️  Total test duration: {total_time:.2f} seconds")
        
        successful = [r for r in results if isinstance(r, dict) and r.get('status') == 'success']
        failed = [r for r in results if isinstance(r, dict) and r.get('status') != 'success']
        exceptions = [r for r in results if not isinstance(r, dict)]
        
        print(f"✅ Successful requests: {len(successful)}/{num_requests}")
        print(f"❌ Failed requests: {len(failed)}")
        print(f"💥 Exceptions: {len(exceptions)}")
        
        if successful:
            durations = [r['duration'] for r in successful]
            avg_duration = sum(durations) / len(durations)
            min_duration = min(durations)
            max_duration = max(durations)
            
            print(f"📊 Response times:")
            print(f"   • Average: {avg_duration:.2f}s")
            print(f"   • Fastest: {min_duration:.2f}s")
            print(f"   • Slowest: {max_duration:.2f}s")
            
            # Check if parallel processing worked
            if max_duration < total_time * 0.8:  # If max individual time is much less than total time
                print(f"🎉 PARALLEL PROCESSING CONFIRMED! Requests processed concurrently.")
            else:
                print(f"⚠️  Requests may have been processed sequentially.")
        
        if failed:
            print(f"\n❌ FAILED REQUESTS:")
            for r in failed:
                print(f"   • Request {r['request_id']}: {r.get('error', 'Unknown error')}")
        
        if exceptions:
            print(f"\n💥 EXCEPTIONS:")
            for i, exc in enumerate(exceptions):
                print(f"   • Exception {i+1}: {exc}")
        
        return {
            "total_requests": num_requests,
            "successful": len(successful),
            "failed": len(failed),
            "exceptions": len(exceptions),
            "total_time": total_time,
            "avg_response_time": sum([r['duration'] for r in successful]) / len(successful) if successful else 0
        }

async def test_single_request():
    """Test a single request first"""
    print(f"\n🔧 SINGLE REQUEST TEST")
    print(f"=" * 30)
    
    async with aiohttp.ClientSession() as session:
        result = await send_request(session, 1)
        return result

def main():
    """Main test function"""
    print(f"🧪 HackRX API v2 Parallel Processing Test")
    print(f"=" * 60)
    
    if len(sys.argv) > 1:
        try:
            num_requests = int(sys.argv[1])
        except ValueError:
            print(f"❌ Invalid number of requests: {sys.argv[1]}")
            num_requests = 5
    else:
        num_requests = 5
    
    try:
        # Test single request first
        print(f"🔍 Testing single request first...")
        single_result = asyncio.run(test_single_request())
        
        if single_result['status'] == 'success':
            print(f"✅ Single request successful, proceeding with parallel test...")
            
            # Test parallel processing
            results = asyncio.run(test_parallel_processing(num_requests))
            
            print(f"\n🎯 FINAL VERDICT:")
            if results['successful'] >= num_requests * 0.8:  # 80% success rate
                print(f"🎉 PARALLEL PROCESSING TEST PASSED!")
                print(f"   Successfully handled {results['successful']}/{results['total_requests']} concurrent requests")
            else:
                print(f"⚠️  PARALLEL PROCESSING TEST NEEDS ATTENTION")
                print(f"   Only {results['successful']}/{results['total_requests']} requests succeeded")
        else:
            print(f"❌ Single request failed, check your API server:")
            print(f"   Error: {single_result.get('error', 'Unknown error')}")
            print(f"   Make sure the server is running on {API_BASE_URL}")
            
    except KeyboardInterrupt:
        print(f"\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n💥 Test failed with exception: {e}")

if __name__ == "__main__":
    main() 