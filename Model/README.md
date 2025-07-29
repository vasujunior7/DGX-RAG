# 🤖 Model

This directory contains AI/ML models and inference components for document processing and question-answering capabilities, supporting both V1 and V2 API endpoints with enhanced features.

## 📁 Structure

```
Model/
├── sample_model.py          # Sample LLM model implementation
├── gemini_basic.py         # Google Gemini LLM integration (production-ready)
├── __pycache__/            # Python bytecode cache
└── README.md               # This documentation
```

## 🚀 Components

### `sample_model.py`

- **Sample model implementation** for testing and development
- **Simple interface** for document loading and inference
- **Mock responses** for rapid prototyping and testing
- **V1/V2 compatible** interface

**Class: `SampleModel`**

```python
class SampleModel:
    def __init__(self, api_key: str = None)
    def load_document(self, file_path: str) -> None
    def load_documents(self, file_paths: List[str]) -> None  # V2 feature
    def inference(self, question: str) -> str
    def batch_inference(self, questions: List[str]) -> List[str]  # V2 feature
```

**Features:**

- ✅ API key initialization (mock)
- ✅ Single document loading simulation
- ✅ **NEW**: Multiple document loading for V2 API
- ✅ Question answering with sample responses
- ✅ **NEW**: Batch processing capabilities
- ✅ Console logging for debugging
- ✅ Thread-safe operations

### `gemini_basic.py`

- **Google Gemini LLM integration** (production implementation)
- **Multi-format document loading** (PDF, DOCX, TXT)
- **Real AI inference** using Google's Generative AI
- **Enhanced V2 features** with batch processing and metadata

**Class: `GeminiBasicLLM`**

```python
class GeminiBasicLLM:
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-1.5-flash")
    def load_document(self, file_path: str) -> str
    def load_documents(self, file_paths: List[str]) -> Dict[str, str]  # V2 feature
    def inference(self, prompt: str, context: Optional[str] = None, use_documents: bool = True) -> str
    def batch_inference(self, prompts: List[str], options: Dict = None) -> List[Dict]  # V2 feature
    def chat(self, prompt: str) -> str
    def get_loaded_documents(self) -> List[Dict[str, Any]]
    def clear_documents(self)
    def get_processing_metadata(self) -> Dict  # V2 feature
```

**Features:**

- ✅ Google Gemini API integration with latest models
- ✅ Multi-format document support (PDF, DOCX, TXT, URLs)
- ✅ Context-aware responses with memory
- ✅ **NEW**: Batch document processing for V2 API
- ✅ **NEW**: Processing metadata and analytics
- ✅ **NEW**: Parallel processing capabilities
- ✅ Document management and caching
- ✅ Advanced error handling and validation
- ✅ Token usage tracking and optimization

## 🔧 Model Interface

All models in this directory implement a consistent interface supporting both V1 and V2 API requirements:

### Required Methods (V1 Compatible)

```python
def __init__(self, api_key: str = None):
    """Initialize the model with API credentials"""
    pass

def load_document(self, file_path: str) -> None:
    """Load and process a single document"""
    pass

def inference(self, question: str) -> str:
    """Generate answer for a given question"""
    pass
```

### Enhanced Methods (V2 Features)

```python
def load_documents(self, file_paths: List[str]) -> Dict[str, str]:
    """Load and process multiple documents simultaneously"""
    pass

def batch_inference(self, questions: List[str], options: Dict = None) -> List[Dict]:
    """Process multiple questions with enhanced responses"""
    pass

def get_processing_metadata(self) -> Dict:
    """Get processing statistics and metadata"""
    pass
```

### Optional Methods

```python
def chat(self, prompt: str) -> str:
    """Simple chat interface"""
    pass

def get_loaded_documents(self) -> List:
    """Get information about loaded documents"""
    pass

def clear_documents(self):
    """Clear all loaded documents from memory"""
    pass
```

## 📋 Document Support

### `SampleModel` (V1/V2 Compatible)

- **Input**: Any file path or list of paths (simulated)
- **Processing**: Mock processing with realistic timing simulation
- **Output**: Generic sample responses with metadata for V2
- **V2 Enhancements**: Supports batch processing and metadata responses

### `GeminiBasicLLM` (Production Ready)

- **Supported Formats**:
  - 📄 PDF files (via PyPDF2 and advanced parsing)
  - 📝 DOCX files (via python-docx with formatting preservation)
  - 📄 TXT files (with encoding detection)
  - 🌐 **NEW**: URL content extraction
  - 📊 **NEW**: CSV and structured data support
- **Processing**: Advanced text extraction with AI-powered analysis
- **Output**: Context-aware AI responses with source attribution
- **V2 Features**: Parallel processing, batch operations, metadata tracking

## 🔗 Dependencies

### `sample_model.py`

- **No external dependencies** (pure Python)
- **Threading support** for concurrent operations
- **Logging integration** with structured output

### `gemini_basic.py`

#### Core Dependencies

