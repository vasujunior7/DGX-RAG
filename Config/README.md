# ⚙️ Configuration Management

This directory contains all configuration files for the HackRX API, supporting both V1 and V2 endpoints with enhanced security and flexibility.

## 📁 Files Structure

```
Config/
├── config.json         # Main application configuration
├── api_keys.json      # API key definitions and permissions
├── .env.example       # Environment variables template
├── logging.yaml       # Advanced logging configuration
└── README.md          # This documentation
```

## 🔧 Configuration Details

### config.json (Main Configuration)

Controls application behavior across all API versions:

```json
{
  "api_authentication": {
    "enabled": true, // Enable/disable authentication globally
    "require_api_key": true, // Require API key for protected endpoints
    "api_versions": {
      "v1": {
        "enabled": true,
        "rate_limit": "100/hour",
        "features": ["basic_processing"]
      },
      "v2": {
        "enabled": true,
        "rate_limit": "200/hour",
        "features": ["batch_processing", "metadata", "enhanced_responses"]
      }
    }
  },
  "logging": {
    "level": "INFO",
    "max_file_size_mb": 10,
    "backup_count": 5,
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "enable_request_logging": true,
    "enable_performance_logging": true
  },
  "server": {
    "host": "0.0.0.0",
    "port": 8000,
    "reload": false,
    "workers": 1,
    "max_request_size": "50MB",
    "timeout": 300
  },
  "models": {
    "default_model": "gemini_basic",
    "model_timeout": 30,
    "enable_caching": true,
    "cache_ttl": 3600
  },
  "batch_processing": {
    "enabled": true, // V2 feature
    "max_batch_size": 10,
    "parallel_processing": true,
    "batch_timeout": 600
  }
}
```

### api_keys.json (Authentication & Authorization)

Defines API keys with granular permissions for V1/V2 endpoints:

```json
{
  "api_keys": [
    {
      "key": "hackrx_2025_dev_key_123456789",
      "name": "Development Key",
      "created_date": "2025-07-26",
      "permissions": ["read", "write", "v1_access", "v2_access"],
      "rate_limits": {
        "requests_per_hour": 500,
        "batch_requests_per_hour": 50
      },
      "active": true,
      "environment": "development"
    },
    {
      "key": "hackrx_2025_prod_key_987654321",
      "name": "Production Key",
      "created_date": "2025-07-26",
      "permissions": ["read", "write", "v1_access", "v2_access", "admin"],
      "rate_limits": {
        "requests_per_hour": 1000,
        "batch_requests_per_hour": 100
      },
      "active": true,
      "environment": "production"
    },
    {
      "key": "hackrx_2025_test_key_555666777",
      "name": "Testing Key",
      "created_date": "2025-07-26",
      "permissions": ["read", "v1_access"],
      "rate_limits": {
        "requests_per_hour": 100,
        "batch_requests_per_hour": 0
      },
      "active": true,
      "environment": "testing"
    }
  ]
}
```

### .env.example (Environment Template)

```bash
# Application Environment
NODE_ENV=development
DEBUG=true

# API Configuration
HACKRX_API_PORT=8000
HACKRX_API_HOST=0.0.0.0

# Authentication
HACKRX_AUTH_ENABLED=true
HACKRX_API_KEY_FILE=Config/api_keys.json

# Model Configuration
GOOGLE_API_KEY=your-google-api-key-here
GEMINI_MODEL=gemini-1.5-flash
MODEL_TIMEOUT=30

# Database (if applicable)
DATABASE_URL=sqlite:///hackrx.db

# Redis Cache (for production)
REDIS_URL=redis://localhost:6379

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/hackrx.log

# Security
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]
```

]
}

````

## Available API Keys

| Key                              | Name            | Permissions | Purpose                 |
| -------------------------------- | --------------- | ----------- | ----------------------- |
| `hackrx_2025_dev_key_123456789`  | Development Key | read, write | Development and testing |
| `hackrx_2025_prod_key_987654321` | Production Key  | read, write | Production usage        |
| `hackrx_2025_test_key_555666777` | Testing Key     | read        | Read-only testing       |

## Security Notes

⚠️ **Important Security Considerations:**

1. **Keep API Keys Secret**: Never commit real API keys to version control
2. **Environment Variables**: In production, consider using environment variables
3. **Regular Rotation**: Rotate API keys regularly for security
4. **Least Privilege**: Grant minimum required permissions

## Configuration Management

### Disabling Authentication

For development, you can disable authentication:

```json
{
  "api_authentication": {
    "enabled": false
  }
}
````

### Adding New API Keys

1. Edit `api_keys.json`
2. Add new key object with appropriate permissions
3. Restart the application to reload configuration

### Permission Levels

- `read`: Access to read operations and data retrieval
- `write`: Access to write operations (includes read permissions)

## Environment Setup

For production deployment, consider using environment variables:

```bash
export HACKRX_API_KEY_FILE="/secure/path/api_keys.json"
export HACKRX_CONFIG_FILE="/secure/path/config.json"
```
