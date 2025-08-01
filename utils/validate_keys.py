#!/usr/bin/env python3
"""
API Key Validation Utility for HackRX
=====================================

This script validates all loaded API keys and tests their connectivity.
Run this script to ensure your environment is properly configured.

Usage:
    python utils/validate_keys.py
    python utils/validate_keys.py --verbose
    python utils/validate_keys.py --test-llm
"""

import os
import sys
import argparse
import requests
import json
from typing import Dict, List, Optional, Tuple
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.load_env import api_key_manager

class APIKeyValidator:
    """Validate and test API keys"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.results = {}
        
    def log(self, message: str, level: str = "INFO"):
        """Log message if verbose mode is enabled"""
        if self.verbose or level == "ERROR":
            prefix = {
                "INFO": "ℹ️",
                "SUCCESS": "✅", 
                "WARNING": "⚠️",
                "ERROR": "❌"
            }.get(level, "ℹ️")
            print(f"{prefix} {message}")
    
    def validate_openai_key(self, api_key: str) -> Tuple[bool, str]:
        """Validate OpenAI API key"""
        if not api_key:
            return False, "API key not provided"
        
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            response = requests.get(
                "https://api.openai.com/v1/models",
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                return True, "Valid - API accessible"
            elif response.status_code == 401:
                return False, "Invalid API key"
            else:
                return False, f"HTTP {response.status_code}"
        except Exception as e:
            return False, f"Connection error: {str(e)}"
    
    def validate_anthropic_key(self, api_key: str) -> Tuple[bool, str]:
        """Validate Anthropic API key"""
        if not api_key:
            return False, "API key not provided"
        
        try:
            headers = {
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01"
            }
            # Test with a minimal request
            data = {
                "model": "claude-3-haiku-20240307",
                "max_tokens": 1,
                "messages": [{"role": "user", "content": "Hi"}]
            }
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=data,
                timeout=10
            )
            if response.status_code == 200:
                return True, "Valid - API accessible"
            elif response.status_code == 401:
                return False, "Invalid API key"
            else:
                return False, f"HTTP {response.status_code}"
        except Exception as e:
            return False, f"Connection error: {str(e)}"
    
    def validate_google_key(self, api_key: str) -> Tuple[bool, str]:
        """Validate Google AI API key"""
        if not api_key:
            return False, "API key not provided"
        
        try:
            url = f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return True, "Valid - API accessible"
            elif response.status_code == 400:
                return False, "Invalid API key"
            else:
                return False, f"HTTP {response.status_code}"
        except Exception as e:
            return False, f"Connection error: {str(e)}"
    
    def validate_groq_key(self, api_key: str) -> Tuple[bool, str]:
        """Validate Groq API key"""
        if not api_key:
            return False, "API key not provided"
        
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            response = requests.get(
                "https://api.groq.com/openai/v1/models",
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                return True, "Valid - API accessible"
            elif response.status_code == 401:
                return False, "Invalid API key"
            else:
                return False, f"HTTP {response.status_code}"
        except Exception as e:
            return False, f"Connection error: {str(e)}"
    
    def validate_huggingface_key(self, api_key: str) -> Tuple[bool, str]:
        """Validate Hugging Face API key"""
        if not api_key:
            return False, "API key not provided"
        
        try:
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get(
                "https://huggingface.co/api/whoami",
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                return True, "Valid - API accessible"
            elif response.status_code == 401:
                return False, "Invalid API key"
            else:
                return False, f"HTTP {response.status_code}"
        except Exception as e:
            return False, f"Connection error: {str(e)}"
    
    def validate_basic_format(self, api_key: str, key_name: str) -> Tuple[bool, str]:
        """Basic validation for API key format"""
        if not api_key:
            return False, "API key not provided"
        
        # Basic checks
        if len(api_key) < 10:
            return False, "API key too short"
        
        if api_key.startswith('your_') or api_key.endswith('_here'):
            return False, "Placeholder value detected"
        
        return True, "Format appears valid"
    
    def validate_all_keys(self, test_connectivity: bool = False) -> Dict:
        """Validate all loaded API keys"""
        keys = api_key_manager.get_all_keys()
        
        # Define key validators
        validators = {
            'OPENAI_API_KEY': self.validate_openai_key if test_connectivity else self.validate_basic_format,
            'ANTHROPIC_API_KEY': self.validate_anthropic_key if test_connectivity else self.validate_basic_format,
            'GOOGLE_API_KEY': self.validate_google_key if test_connectivity else self.validate_basic_format,
            'GEMINI_API_KEY': self.validate_google_key if test_connectivity else self.validate_basic_format,
            'GROQ_API_KEY': self.validate_groq_key if test_connectivity else self.validate_basic_format,
            'HUGGINGFACE_API_KEY': self.validate_huggingface_key if test_connectivity else self.validate_basic_format,
        }
        
        results = {}
        
        self.log("\n🔍 Starting API Key Validation...")
        self.log("=" * 50)
        
        for key_name, key_value in keys.items():
            if key_value:  # Only validate non-empty keys
                self.log(f"Validating {key_name}...")
                
                if key_name in validators:
                    if test_connectivity:
                        is_valid, message = validators[key_name](key_value)
                    else:
                        is_valid, message = validators[key_name](key_value, key_name)
                else:
                    # Default validation for unknown keys
                    is_valid, message = self.validate_basic_format(key_value, key_name)
                
                results[key_name] = {
                    'valid': is_valid,
                    'message': message,
                    'masked_key': f"***{key_value[-4:]}" if len(key_value) > 4 else "***"
                }
                
                status = "✅" if is_valid else "❌"
                self.log(f"{status} {key_name}: {message}", 
                        "SUCCESS" if is_valid else "WARNING")
        
        return results
    
    def print_summary(self, results: Dict):
        """Print validation summary"""
        total_keys = len(results)
        valid_keys = sum(1 for r in results.values() if r['valid'])
        invalid_keys = total_keys - valid_keys
        
        print(f"\n📊 Validation Summary")
        print("=" * 30)
        print(f"Total Keys Tested: {total_keys}")
        print(f"✅ Valid Keys: {valid_keys}")
        print(f"❌ Invalid Keys: {invalid_keys}")
        print(f"Success Rate: {(valid_keys/total_keys)*100:.1f}%" if total_keys > 0 else "No keys to test")
        
        if invalid_keys > 0:
            print(f"\n⚠️ Issues Found:")
            for key_name, result in results.items():
                if not result['valid']:
                    print(f"  • {key_name}: {result['message']}")
        
        print(f"\n💡 Tip: Use --test-llm flag to test actual API connectivity")
    
    def generate_report(self, results: Dict, output_file: str = None):
        """Generate detailed validation report"""
        from datetime import datetime
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_keys": len(results),
            "valid_keys": sum(1 for r in results.values() if r['valid']),
            "results": results
        }
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
            self.log(f"Report saved to {output_file}")
        
        return report

def main():
    parser = argparse.ArgumentParser(description="Validate HackRX API Keys")
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="Enable verbose output")
    parser.add_argument("--test-llm", action="store_true", 
                       help="Test actual API connectivity (slower)")
    parser.add_argument("--output", "-o", type=str, 
                       help="Save report to JSON file")
    parser.add_argument("--summary", action="store_true",
                       help="Print key status summary")
    
    args = parser.parse_args()
    
    # Print key status if requested
    if args.summary:
        api_key_manager.print_key_status()
        return
    
    # Initialize validator
    validator = APIKeyValidator(verbose=args.verbose)
    
    # Validate keys
    results = validator.validate_all_keys(test_connectivity=args.test_llm)
    
    # Print summary
    validator.print_summary(results)
    
    # Save report if requested
    if args.output:
        validator.generate_report(results, args.output)

if __name__ == "__main__":
    main()