- `google-generativeai` - Google's Generative AI library (latest)
- `PyPDF2` - PDF processing and text extraction
- `python-docx` - DOCX file handling and formatting
- `pathlib` - Modern file path handling
- `typing` - Enhanced type hints for better code quality

#### V2 Enhancement Dependencies

- `concurrent.futures` - Parallel processing for batch operations
- `requests` - URL content fetching for web documents
- `chardet` - Character encoding detection
- `json` - Metadata and response formatting
- `time` - Processing timing and performance metrics

## 🚀 Usage Examples

### Using SampleModel (V1 API)

```python
from Model.sample_model import SampleModel

# Initialize model
model = SampleModel(api_key="dummy_key")

# Load single document
model.load_document("path/to/document.pdf")

# Get answer
answer = model.inference("What is this document about?")
print(answer)  # "Sample response to the question."
```

### Using SampleModel (V2 API)

```python
from Model.sample_model import SampleModel

# Initialize model
model = SampleModel(api_key="dummy_key")

# Load multiple documents
model.load_documents([
    "document1.pdf",
    "document2.docx",
    "document3.txt"
])

# Batch processing
questions = [
    "What is the main topic?",
    "Who are the key stakeholders?",
    "What are the conclusions?"
]

responses = model.batch_inference(questions, options={"include_metadata": True})
for response in responses:
    print(f"Q: {response['question']}")
    print(f"A: {response['answer']}")
    print(f"Source: {response['metadata']['source_document']}")
```

### Using GeminiBasicLLM (Production)

```python
from Model.gemini_basic import GeminiBasicLLM
import os

# Set API key
os.environ['GOOGLE_API_KEY'] = 'your-actual-api-key'

# Initialize model with enhanced features
llm = GeminiBasicLLM(model_name="gemini-1.5-pro")

# V1 API Compatible Usage
content = llm.load_document("document.pdf")
response = llm.inference("Summarize the main points")
print(response)

# V2 API Enhanced Usage - Batch Processing
documents = [
    "report1.pdf",
    "analysis2.docx",
    "data3.txt",
    "https://example.com/article"
]

# Load multiple documents
loaded_docs = llm.load_documents(documents)
print(f"Successfully loaded {len(loaded_docs)} documents")

# Batch inference with options
questions = [
    "What are the key findings?",
    "What recommendations are made?",
    "What are the risk factors?"
]

batch_responses = llm.batch_inference(
    questions,
    options={
        "include_sources": True,
        "max_length": 200,
        "temperature": 0.7
    }
)

# Process enhanced responses
for response in batch_responses:
    print(f"\nQuestion: {response['question']}")
    print(f"Answer: {response['answer']}")
    print(f"Sources: {', '.join(response['sources'])}")
    print(f"Confidence: {response['metadata']['confidence']}")

# Get processing statistics
metadata = llm.get_processing_metadata()
print(f"Total tokens used: {metadata['total_tokens']}")
print(f"Processing time: {metadata['processing_time']}s")
print(f"Documents in memory: {metadata['documents_loaded']}")
```

## 🔧 Configuration

### Environment Variables

- `GOOGLE_API_KEY` - **Required** for GeminiBasicLLM production usage
- `GEMINI_MODEL` - Optional: Specify Gemini model variant
- `MAX_BATCH_SIZE` - Optional: Maximum batch processing size (default: 10)
- `ENABLE_CACHING` - Optional: Enable document caching (default: true)

**Setup (Windows PowerShell):**

```powershell
$env:GOOGLE_API_KEY = "your-actual-api-key-here"
$env:GEMINI_MODEL = "gemini-1.5-pro"
$env:MAX_BATCH_SIZE = "15"
```

### Model Parameters

#### SampleModel Configuration

```python
model = SampleModel(
    api_key="test_key",           # Mock API key
    response_delay=0.1,           # Simulate processing time
    enable_logging=True           # Enable debug logging
)
```

#### GeminiBasicLLM Configuration

```python
llm = GeminiBasicLLM(
    api_key="your-api-key",           # Google API key
    model_name="gemini-1.5-flash",   # Model variant
    temperature=0.7,                  # Response creativity
    max_tokens=2048,                  # Maximum response length
    enable_caching=True,              # Document caching
    parallel_processing=True          # V2 batch processing
)
```

### Supported Model Variants

| Model            | Speed     | Quality   | Use Case                     |
| ---------------- | --------- | --------- | ---------------------------- |
| gemini-1.5-flash | ⚡ Fast   | 🟢 Good   | Development, Quick responses |
| gemini-1.5-pro   | 🐌 Slower | 🟡 Better | Production, Complex analysis |
| gemini-1.0-pro   | ⚡ Fast   | 🟢 Good   | Legacy compatibility         |

## 🧪 Testing

### Test SampleModel (V1/V2)

