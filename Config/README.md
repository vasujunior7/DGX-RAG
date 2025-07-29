# Configuration Files

This directory contains all configuration files for the HackRX API.

## Files

### Main Configuration

- `config.json` - Main application configuration
- `api_keys.json` - API key definitions and permissions

## Configuration Details

### config.json

Controls the main application behavior:

```json
{
  "api_authentication": {
    "enabled": true, // Enable/disable authentication
    "require_api_key": true // Require API key for protected endpoints
  },
  "logging": {
    "level": "INFO",
    "max_file_size_mb": 10,
    "backup_count": 5
  },
  "server": {
    "host": "0.0.0.0",
    "port": 8000,
    "reload": false
  }
}
```

### api_keys.json

Defines all valid API keys with their permissions:

```json
{
  "api_keys": [
    {
      "key": "hackrx_2025_dev_key_123456789",
      "name": "Development Key",
      "created_date": "2025-07-26",
      "permissions": ["read", "write"],
      "active": true
    }
  ]
}
```

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
```

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
