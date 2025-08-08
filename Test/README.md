# 🧪 HackRX Testing Suite - Comprehensive API Testing Infrastructure

Advanced testing suite for HackRX multi-model RAG system, supporting AURA Legal AI, SAM Insurance AI, and the main HackRX API with comprehensive load testing, performance monitoring, and multi-platform execution support.

## 📁 Testing Infrastructure

```
Test/
├── 🎯 Core Testing Scripts
│   ├── simple_test.py           # Quick API validation with current endpoint format
│   ├── load_test.py             # Advanced load testing (300+ lines) with metrics
│   ├── test_aura.py             # AURA Legal AI testing
│   ├── test_anthropic.py        # Anthropic API authentication testing
│   └── test_dependencies.py     # Environment and dependency validation
├── 🚀 Execution Runners
│   ├── run_tests.bat           # Windows batch testing with interactive menu
│   ├── run_load_test.bat       # Dedicated load testing batch script
│   ├── test_runner.ps1         # PowerShell runner with advanced parameters
│   └── api-keys.ps1            # PowerShell API key management script
├── 📊 Test Data & Configuration
│   ├── request.json            # Sample request payloads for testing
│   ├── test_request.json       # Additional test scenarios
│   └── requirements_test.txt   # Testing-specific Python dependencies
└── 📚 Documentation
    └── README.md               # This comprehensive testing guide
```

---

## 🎯 Quick Start Testing

### ⚡ Instant API Validation

```bash
# 1. Quick API test with current endpoint format
python Test/simple_test.py

# 2. Windows batch testing (interactive)
Test/run_tests.bat

# 3. PowerShell testing with options
powershell -ExecutionPolicy Bypass -File Test/test_runner.ps1
```

### 🏋️ Advanced Load Testing

```bash
# Basic load test with performance metrics
python Test/load_test.py

# Load test with multiple repetitions
python Test/load_test.py --repeat 10

# Comprehensive testing with JSON logging
python Test/load_test.py --verbose --output results.json
```

---

## 🚀 API Testing Features

### 📊 Current API Format Support

Our testing suite supports the **latest V2 API format**:

```json
{
    "documents": "https://example.com/document.pdf",
    "questions": [
        "What is the grace period for premium payment?",
        "What are the waiting periods for pre-existing conditions?",
        "Does this policy cover maternity expenses?"
    ]
}
```

**Endpoint**: `POST /hackrx/run`  
**Authentication**: `Bearer token` (any random string for development)

### ⚖️ AURA Legal AI Testing

```bash
# Test AURA Legal AI capabilities
python Test/test_aura.py

# Legal document analysis
curl -X POST "http://localhost:8000/aura/legal-query" \
  -H "Authorization: Bearer test_key_123" \
  -d '{"document": "legal_contract.pdf", "questions": ["What are the termination clauses?"]}'
```

### 🛡️ SAM Insurance AI Testing

```bash
# Test SAM Insurance AI
python Test/test_sam.py  # (if available)

# Insurance policy analysis
curl -X POST "http://localhost:8000/sam/policy-analysis" \
  -H "Authorization: Bearer test_key_123" \
  -d '{"policy": "insurance_policy.pdf", "analysis_type": "comprehensive"}'
```

### 💻 PowerShell (Windows)

```powershell
# Simple test
.\Test\test_runner.ps1 -TestType simple

# Load test with verbose output
.\Test\test_runner.ps1 -TestType load -Verbose

# Stress test (10 repeats)
.\Test\test_runner.ps1 -TestType stress
```

## 📊 Test Payload Overview

The load test sends requests to process **4 different documents** with **18 total questions**:

1. **Legal Constitution** (10 questions) - Rights, laws, constitutional matters
2. **Insurance Claims** (1 question) - HDFC claim scenarios
3. **Medical Insurance** (4 questions) - Coverage, claims, procedures
4. **Policy Terms** (3 questions) - Terms, conditions, coverage details

## 🛠️ Advanced Features

### `load_test.py` Features

- ✅ **Server health checks** before testing
- ✅ **Response time measurement** and statistics
- ✅ **Multiple test repeats** for consistency
- ✅ **JSON result logging** with timestamps
- ✅ **Comprehensive error handling** and reporting
- ✅ **API key authentication** support
- ✅ **Custom timeout** configurations
- ✅ **Detailed performance metrics**

### Example Output

```
🚀 HackRX API v2 Load Test
========================================
🌐 Server: http://localhost:8000
🔑 API Key: Not provided
⏱️  Timeout: 300s
🔁 Repeats: 1

🏥 Testing server health...
✅ Server is healthy!

📋 Test Payload Summary:
   📄 Documents: 4
   ❓ Total Questions: 18

📤 Sending request to API v2...
⏱️  Response Time: 42.15s
📊 Status Code: 200
✅ Request completed successfully!
📝 Received 18 answers

📊 TEST SUMMARY
============================================================
📈 Total Tests: 1
✅ Successful: 1
❌ Failed: 0
📊 Success Rate: 100.0%
⏱️  Average Response Time: 42.15s

💾 Results saved to: load_test_results_20250801_143022.json
🎉 All tests passed!
```

