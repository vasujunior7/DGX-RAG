# 🤖 AI Models - Multi-Model RAG Architecture

Advanced AI model directory featuring specialized legal and insurance AI systems with multi-model LLM integration including Anthropic Claude, OpenAI GPT, Google Gemini, and Groq for comprehensive document processing and analysis.

## 📁 Model Architecture

```
Model/
├── ⚖️ AURA - Legal AI Specialist
│   ├── infrance.py              # Legal document inference engine
│   ├── legal_chunker/           # Legal text analysis system
│   │   ├── llm_answer.py       # Anthropic Claude integration  
│   │   └── __pycache__/        # Compiled modules
│   └── __pycache__/            # Compiled legal AI modules
├── 🛡️ SAM_model - Insurance AI Specialist  
│   ├── src/                    # Core SAM architecture
│   │   ├── config.py           # SAM configuration
│   │   ├── legal_query_rag.py  # RAG for legal queries
│   │   ├── llm_generator.py    # LLM generation engine
│   │   ├── embeddings.py       # Text embeddings  
│   │   ├── retrieval.py        # Document retrieval
│   │   ├── vector_db.py        # Vector database management
│   │   └── evaluation.py       # Model evaluation metrics
│   ├── embeddings_cache/       # Pre-computed embeddings
│   │   ├── *.faiss             # FAISS index files
│   │   └── *.pkl               # Pickle embedding files
│   ├── processed_documents/    # Cached processed documents
│   ├── inference.py           # Main SAM inference engine
│   ├── setup.py               # SAM installation script
│   └── requirements.txt       # SAM-specific dependencies
├── 🚀 Core LLM Integration
│   └── gemini_basic.py        # Google Gemini integration
└── 📚 Documentation
    └── README.md              # This comprehensive guide
```

## ⚖️ AURA - Legal AI Specialist

**Advanced Legal Document Analysis and Reasoning System**

### 🎯 **Core Capabilities**
- **📜 Legal Document Processing** - Contracts, policies, regulations, case law
- **🔍 Legal Research** - Precedent analysis and case law lookup
- **⚖️ Compliance Analysis** - Regulatory compliance checking
- **💼 Contract Review** - Terms, conditions, and risk assessment
- **🧠 Legal Reasoning** - Claude-powered sophisticated legal analysis

### 🔧 **Architecture Components**

#### `infrance.py` - Legal Inference Engine
```python
class AURALegalProcessor:
    def __init__(self, anthropic_key: str):
        # Initialize with Anthropic Claude
        
    def analyze_legal_document(self, document_url: str, questions: List[str]):
        # Legal document analysis with specialized prompting
        
    def case_law_research(self, legal_query: str):
        # Case law and precedent research
        
    def compliance_check(self, document: str, regulations: List[str]):
        # Regulatory compliance analysis
```

#### `legal_chunker/llm_answer.py` - Anthropic Integration
- **🤖 Claude 3.5 Sonnet Integration** - Advanced reasoning capabilities
- **📋 Legal Context Processing** - Specialized legal document chunking
- **🔐 Secure Authentication** - Production-ready API key management
- **⚡ Error Handling** - Robust error handling with fallback systems

### 💡 **Usage Examples**

```python
from Model.AURA.infrance import AURALegalProcessor

# Initialize AURA Legal AI
aura = AURALegalProcessor(anthropic_key="your_key")

# Legal document analysis
result = aura.analyze_legal_document(
    document_url="https://example.com/contract.pdf",
    questions=[
        "What are the termination clauses?",
        "Are there any penalty provisions?",
        "What dispute resolution mechanisms are included?"
    ]
)

# Case law research
precedents = aura.case_law_research(
    "employment contract termination without cause"
)
```

## 🛡️ SAM - Insurance AI Specialist

**Specialized Insurance Policy Analysis and Claims Processing Model**

### 🎯 **Advanced Features**
- **📋 Policy Analysis** - Comprehensive insurance policy understanding
- **💰 Claims Processing** - Automated claims evaluation and settlement
- **🔍 Coverage Assessment** - Gap analysis and coverage optimization
- **📊 Risk Evaluation** - Risk scoring and assessment
- **⚡ High-Performance Caching** - FAISS-powered embeddings cache

