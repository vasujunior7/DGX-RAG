"""
Authentication utilities for HackRX API
"""
import json
import os
from typing import Optional, Dict, List
from pathlib import Path

class AuthManager:
    def __init__(self, config_path: str = "Config/config.json", api_keys_path: str = "Config/api_keys.json"):
        self.config_path = Path(config_path)
        self.api_keys_path = Path(api_keys_path)
        self._load_config()
        self._load_api_keys()
    
    def _load_config(self):
        """Load configuration from config.json"""
        try:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            # Default configuration if file doesn't exist
            self.config = {
                "api_authentication": {
                    "enabled": True,
                    "require_api_key": True
                }
            }
    
    def _load_api_keys(self):
        """Load API keys from api_keys.json"""
        try:
            with open(self.api_keys_path, 'r') as f:
                data = json.load(f)
                self.api_keys = {key["key"]: key for key in data["api_keys"] if key["active"]}
        except FileNotFoundError:
            self.api_keys = {}
    
    def is_authentication_enabled(self) -> bool:
        """Check if API authentication is enabled"""
        return self.config.get("api_authentication", {}).get("enabled", True)
    
    def is_api_key_required(self) -> bool:
        """Check if API key is required"""
        return self.config.get("api_authentication", {}).get("require_api_key", True)
    
    def validate_api_key(self, api_key: str) -> Optional[Dict]:
        """Validate an API key and return key info if valid"""
        if not self.is_authentication_enabled():
            return {"valid": True, "bypass": True}
        
        if not self.is_api_key_required():
            return {"valid": True, "bypass": True}
        
        if not api_key:
            return None
        
        # Remove 'Bearer ' prefix if present
        if api_key.startswith('Bearer '):
            api_key = api_key[7:]
        
        key_info = self.api_keys.get(api_key)
        if key_info and key_info.get("active", False):
            return {
                "valid": True,
                "key": api_key,
                "name": key_info.get("name"),
                "permissions": key_info.get("permissions", [])
            }
        
        return None
    
    def has_permission(self, key_info: Dict, permission: str) -> bool:
        """Check if a validated key has specific permission"""
        if key_info.get("bypass"):
            return True
        
        permissions = key_info.get("permissions", [])
        return permission in permissions or "write" in permissions  # write implies read
    
    def reload_config(self):
        """Reload configuration and API keys"""
        self._load_config()
        self._load_api_keys()

# Global auth manager instance
auth_manager = AuthManager()