## 🔧 Configuration Options

### Command Line Arguments

| Argument    | Description                | Default                 |
| ----------- | -------------------------- | ----------------------- |
| `--server`  | Server URL                 | `http://localhost:8000` |
| `--api-key` | API key for authentication | None                    |
| `--verbose` | Enable detailed output     | False                   |
| `--timeout` | Request timeout (seconds)  | 300                     |
| `--repeat`  | Number of test repeats     | 1                       |

### Usage Examples

```bash
# Basic test
python Test/load_test.py

# Production server test
python Test/load_test.py --server https://api.hackrx.com --api-key your-key

# Stress testing
python Test/load_test.py --repeat 10 --timeout 600 --verbose

# Quick validation
python Test/simple_test.py
```

## 🐛 Troubleshooting

### Common Issues & Solutions

**Connection Error**

```
🌐 Connection error - is the server running?
💡 Try: python main.py
```

**Timeout Error**

```bash
# Increase timeout for heavy processing
python Test/load_test.py --timeout 600
```

**Authentication Error**

```bash
# Add API key
python Test/load_test.py --api-key your-api-key-here
```

---

# 🔐 Authentication Testing (Existing)

├── comprehensive_test.py # Full API functionality tests (V1/V2)
├── example_usage.py # Example usage scripts and demonstrations
├── test_v2_features.py # V2-specific feature tests
├── performance_test.py # Performance and load testing
├── integration_test.py # End-to-end integration tests
├── test_request.json # Sample request data for V1 API
├── test_request_v2.json # Sample request data for V2 API
└── README.md # This documentation

````

## 🔧 Test Categories

### Authentication Tests

#### `test_auth.py` - Comprehensive Authentication

- **API Key Validation**: Tests all configured API keys
- **Permission Testing**: Validates read/write/admin permissions
- **V1/V2 Access Control**: Tests version-specific access
- **Rate Limiting**: Validates request rate limits
- **Bearer Token Format**: Tests authentication header formats

#### `quick_test.py` - Quick Authentication Check

- **Basic Connectivity**: Verifies API server is running
- **Key Validation**: Quick API key authentication test
- **Endpoint Availability**: Checks V1/V2 endpoint status

### API Functionality Tests

#### `comprehensive_test.py` - Full API Testing

- **V1 API Endpoints**: Complete V1 functionality testing
- **V2 API Endpoints**: Enhanced V2 feature testing
- **Document Processing**: Single and batch document tests
- **Error Handling**: Invalid requests and error responses
- **Response Validation**: Schema and data validation

#### `test_v2_features.py` - V2 Enhanced Features

- **Batch Processing**: Multiple document processing
- **Metadata Responses**: Enhanced response validation
- **Source Attribution**: Document source tracking
- **Processing Options**: Custom processing parameters
- **Parallel Processing**: Concurrent request handling

### Performance Tests

#### `performance_test.py` - Load and Performance

- **Response Time**: Measures API response times
- **Throughput**: Tests requests per second capacity
- **Memory Usage**: Monitors memory consumption
- **Concurrent Users**: Simulates multiple users
- **Stress Testing**: High-load scenario testing

#### `integration_test.py` - End-to-End Testing

- **Full Workflow**: Complete user journey testing
- **Model Integration**: AI model response validation
- **Error Recovery**: Failure scenarios and recovery
- **Cross-Version**: V1 to V2 migration testing

## 🚀 Running Tests

### Prerequisites

```powershell
# Ensure API server is running
python main.py

# Install test dependencies (if any)
pip install requests pytest pytest-asyncio
````

### Authentication Tests

```powershell
# Quick authentication verification
python Test/quick_test.py

# Comprehensive authentication testing
python Test/test_auth.py

# Full authentication system test with V2 features
python Test/comprehensive_test.py
```

### V2 Feature Tests

```powershell
# Test V2-specific enhancements
python Test/test_v2_features.py

# Performance and load testing
python Test/performance_test.py

# End-to-end integration testing
python Test/integration_test.py
```

### Example Usage & Demonstrations

```powershell
# Run usage examples and demonstrations
python Test/example_usage.py

# Interactive testing session
python -i Test/example_usage.py
```

### Automated Test Suite

```powershell
# Run all tests using pytest
pytest Test/ -v --tb=short

# Run specific test categories
pytest Test/test_auth.py -v
pytest Test/test_v2_features.py -v