### 🏗️ **SAM Architecture**

#### Core Engine - `inference.py`
```python
class SAMInferenceEngine:
    def __init__(self):
        self.embeddings_cache = FAISSEmbeddingsCache()
        self.retrieval_system = DocumentRetrieval()
        self.llm_generator = LLMGenerator()
        
    def analyze_policy(self, policy_url: str, questions: List[str]):
        # High-performance policy analysis with caching
        
    def process_claim(self, claim_data: dict):
        # Automated claims processing and evaluation
```

#### Performance Optimization
- **💾 Embeddings Cache** - Pre-computed document embeddings in `embeddings_cache/`
  ```
  embeddings_cache/
  ├── policy_doc1.pdf_embeddings.pkl.faiss  # FAISS indices
  ├── policy_doc1.pdf_embeddings.pkl.pkl    # Pickle embeddings
  └── ...
  ```
- **📄 Document Cache** - Processed documents in `processed_documents/`
- **🔄 FAISS Integration** - Sub-second similarity search
- **⚡ Vector Database** - Optimized vector storage and retrieval

#### Advanced RAG Pipeline
```python
# SAM RAG Components
src/
├── legal_query_rag.py     # RAG for insurance legal queries
├── embeddings.py          # Advanced text embeddings
├── retrieval.py           # Document retrieval system
├── vector_db.py           # Vector database management
├── llm_generator.py       # Multi-model LLM generation
└── evaluation.py          # Performance evaluation metrics
```

### 💡 **Usage Examples**

```python
from Model.SAM_model.inference import SAMInferenceEngine

# Initialize SAM Insurance AI
sam = SAMInferenceEngine()

# Policy analysis
analysis = sam.analyze_policy(
    policy_url="https://example.com/policy.pdf",
    questions=[
        "What is the coverage amount?",
        "What are the exclusions?",
        "What is the claim settlement process?",
        "Are pre-existing conditions covered?"
    ]
)

# Claims processing
claim_result = sam.process_claim({
    "policy_number": "POL123456",
    "claim_type": "hospitalization",
    "amount": 50000,
    "documents": ["hospital_bill.pdf", "discharge_summary.pdf"]
})
```

## 🚀 Multi-Model LLM Integration

### 🤖 **Supported AI Models**

#### Google Gemini (`gemini_basic.py`)
```python
from Model.gemini_basic import GeminiModel

gemini = GeminiModel(api_key="your_google_api_key")
response = gemini.inference(
    document_url="https://example.com/document.pdf",
    question="Analyze this document"
)
```

#### Model Capabilities Matrix

| Model | Strength | Use Case | Integration |
|-------|----------|----------|-------------|
| **🤖 Anthropic Claude** | Legal reasoning, complex analysis | AURA Legal AI | `legal_chunker/llm_answer.py` |
| **🧠 OpenAI GPT** | General intelligence, versatile | General document processing | Multi-model pipeline |
| **🚀 Google Gemini** | Multi-modal, fast inference | Document understanding | `gemini_basic.py` |
| **⚡ Groq** | Ultra-fast inference | Real-time responses | Speed-optimized pipeline |

## 🔧 Configuration & Setup

### 📋 **Environment Requirements**

```bash
# Core AI model keys (choose minimum 1-2)
ANTHROPIC_API_KEY=sk-ant-...        # For AURA Legal AI
OPENAI_API_KEY=sk-...               # General processing
GOOGLE_API_KEY=AI...                # Gemini integration  
GROQ_API_KEY=gsk_...                # Fast inference

# Performance optimization
CUDA_VISIBLE_DEVICES=0              # GPU acceleration
FAISS_USE_CUDA=true                 # FAISS GPU support
```

### 🚀 **Installation & Setup**

```bash
# Install model dependencies
pip install -r Model/SAM_model/requirements.txt

# Setup SAM model
cd Model/SAM_model
python setup.py install

# Validate model installation
python Model/SAM_model/test_installation.py
```

### 🧪 **Model Testing**

```bash
# Test AURA Legal AI
python Model/AURA/test_aura.py

# Test SAM Insurance AI  
python Model/SAM_model/test_module.py

# Test Gemini integration
python Model/test_gemini.py

# Comprehensive model testing
python Test/test_dependencies.py
```

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