```powershell
# Quick V1 test
python -c "
from Model.sample_model import SampleModel
model = SampleModel('test')
model.load_document('test.pdf')
print(model.inference('test question'))
"

# V2 batch test
python -c "
from Model.sample_model import SampleModel
model = SampleModel('test')
model.load_documents(['doc1.pdf', 'doc2.txt'])
responses = model.batch_inference(['Q1?', 'Q2?'])
print(f'Processed {len(responses)} questions')
"
```

### Test GeminiBasicLLM (Production)

```powershell
# Basic functionality test
python -c "
import os
os.environ['GOOGLE_API_KEY'] = 'your-key'
from Model.gemini_basic import GeminiBasicLLM
llm = GeminiBasicLLM()
print(llm.chat('Hello, how are you?'))
"

# V2 enhanced features test
python -c "
import os
os.environ['GOOGLE_API_KEY'] = 'your-key'
from Model.gemini_basic import GeminiBasicLLM
llm = GeminiBasicLLM()
docs = llm.load_documents(['test1.pdf', 'test2.txt'])
responses = llm.batch_inference(['Question 1?', 'Question 2?'])
metadata = llm.get_processing_metadata()
print(f'Loaded: {len(docs)}, Processed: {len(responses)}, Metadata: {metadata}')
"
```

### Performance Testing

```python
# Test batch processing performance
import time
from Model.gemini_basic import GeminiBasicLLM

llm = GeminiBasicLLM()
start_time = time.time()

# Load multiple documents
docs = llm.load_documents([f"test_{i}.pdf" for i in range(5)])

# Batch process questions
questions = [f"Question {i}?" for i in range(10)]
responses = llm.batch_inference(questions)

end_time = time.time()
print(f"Processed {len(questions)} questions in {end_time - start_time:.2f} seconds")
```

## 🔄 Adding New Models

To add a new model with V1/V2 compatibility:

1. **Create Model File**: `Model/your_model.py`

```python
from typing import List, Dict, Optional
import concurrent.futures

class YourModel:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.loaded_documents = {}
        self.processing_stats = {"total_queries": 0, "total_time": 0}

    # V1 Compatible Methods
    def load_document(self, file_path: str) -> None:
        """V1: Load single document"""
        pass

    def inference(self, question: str) -> str:
        """V1: Single question processing"""
        pass

    # V2 Enhanced Methods
    def load_documents(self, file_paths: List[str]) -> Dict[str, str]:
        """V2: Load multiple documents"""
        pass

    def batch_inference(self, questions: List[str], options: Dict = None) -> List[Dict]:
        """V2: Batch question processing with metadata"""
        pass

    def get_processing_metadata(self) -> Dict:
        """V2: Get processing statistics"""
        return self.processing_stats
```

2. **Update Backend Integration**: Modify `Backend/api/v1/api.py` and `Backend/api/v2/api.py`

3. **Add Configuration**: Update environment variables and settings

4. **Test Compatibility**: Ensure both V1 and V2 API endpoints work

## 📊 Performance Considerations

### Model Comparison

| Model          | V1 Single Query | V2 Batch (10 queries) | Memory Usage | Best For             |
| -------------- | --------------- | --------------------- | ------------ | -------------------- |
| SampleModel    | ~0.1s           | ~0.5s                 | <10MB        | Testing, Development |
| GeminiBasicLLM | ~2-5s           | ~8-15s                | 50-200MB     | Production, Real AI  |

### Optimization Strategies

#### SampleModel

- **Speed**: Instant responses (mock)
- **Memory**: Minimal footprint
- **Scalability**: Unlimited (no API calls)
- **Use Case**: Testing, development, demonstrations

#### GeminiBasicLLM

- **Speed**: Network-dependent, caching improves performance
- **Memory**: Document content cached in memory
- **Scalability**: Limited by API quotas and rate limits
- **Optimization**:
  - Enable document caching
  - Use batch processing for multiple queries
  - Implement retry logic for network issues
  - Monitor token usage and costs

### V2 Batch Processing Benefits

- **Efficiency**: Process multiple questions simultaneously
- **Context Sharing**: Documents loaded once, used for all questions
- **Metadata**: Rich response information including sources and confidence
- **Parallel Processing**: Concurrent operations where supported
- **Resource Management**: Better memory and API quota utilization

## 🔒 Security & Best Practices

### API Key Management

- **Never commit API keys** to version control
- **Use environment variables** for sensitive credentials
- **Implement key rotation** for production environments
- **Monitor API usage** and set spending limits

### Document Security

- **Sanitize file paths** to prevent directory traversal
- **Validate file types** before processing
- **Limit file sizes** to prevent memory exhaustion
- **Clear sensitive documents** from memory after processing

### Error Handling

```python
try:
    response = llm.inference("Your question")
except Exception as e:
    logger.error(f"Model inference failed: {e}")
    # Fallback to default response or error handling
```

### Production Deployment

- **Rate limiting**: Implement request throttling
- **Caching**: Use Redis or similar for document caching
- **Monitoring**: Track performance and error rates
- **Load balancing**: Distribute requests across model instances

---

**🤖 AI/ML Component of the HackRX Project - Enhanced for V2 API**