# Run with coverage report
pytest Test/ --cov=Backend --cov-report=html
```

## 📊 Test Data Formats

### V1 API Test Data (`test_request.json`)

```json
{
  "documents": "sample_document.pdf",
  "questions": [
    "What is the main topic of this document?",
    "Who are the key stakeholders mentioned?",
    "What are the main conclusions?"
  ]
}
```

### V2 API Test Data (`test_request_v2.json`)

```json
{
  "documents": [
    "document1.pdf",
    "document2.docx",
    "document3.txt",
    "https://example.com/document4"
  ],
  "questions": [
    "What are the key findings across all documents?",
    "What recommendations are provided?",
    "What are the common themes?",
    "How do the documents relate to each other?"
  ],
  "options": {
    "include_metadata": true,
    "include_sources": true,
    "max_length": 200,
    "temperature": 0.7,
    "parallel_processing": true
  }
}
```

### Batch Processing Test Data

```json
{
  "batch_requests": [
    {
      "documents": ["doc1.pdf", "doc2.pdf"],
      "questions": ["Question set 1?"],
      "options": { "include_metadata": true }
    },
    {
      "documents": ["doc3.pdf"],
      "questions": ["Question set 2?", "Another question?"],
      "options": { "max_length": 150 }
    }
  ]
}
```

## 🔑 API Keys for Testing

### Available Test Keys (from Config/api_keys.json)

| Key                              | Environment | Permissions                              | V1 Access | V2 Access | Rate Limit |
| -------------------------------- | ----------- | ---------------------------------------- | --------- | --------- | ---------- |
| `hackrx_2025_dev_key_123456789`  | Development | read, write, v1_access, v2_access        | ✅        | ✅        | 500/hour   |
| `hackrx_2025_prod_key_987654321` | Production  | read, write, v1_access, v2_access, admin | ✅        | ✅        | 1000/hour  |
| `hackrx_2025_test_key_555666777` | Testing     | read, v1_access                          | ✅        | ❌        | 100/hour   |

### Usage in Tests

```python
# Test configuration
TEST_KEYS = {
    "development": "hackrx_2025_dev_key_123456789",
    "production": "hackrx_2025_prod_key_987654321",
    "testing": "hackrx_2025_test_key_555666777"
}

# Authentication headers
def get_auth_header(key_type="development"):
    return {
        "Authorization": f"Bearer {TEST_KEYS[key_type]}",
        "Content-Type": "application/json"
    }
```

## 📋 Test Scenarios

### V1 API Test Scenarios

```python
# Basic V1 API test scenarios
V1_TEST_SCENARIOS = [
    {
        "name": "Single Document Processing",
        "endpoint": "/api/v1/hackrx/run",
        "method": "POST",
        "data": {
            "documents": "sample.pdf",
            "questions": ["What is this document about?"]
        },
        "expected_status": 200,
        "expected_fields": ["answers"]
    },
    {
        "name": "Multiple Questions",
        "endpoint": "/api/v1/hackrx/run",
        "method": "POST",
        "data": {
            "documents": "sample.pdf",
            "questions": [
                "What is the main topic?",
                "Who are the authors?",
                "What are the conclusions?"
            ]
        },
        "expected_status": 200,
        "expected_fields": ["answers"]
    }
]
```

### V2 API Test Scenarios

```python
# Enhanced V2 API test scenarios
V2_TEST_SCENARIOS = [
    {
        "name": "Batch Document Processing",
        "endpoint": "/api/v2/hackrx/run",
        "method": "POST",
        "data": {
            "documents": ["doc1.pdf", "doc2.docx", "doc3.txt"],
            "questions": ["What are the key themes?"],
            "options": {"include_metadata": True}
        },
        "expected_status": 200,
        "expected_fields": ["answers", "metadata", "sources"]
    },
    {
        "name": "Enhanced Response with Options",
        "endpoint": "/api/v2/hackrx/run",
        "method": "POST",
        "data": {
            "documents": ["sample.pdf"],
            "questions": ["Summarize this document"],
            "options": {
                "max_length": 150,
                "temperature": 0.8,
                "include_sources": True
            }
        },
        "expected_status": 200,
        "expected_fields": ["answers", "metadata", "sources"]
    }
]
```

### Error Handling Test Scenarios

```python
# Error scenarios for robust testing
ERROR_TEST_SCENARIOS = [
    {
        "name": "Invalid API Key",
        "headers": {"Authorization": "Bearer invalid_key"},
        "expected_status": 401,
        "expected_error": "authentication_failed"
    },
    {
        "name": "Missing Required Fields",
        "data": {"questions": ["Test question"]},  # Missing documents
        "expected_status": 422,
        "expected_error": "validation_error"
    },
    {
        "name": "Rate Limit Exceeded",
        "scenario": "Multiple rapid requests",
        "expected_status": 429,
        "expected_error": "rate_limit_exceeded"
    }
]
```

## 🎯 Example Test Implementations

### Authentication Test Example

```python
import requests
import json

