# Test Files

This directory contains all test files and example usage scripts for the HackRX API.

## Files

### Test Scripts
- `test_auth.py` - Comprehensive authentication system tests
- `quick_test.py` - Quick authentication verification
- `comprehensive_test.py` - Full API functionality tests
- `example_usage.py` - Example usage scripts and demonstrations

### Test Data
- `test_request.json` - Sample request data for testing the API

## Running Tests

### Authentication Tests
```bash
# Quick authentication test
python Test/quick_test.py

# Comprehensive authentication test
python Test/comprehensive_test.py

# Full authentication system test
python Test/test_auth.py
```

### Example Usage
```bash
# Run example usage demonstrations
python Test/example_usage.py
```

## Test Requirements

Make sure the HackRX API server is running before executing tests:
```bash
python main.py
```

## Test Data Format

The `test_request.json` file contains sample data in the expected API format:
```json
{
    "documents": "document_url",
    "questions": ["question1", "question2", ...]
}
```

## API Keys for Testing

Use the following API keys for testing (defined in Config/api_keys.json):
- Development: `hackrx_2025_dev_key_123456789`
- Production: `hackrx_2025_prod_key_987654321`
- Testing (read-only): `hackrx_2025_test_key_555666777`
