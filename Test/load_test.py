#!/usr/bin/env python3
"""
Load Test Script for HackRX API v2
===================================

This script sends requests to the API v2 endpoint with document processing tasks.
It includes error handling, response parsing, and detailed logging.

Usage:
    python load_test.py
    python load_test.py --verbose
    python load_test.py --server http://localhost:8000
"""

import requests
import json
import time
import argparse
import sys
from typing import Dict, List, Any
from datetime import datetime

class HackRXAPIClient:
    """Client for interacting with HackRX API v2"""
    
    def __init__(self, base_url: str = "http://localhost:8000", api_key: str = None, timeout: int = 300):
        """
        Initialize the API client
        
        Args:
            base_url: Base URL of the API server
            api_key: API key for authentication (optional)
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'HackRX-LoadTest/1.0'
        })
        
        # Add API key if provided
        if self.api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}'
            })
    
    def send_v2_request(self, payload: Dict[str, Any], verbose: bool = False) -> Dict[str, Any]:
        """
        Send request to API v2 endpoint
        
        Args:
            payload: Request payload
            verbose: Enable verbose logging
            
        Returns:
            Response data from the API
        """
        url = f"{self.base_url}/api/v2/hackrx/run"
        
        if verbose:
            print(f"🚀 Sending request to: {url}")
            print(f"📤 Payload: {json.dumps(payload, indent=2)}")
        
        try:
            start_time = time.time()
            
            response = self.session.post(
                url,
                json=payload,
                timeout=self.timeout
            )
            
            end_time = time.time()
            response_time = round(end_time - start_time, 2)
            
            # Log response details
            if verbose:
                print(f"⏱️  Response Time: {response_time}s")
                print(f"📊 Status Code: {response.status_code}")
                print(f"📏 Response Size: {len(response.content)} bytes")
            
            # Handle different status codes
            if response.status_code == 200:
                try:
                    result = response.json()
                    if verbose:
                        print(f"✅ Success! Response: {json.dumps(result, indent=2)}")
                    return {
                        'success': True,
                        'status_code': response.status_code,
                        'response_time': response_time,
                        'data': result
                    }
                except json.JSONDecodeError as e:
                    print(f"❌ Failed to parse JSON response: {e}")
                    return {
                        'success': False,
                        'status_code': response.status_code,
                        'response_time': response_time,
                        'error': f"JSON decode error: {e}",
                        'raw_response': response.text
                    }
            
            elif response.status_code == 401:
                print(f"🔐 Authentication Error (401): Check your API key")
                return {
                    'success': False,
                    'status_code': response.status_code,
                    'response_time': response_time,
                    'error': 'Authentication failed - invalid or missing API key'
                }
            
            elif response.status_code == 422:
                print(f"📝 Validation Error (422): Check your request format")
                try:
                    error_detail = response.json()
                    if verbose:
                        print(f"📋 Error Details: {json.dumps(error_detail, indent=2)}")
                except:
                    pass
                return {
                    'success': False,
                    'status_code': response.status_code,
                    'response_time': response_time,
                    'error': 'Request validation failed',
                    'details': response.text
                }
            
            else:
                print(f"⚠️  Unexpected Status Code: {response.status_code}")
                return {
                    'success': False,
                    'status_code': response.status_code,
                    'response_time': response_time,
                    'error': f'HTTP {response.status_code}',
                    'details': response.text
                }
                
        except requests.exceptions.Timeout:
            print(f"⏰ Request timed out after {self.timeout} seconds")
            return {
                'success': False,
                'error': f'Request timeout after {self.timeout}s'
            }
        
        except requests.exceptions.ConnectionError as e:
            print(f"🌐 Connection Error: {e}")
            return {
                'success': False,
                'error': f'Connection error: {e}'
            }
        
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
            return {
                'success': False,
                'error': f'Unexpected error: {e}'
            }
    
    def test_server_health(self, verbose: bool = False) -> bool:
        """Test if the server is reachable"""
        try:
            url = f"{self.base_url}/health"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                if verbose:
                    print(f"✅ Server is healthy at {self.base_url}")
                return True
            else:
                if verbose:
                    print(f"⚠️  Server returned status {response.status_code}")
                return False
                
        except Exception as e:
            if verbose:
                print(f"❌ Server health check failed: {e}")
            return False

def create_test_payload() -> Dict[str, Any]:
    """Create the test payload for API v2"""
    return {
        "requests": [
            {
                "documents": "http://localhost:8000/api/hostfile/download_file/f15345ba5ce7155ebb1fc8f231da2654.pdf",
                "questions": [
                    "If my car is stolen, what case will it be in law?",
                    "If I am arrested without a warrant, is that legal?",
                    "If someone denies me a job because of my caste, is that allowed?",
                    "If the government takes my land for a project, can I stop it?",
                    "If my child is forced to work in a factory, is that legal?",
                    "If I am stopped from speaking at a protest, is that against my rights?",
                    "If a religious place stops me from entering because I'm a woman, is that constitutional?",
                    "If I change my religion, can the government stop me?",
                    "If the police torture someone in custody, what right is being violated?",
                    "If I'm denied admission to a public university because I'm from a backward community, can I do something?"
                ]
            },
            {
                "documents": "http://localhost:8000/api/hostfile/download_file/d6cf54e2e41ddc58c1eadbcdb3ea24ef.pdf",
                "questions": [
                    "I have raised a claim for hospitalization for Rs 200,000 with HDFC, and it's approved. My total expenses are Rs 250,000. Can I raise the remaining Rs 50,000 with you?"
                ]
            },
            {
                "documents": "http://localhost:8000/api/hostfile/download_file/515f4f14a724226a7fb15e44f7d8f32c.pdf",
                "questions": [
                    "When will my root canal claim of Rs 25,000 be settled?",
                    "I have done an IVF for Rs 56,000. Is it covered?",
                    "I did a cataract treatment of Rs 100,000. Will you settle the full Rs 100,000?",
                    "Give me a list of documents to be uploaded for hospitalization for heart surgery."
                ]
            },
            {
                "documents": "http://localhost:8000/api/hostfile/download_file/6635d94cf9023c83521982b3043ec70c.pdf",
                "questions": [
                    "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
                    "What is the waiting period for pre-existing diseases (PED) to be covered?",
                    "Does this policy cover maternity expenses, and what are the conditions?"
                ]
            }
        ]
    }

def print_summary(results: List[Dict[str, Any]]) -> None:
    """Print a summary of test results"""
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    total_tests = len(results)
    successful_tests = sum(1 for r in results if r.get('success', False))
    failed_tests = total_tests - successful_tests
    
    if total_tests > 0:
        success_rate = (successful_tests / total_tests) * 100
    else:
        success_rate = 0
    
    print(f"📈 Total Tests: {total_tests}")
    print(f"✅ Successful: {successful_tests}")
    print(f"❌ Failed: {failed_tests}")
    print(f"📊 Success Rate: {success_rate:.1f}%")
    
    # Calculate average response time for successful requests
    successful_times = [r.get('response_time', 0) for r in results if r.get('success', False)]
    if successful_times:
        avg_time = sum(successful_times) / len(successful_times)
        print(f"⏱️  Average Response Time: {avg_time:.2f}s")
        print(f"⚡ Fastest Response: {min(successful_times):.2f}s")
        print(f"🐌 Slowest Response: {max(successful_times):.2f}s")
    
    # Show errors if any
    if failed_tests > 0:
        print(f"\n❌ ERRORS:")
        for i, result in enumerate(results):
            if not result.get('success', False):
                print(f"   Test {i+1}: {result.get('error', 'Unknown error')}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="HackRX API v2 Load Test")
    parser.add_argument("--server", "-s", default="http://localhost:8000", 
                       help="Server URL (default: http://localhost:8000)")
    parser.add_argument("--api-key", "-k", help="API key for authentication")
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="Enable verbose output")
    parser.add_argument("--timeout", "-t", type=int, default=300,
                       help="Request timeout in seconds (default: 300)")
    parser.add_argument("--repeat", "-r", type=int, default=1,
                       help="Number of times to repeat the test (default: 1)")
    
    args = parser.parse_args()
    
    print("🚀 HackRX API v2 Load Test")
    print("=" * 40)
    print(f"🌐 Server: {args.server}")
    print(f"🔑 API Key: {'Provided' if args.api_key else 'Not provided'}")
    print(f"⏱️  Timeout: {args.timeout}s")
    print(f"🔁 Repeats: {args.repeat}")
    print("")
    
    # Initialize client
    client = HackRXAPIClient(
        base_url=args.server,
        api_key=args.api_key,
        timeout=args.timeout
    )
    
    # Test server health
    print("🏥 Testing server health...")
    if not client.test_server_health(verbose=args.verbose):
        print("❌ Server health check failed. Please ensure the server is running.")
        print(f"💡 Try: python main.py (to start the server)")
        sys.exit(1)
    
    print("✅ Server is healthy!")
    print("")
    
    # Create test payload
    payload = create_test_payload()
    
    # Show payload summary
    total_questions = sum(len(req['questions']) for req in payload['requests'])
    print(f"📋 Test Payload Summary:")
    print(f"   📄 Documents: {len(payload['requests'])}")
    print(f"   ❓ Total Questions: {total_questions}")
    print("")
    
    # Run tests
    results = []
    
    for i in range(args.repeat):
        if args.repeat > 1:
            print(f"🔄 Running test {i+1}/{args.repeat}")
        
        print("📤 Sending request to API v2...")
        result = client.send_v2_request(payload, verbose=args.verbose)
        results.append(result)
        
        if result['success']:
            print("✅ Request completed successfully!")
            
            # Show response summary if available
            if 'data' in result and isinstance(result['data'], dict):
                data = result['data']
                if 'answers' in data:
                    answers = data['answers']
                    print(f"📝 Received {len(answers)} answers")
                    
                    if not args.verbose:
                        # Show first few answers as preview
                        preview_count = min(3, len(answers))
                        for j in range(preview_count):
                            answer = answers[j]
                            if isinstance(answer, str):
                                preview = answer[:100] + "..." if len(answer) > 100 else answer
                                print(f"   Answer {j+1}: {preview}")
                        
                        if len(answers) > preview_count:
                            print(f"   ... and {len(answers) - preview_count} more answers")
        else:
            print(f"❌ Request failed: {result.get('error', 'Unknown error')}")
        
        # Wait between repeats
        if i < args.repeat - 1:
            print("⏳ Waiting 2 seconds before next test...")
            time.sleep(2)
            print("")
    
    # Print summary
    print_summary(results)
    
    # Save results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"load_test_results_{timestamp}.json"
    
    try:
        with open(filename, 'w') as f:
            json.dump({
                'timestamp': timestamp,
                'config': {
                    'server': args.server,
                    'timeout': args.timeout,
                    'repeats': args.repeat,
                    'api_key_provided': bool(args.api_key)
                },
                'payload': payload,
                'results': results
            }, f, indent=2)
        
        print(f"\n💾 Results saved to: {filename}")
    except Exception as e:
        print(f"⚠️  Could not save results to file: {e}")
    
    # Exit with appropriate code
    success_count = sum(1 for r in results if r.get('success', False))
    if success_count == len(results):
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print(f"\n⚠️  {len(results) - success_count} test(s) failed")
        sys.exit(1)

if __name__ == "__main__":
    main()