def test_authentication():
    """Test API authentication with different keys"""
    base_url = "http://localhost:8000"

    # Test valid key
    valid_headers = {"Authorization": "Bearer hackrx_2025_dev_key_123456789"}
    response = requests.get(f"{base_url}/api/v1/auth/status", headers=valid_headers)
    assert response.status_code == 200

    # Test invalid key
    invalid_headers = {"Authorization": "Bearer invalid_key"}
    response = requests.get(f"{base_url}/api/v1/auth/status", headers=invalid_headers)
    assert response.status_code == 401

    print("✅ Authentication tests passed")
```

### V2 Feature Test Example

```python
def test_v2_batch_processing():
    """Test V2 batch processing capabilities"""
    base_url = "http://localhost:8000"
    headers = {
        "Authorization": "Bearer hackrx_2025_dev_key_123456789",
        "Content-Type": "application/json"
    }

    data = {
        "documents": ["test1.pdf", "test2.pdf"],
        "questions": ["What are the main points?"],
        "options": {
            "include_metadata": True,
            "parallel_processing": True
        }
    }

    response = requests.post(f"{base_url}/api/v2/hackrx/run",
                           headers=headers, json=data)

    assert response.status_code == 200
    result = response.json()

    # Validate V2 response structure
    assert "answers" in result
    assert "metadata" in result
    assert "sources" in result
    assert len(result["sources"]) == 2  # Two documents

    print("✅ V2 batch processing test passed")
```

### Performance Test Example

```python
import time
import concurrent.futures

def test_performance():
    """Test API performance and response times"""
    base_url = "http://localhost:8000"
    headers = {"Authorization": "Bearer hackrx_2025_dev_key_123456789"}

    def make_request():
        start_time = time.time()
        response = requests.get(f"{base_url}/api/v1/", headers=headers)
        end_time = time.time()
        return response.status_code, end_time - start_time

    # Test concurrent requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(make_request) for _ in range(10)]
        results = [future.result() for future in futures]

    # Analyze results
    response_times = [result[1] for result in results]
    avg_response_time = sum(response_times) / len(response_times)

    assert avg_response_time < 1.0  # Should respond within 1 second
    print(f"✅ Average response time: {avg_response_time:.3f}s")
```

## 🔍 Test Validation

### Response Schema Validation

```python
from jsonschema import validate

# V1 Response Schema
V1_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "answers": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["answers"]
}

# V2 Response Schema
V2_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "answers": {
            "type": "array",
            "items": {"type": "string"}
        },
        "metadata": {
            "type": "object",
            "properties": {
                "processing_time": {"type": "number"},
                "model_used": {"type": "string"},
                "documents_processed": {"type": "integer"}
            }
        },
        "sources": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["answers", "metadata", "sources"]
}

def validate_response(response_data, api_version="v1"):
    """Validate API response against schema"""
    schema = V2_RESPONSE_SCHEMA if api_version == "v2" else V1_RESPONSE_SCHEMA
    validate(instance=response_data, schema=schema)
```

## 📈 Test Reporting

### Automated Test Reports

```python
# Generate test report
def generate_test_report(test_results):
    """Generate comprehensive test report"""
    report = {
        "test_summary": {
            "total_tests": len(test_results),
            "passed": len([r for r in test_results if r["status"] == "passed"]),
            "failed": len([r for r in test_results if r["status"] == "failed"]),
            "execution_time": sum([r["duration"] for r in test_results])
        },
        "test_details": test_results,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    # Save report
    with open(f"test_report_{int(time.time())}.json", "w") as f:
        json.dump(report, f, indent=2)

    return report
```

## 🛠️ Testing Best Practices

### Test Environment Setup

- ✅ **Isolated Environment**: Use separate test database/config
- ✅ **Clean State**: Reset state between tests
- ✅ **Reproducible**: Tests should produce consistent results
- ✅ **Independent**: Tests should not depend on each other
- ✅ **Fast Execution**: Optimize for quick feedback

### Data Management

- ✅ **Test Data Separation**: Keep test data separate from production
- ✅ **Data Cleanup**: Clean up test data after execution
- ✅ **Realistic Data**: Use data similar to production scenarios
- ✅ **Edge Cases**: Test boundary conditions and edge cases

### Continuous Integration

```yaml
# Example CI configuration (.github/workflows/tests.yml)
name: API Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: "3.12"
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: |
          python main.py &
          sleep 10
          pytest Test/ -v --tb=short
          kill %1
```

---

**🧪 Comprehensive Test Suite for HackRX V2 API**
