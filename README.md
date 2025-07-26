# 🚀 HackRX - AI-Powered Document Processing API

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge)](LICENSE)

A high-performance FastAPI-based service that provides intelligent document processing and question-answering capabilities using advanced LLM integration. Built for the HackRX hackathon, this API enables users to upload documents and get AI-powered answers to their questions.

## 🌟 Features

- **🤖 AI-Powered Document Analysis** - Process documents using advanced LLM models
- **📄 Multi-Format Support** - Handle PDF, DOCX, and TXT documents
- **🚀 High-Performance API** - Built with FastAPI for maximum speed
- **📊 Comprehensive Logging** - Full request/response logging with rotation
- **📖 Interactive Documentation** - Auto-generated Swagger UI and ReDoc
- **🔒 Secure Architecture** - Token-based authentication support
- **🎨 Beautiful Web Interface** - HTML guide for easy API exploration
- **⚡ Auto-Reload Development** - Hot reloading for rapid development

## 🏗️ Project Structure

```
HackRX/
├── 📄 main.py                 # Application entry point
├── 📁 Backend/                # Core API implementation
│   ├── main_api.py           # Main FastAPI application
│   └── api/v1/               # Version 1 API endpoints
├── 📁 Model/                  # AI/ML models and inference
├── 📁 utils/                  # Utility functions and middleware
├── 📁 templates/              # HTML templates and documentation
├── 📁 Config/                 # Configuration files
│   ├── config.json           # Main application configuration
│   ├── api_keys.json         # API key definitions
│   └── README.md             # Configuration documentation
├── 📁 Test/                   # Test files and examples
│   ├── test_auth.py          # Authentication tests
│   ├── comprehensive_test.py # Full API tests
│   ├── test_request.json     # Sample test data
│   └── README.md             # Test documentation
├── 📁 logs/                   # Application logs
├── 📁 Frontend/               # Frontend components
├── 📄 requirements.txt        # Python dependencies
└── 📄 README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/vasujunior7/DGX-RAG.git
   cd HackRX
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional)

   ```bash
   # For production use
   set GOOGLE_API_KEY=your_google_api_key_here
   ```

4. **Run the application**

   ```bash
   python main.py
   ```

5. **Access the API**
   - **Web Interface**: http://localhost:8000/
   - **Interactive Docs**: http://localhost:8000/docs
   - **ReDoc**: http://localhost:8000/redoc

## 📋 API Endpoints

### Core Endpoints

| Method | Endpoint             | Description                                                |
| ------ | -------------------- | ---------------------------------------------------------- |
| `GET`  | `/`                  | HTML API guide and documentation                           |
| `GET`  | `/help`              | Basic API information                                      |
| `GET`  | `/api/v1/`           | Version 1 welcome message                                  |
| `POST` | `/api/v1/hackrx/run` | **Main endpoint** - Process documents and answer questions |

### Main API Usage

**Process Documents and Answer Questions:**

```bash
curl -X POST "http://localhost:8000/api/v1/hackrx/run" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer your-token-here" \
     -d '{
       "documents": "https://example.com/document.pdf",
       "questions": [
         "What is the main topic of this document?",
         "What are the key findings?",
         "Are there any recommendations?"
       ]
     }'
```

**Response:**

```json
{
  "answers": [
    "The main topic is...",
    "The key findings include...",
    "The recommendations are..."
  ]
}
```

## 🛠️ Development

### Project Components

- **Backend**: FastAPI application with versioned API endpoints
- **Model**: AI/ML models for document processing and inference
- **Utils**: Logging, middleware, and utility functions
- **Templates**: HTML templates for web interface
- **Logs**: Comprehensive logging with rotation

### Adding New Features

1. Create new endpoints in `Backend/api/v1/`
2. Add model functionality in `Model/`
3. Update documentation in `templates/`
4. Test using the interactive docs at `/docs`

### Running in Development Mode

The application runs with auto-reload enabled by default:

```bash
python main.py
```

Changes to Python files will automatically restart the server.

## 📊 Logging

The application provides comprehensive logging:

- **Request Logs**: `logs/requests.log` - All HTTP requests/responses
- **Application Logs**: `logs/app.log` - Application-specific events
- **Server Logs**: `logs/uvicorn.log` - Server startup/shutdown events
- **Access Logs**: `logs/uvicorn_access.log` - Server access logs

All logs feature automatic rotation (10MB max, 5 backups).

## 🧪 Testing

Test the API using the interactive documentation:

1. Visit http://localhost:8000/docs
2. Click "Try it out" on any endpoint
3. Fill in the required parameters
4. Execute the request

Or use curl/Python requests as shown in the examples above.

## 📚 Documentation

- **Interactive API Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc (ReDoc)
- **API Guide**: http://localhost:8000/ (Custom HTML guide)

## 🔧 Configuration

### Environment Variables

- `GOOGLE_API_KEY`: API key for Google's Gemini model (optional for development)

### Logging Configuration

Logging settings can be modified in `main.py` and `utils/logging_config.py`.

### Server Configuration

Server settings (host, port, reload) can be modified in `main.py`.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For support and questions:

- Create an issue on GitHub
- Check the interactive documentation at `/docs`
- Review the API guide at the root URL

## 🏆 HackRX 2025

This project was built for the HackRX 2025 hackathon, showcasing:

- **Advanced AI Integration**: Document processing with LLM models
- **Production-Ready Architecture**: Comprehensive logging, error handling
- **Developer Experience**: Interactive docs, beautiful web interface
- **Scalable Design**: Versioned APIs, modular structure

---

**Built with ❤️ for HackRX 2025**
