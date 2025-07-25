# 🤖 Model

This directory contains AI/ML models and inference components for document processing and question-answering capabilities.

## 📁 Structure

```
Model/
├── sample_model.py          # Sample LLM model implementation
├── gemini_basic.py         # Google Gemini LLM integration (basic)
└── __pycache__/            # Python bytecode cache
```

## 🚀 Components

### `sample_model.py`

- **Sample model implementation** for testing and development
- **Simple interface** for document loading and inference
- **Mock responses** for rapid prototyping

**Class: `SampleModel`**

```python
class SampleModel:
    def __init__(self, api_key: str = None)
    def load_document(self, file_path: str) -> None
    def inference(self, question: str) -> str
```

**Features:**

- ✅ API key initialization (mock)
- ✅ Document loading simulation
- ✅ Question answering with sample responses
- ✅ Console logging for debugging

### `gemini_basic.py`

- **Google Gemini LLM integration** (comprehensive implementation)
- **Document loading** from multiple formats (PDF, DOCX, TXT)
- **Real AI inference** using Google's Generative AI

**Class: `GeminiBasicLLM`**

```python
class GeminiBasicLLM:
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-1.5-flash")
    def load_document(self, file_path: str) -> str
    def inference(self, prompt: str, context: Optional[str] = None, use_documents: bool = True) -> str
    def chat(self, prompt: str) -> str
    def get_loaded_documents(self) -> List[Dict[str, Any]]
    def clear_documents(self)
```

**Features:**

- ✅ Google Gemini API integration
- ✅ Multi-format document support (PDF, DOCX, TXT)
- ✅ Context-aware responses
- ✅ Document management
- ✅ Error handling and validation

## 🔧 Model Interface

All models in this directory should implement a consistent interface:

### Required Methods

```python
def __init__(self, api_key: str = None):
    """Initialize the model with API credentials"""
    pass

def load_document(self, file_path: str) -> None:
    """Load and process a document"""
    pass

def inference(self, question: str) -> str:
    """Generate answer for a given question"""
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
    """Clear all loaded documents"""
    pass
```

## 📋 Document Support

### `SampleModel`

- **Input**: Any file path (simulated)
- **Processing**: Mock processing with console output
- **Output**: Generic sample responses

### `GeminiBasicLLM`

- **Supported Formats**:
  - 📄 PDF files (via PyPDF2)
  - 📝 DOCX files (via python-docx)
  - 📄 TXT files (direct reading)
- **Processing**: Real text extraction and AI analysis
- **Output**: Context-aware AI responses

## 🔗 Dependencies

### `sample_model.py`

- **No external dependencies** (pure Python)

### `gemini_basic.py`

- `google-generativeai` - Google's Generative AI library
- `PyPDF2` - PDF processing
- `python-docx` - DOCX file handling
- `pathlib` - File path handling
- `typing` - Type hints

## 🚀 Usage Examples

### Using SampleModel

```python
from Model.sample_model import SampleModel

# Initialize model
model = SampleModel(api_key="dummy_key")

# Load document
model.load_document("path/to/document.pdf")

# Get answer
answer = model.inference("What is this document about?")
print(answer)  # "Sample response to the question."
```

### Using GeminiBasicLLM

```python
from Model.gemini_basic import GeminiBasicLLM
import os

# Set API key
os.environ['GOOGLE_API_KEY'] = 'your-actual-api-key'

# Initialize model
llm = GeminiBasicLLM()

# Load document
content = llm.load_document("document.pdf")

# Get AI response
response = llm.inference("Summarize the main points")
print(response)

# Check loaded documents
docs = llm.get_loaded_documents()
print(f"Loaded {len(docs)} documents")
```

## 🔧 Configuration

### Environment Variables

- `GOOGLE_API_KEY` - Required for GeminiBasicLLM
- Set via: `set GOOGLE_API_KEY=your-key-here` (Windows)

### Model Parameters

#### SampleModel

- `api_key` - Mock API key (any string)

#### GeminiBasicLLM

- `api_key` - Google API key (or environment variable)
- `model_name` - Gemini model variant (default: "gemini-1.5-flash")

## 🧪 Testing

### Test SampleModel

```python
# Quick test
python -c "
from Model.sample_model import SampleModel
model = SampleModel('test')
model.load_document('test.pdf')
print(model.inference('test question'))
"
```

### Test GeminiBasicLLM

```python
# With proper API key
python -c "
import os
os.environ['GOOGLE_API_KEY'] = 'your-key'
from Model.gemini_basic import GeminiBasicLLM
llm = GeminiBasicLLM()
print(llm.chat('Hello, how are you?'))
"
```

## 🔄 Adding New Models

To add a new model:

1. **Create new file**: `Model/your_model.py`
2. **Implement interface**:
   ```python
   class YourModel:
       def __init__(self, api_key: str = None):
           # Initialize your model
           pass

       def load_document(self, file_path: str) -> None:
           # Document loading logic
           pass

       def inference(self, question: str) -> str:
           # Inference logic
           return "Your response"
   ```
3. **Update Backend**: Modify `Backend/api/v1/api.py` to use your model
4. **Test**: Ensure compatibility with existing API

## 📊 Performance Considerations

### SampleModel

- **Speed**: Instant (mock responses)
- **Memory**: Minimal usage
- **Use Case**: Development and testing

### GeminiBasicLLM

- **Speed**: Depends on network and API response time
- **Memory**: Stores document content in memory
- **Use Case**: Production with real AI capabilities

## 🔒 Security

- **API Keys**: Never commit API keys to version control
- **Environment Variables**: Use environment variables for sensitive data
- **Document Handling**: Be careful with document content in logs

---

**AI/ML Component of the HackRX Project**
