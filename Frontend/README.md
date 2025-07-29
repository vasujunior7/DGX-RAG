# 🎨 HackRX Frontend

## Overview

Modern, responsive HTML/CSS/JavaScript frontend for the HackRX Document Processing Platform. Provides an intuitive interface to interact with both V1 and V2 API endpoints without requiring complex build processes or frameworks.

## ✨ Features

### Core Features

- **Pure HTML/CSS/JS** - Zero build process, instant deployment
- **Modern UI Design** - Glass morphism effects with responsive layout
- **V1/V2 API Support** - Compatible with both API versions
- **Interactive API Guide** - Built-in testing interface and documentation
- **Document Processing** - Upload documents and process questions

### Enhanced V2 Features

- **Batch Processing** - Handle multiple documents simultaneously
- **API Version Selection** - Switch between V1 and V2 endpoints
- **Enhanced Responses** - Display metadata, sources, and processing info
- **Real-time Feedback** - Processing status and progress indicators
- **Response Comparison** - Compare V1 vs V2 API responses

### User Experience

- **Local Storage** - Processing history and settings persistence
- **Export Functionality** - Download results as JSON/CSV
- **Error Handling** - Comprehensive error messages and recovery
- **Mobile Responsive** - Optimized for all device sizes
- **Accessibility** - WCAG 2.1 compliant interface

## 🚀 Quick Start

### Method 1: Run with main.py (Recommended)

```powershell
# From the main project directory
python main.py
```

This launches:

- **FastAPI backend** (port 8000) with V1/V2 APIs
- **Frontend server** (port 3000) with auto-reload
- **Integrated logging** and monitoring

### Method 2: Direct HTML Opening

```powershell
# Open HTML file directly in browser
start index.html
# Or
start templates/api_guide.html  # For API testing interface
```

**Note**: Manual backend startup required for API functionality

### Method 3: Static Server (Development)

```powershell
# Using Python's built-in server
cd Frontend
python -m http.server 3000
# Then open http://localhost:3000
```

## 📁 File Structure

```
Frontend/
├── index.html          # Main application interface
├── templates/
│   └── api_guide.html  # Interactive API testing guide
├── assets/             # Static assets (if any)
└── README.md          # This documentation
```

## 🔗 API Integration

### V1 API Endpoints (Legacy Support)

- `GET /api/v1/` - API status and information
- `POST /api/v1/hackrx/run` - Single document processing
- `GET /api/v1/auth/status` - Authentication status

### V2 API Endpoints (Enhanced Features)

- `GET /api/v2/` - Enhanced API status with features
- `POST /api/v2/hackrx/run` - Batch document processing
- `GET /api/v2/auth/status` - Advanced authentication info
- `GET /api/v2/hackrx/metadata` - Processing metadata

### Documentation Endpoints

- `GET /docs` - Interactive FastAPI documentation
- `GET /redoc` - Alternative API documentation
- `GET /api_guide` - Custom HTML API guide with testing

## 🎯 Usage Examples

### V1 API Usage (Single Document)

```javascript
// Frontend JavaScript example
const processDocument = async () => {
  const response = await fetch("/api/v1/hackrx/run", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer hackrx_2025_dev_key_123456789",
    },
    body: JSON.stringify({
      documents: "document.pdf",
      questions: ["What is the main topic?"],
    }),
  });

  const result = await response.json();
  console.log(result.answers);
};
```

### V2 API Usage (Batch Processing)

```javascript
// Enhanced V2 processing with metadata
const processBatchDocuments = async () => {
  const response = await fetch("/api/v2/hackrx/run", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer hackrx_2025_dev_key_123456789",
    },
    body: JSON.stringify({
      documents: ["doc1.pdf", "doc2.docx", "doc3.txt"],
      questions: [
        "What are the key findings?",
        "What recommendations are provided?",
        "What are the main conclusions?",
      ],
      options: {
        include_metadata: true,
        max_length: 200,
      },
    }),
  });

  const result = await response.json();
  console.log(result.answers);
  console.log(result.metadata);
  console.log(result.sources);
};
```

## 🛠️ Customization

### Update API Base URL

Edit the `baseUrl` variable in your HTML files:

```javascript
// In index.html or api_guide.html
const baseUrl = "http://localhost:8000"; // Development
// const baseUrl = 'https://your-domain.com'; // Production
```

### API Version Configuration

```javascript
// Configure default API version
const defaultApiVersion = "v2"; // Use V2 by default
// const defaultApiVersion = 'v1'; // Fallback to V1 if needed

// Dynamic version switching
const switchApiVersion = (version) => {
  if (version === "v2") {
    // Enable V2 features: batch processing, metadata, enhanced responses
    enableBatchProcessing(true);
    enableMetadataDisplay(true);
  } else {
    // V1 compatibility mode
    enableBatchProcessing(false);
    enableMetadataDisplay(false);
  }
};
```

### Authentication Configuration

```javascript
// Configure API authentication
const apiConfig = {
  // Development key (for testing)
  devApiKey: "hackrx_2025_dev_key_123456789",

  // Production key (from environment)
  prodApiKey:
    process.env.HACKRX_API_KEY || localStorage.getItem("hackrx_api_key"),

  // Bearer token format
  getAuthHeader: () => ({
    Authorization: `Bearer ${apiConfig.getCurrentKey()}`,
  }),

  getCurrentKey: () => {
    return window.location.hostname === "localhost"
      ? apiConfig.devApiKey
      : apiConfig.prodApiKey;
  },
};
```

### Styling Customization

All CSS is embedded for simplicity. Key customization areas:

```css
/* Main theme colors */
:root {
  --primary-color: #3b82f6; /* Blue theme */
  --secondary-color: #10b981; /* Green accents */
  --background: #0f172a; /* Dark background */
  --surface: rgba(255, 255, 255, 0.1); /* Glass effect */
  --text-primary: #ffffff; /* Main text */
  --text-secondary: #94a3b8; /* Secondary text */
}

/* Responsive breakpoints */
@media (max-width: 768px) {
  /* Mobile optimizations */
}

@media (max-width: 480px) {
  /* Small screen adjustments */
}
```

### Feature Toggles

```javascript
// Enable/disable features based on API version
const featureFlags = {
  batchProcessing: true, // V2 only
  metadataDisplay: true, // V2 only
  sourceAttribution: true, // V2 only
  exportOptions: true, // Both V1/V2
  historyTracking: true, // Both V1/V2
  realTimeStatus: true, // Both V1/V2
};
```

## 📱 Browser Compatibility

### Supported Browsers

| Browser       | Version | V1 API | V2 API | Notes                    |
| ------------- | ------- | ------ | ------ | ------------------------ |
| Chrome        | 80+     | ✅     | ✅     | Full feature support     |
| Firefox       | 75+     | ✅     | ✅     | Full feature support     |
| Safari        | 13+     | ✅     | ✅     | Full feature support     |
| Edge          | 80+     | ✅     | ✅     | Full feature support     |
| Mobile Safari | 13+     | ✅     | ⚠️     | Limited batch processing |
| Chrome Mobile | 80+     | ✅     | ✅     | Full feature support     |

### Progressive Enhancement

```javascript
// Feature detection and fallbacks
const checkBrowserSupport = () => {
  const support = {
    fetch: typeof fetch !== "undefined",
    localStorage: typeof Storage !== "undefined",
    modules: "noModule" in HTMLScriptElement.prototype,
    asyncAwait: (function () {
      try {
        return eval("(async function() {})").constructor;
      } catch (e) {
        return false;
      }
    })(),
  };

  if (!support.fetch) {
    // Fallback to XMLHttpRequest
    loadFetchPolyfill();
  }

  return support;
};
```

### Mobile Responsiveness

- **Touch-friendly** interface with appropriate button sizes
- **Swipe gestures** for navigation (where applicable)
- **Viewport optimization** for different screen sizes
- **Performance optimization** for mobile devices

## 🔧 Development Setup

### Local Development

```powershell
# Clone and setup
git clone <repository>
cd HackRX

# Install Python dependencies (if not done)
pip install -r requirements.txt

# Start development server
python main.py

# Frontend will be available at:
# - Main Interface: http://localhost:3000
# - API Guide: http://localhost:8000/api_guide
# - API Docs: http://localhost:8000/docs
```

### Production Deployment

```bash
# Build static assets (if using build process)
npm run build  # If using npm for asset processing

# Or simply copy HTML files to web server
cp Frontend/*.html /var/www/html/
cp templates/*.html /var/www/html/templates/

# Update API URLs for production
sed -i 's/localhost:8000/your-api-domain.com/g' *.html
```

### Environment Configuration

```javascript
// Environment-specific configuration
const config = {
  development: {
    apiUrl: "http://localhost:8000",
    debugMode: true,
    logLevel: "debug",
  },
  production: {
    apiUrl: "https://api.yourdomain.com",
    debugMode: false,
    logLevel: "error",
  },
};

const currentConfig = config[process.env.NODE_ENV] || config.development;
```

## 🧪 Testing

### Manual Testing Checklist

- [ ] V1 API single document processing
- [ ] V2 API batch document processing
- [ ] API version switching functionality
- [ ] Error handling for network issues
- [ ] Mobile responsiveness
- [ ] Cross-browser compatibility
- [ ] Authentication flow
- [ ] Export functionality

### Automated Testing

```javascript
// Simple test runner for frontend functionality
const runTests = async () => {
  const tests = [
    testApiConnection,
    testV1Processing,
    testV2BatchProcessing,
    testErrorHandling,
    testLocalStorage,
    testExportFunctionality,
  ];

  for (const test of tests) {
    try {
      await test();
      console.log(`✅ ${test.name} passed`);
    } catch (error) {
      console.error(`❌ ${test.name} failed:`, error);
    }
  }
};
```

## 🚀 Deployment Options

### Static Hosting (Recommended)

- **Netlify**: Drag and drop deployment
- **Vercel**: Git-based deployment
- **GitHub Pages**: Free hosting for public repositories
- **AWS S3**: Scalable static hosting

### Integration with Backend

```javascript
// Dynamic API endpoint discovery
const discoverApiEndpoints = async () => {
  try {
    const response = await fetch("/api/v1/");
    const apiInfo = await response.json();

    // Update available endpoints based on API response
    updateAvailableEndpoints(apiInfo.available_endpoints);
  } catch (error) {
    console.warn("API endpoint discovery failed, using defaults");
  }
};
```

## 📚 Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Modern JavaScript Guide**: https://javascript.info/
- **CSS Grid Guide**: https://css-tricks.com/snippets/css/complete-guide-grid/
- **Web Accessibility**: https://web.dev/accessibility/

## 🔒 Security Considerations

- **API Key Management**: Never expose production API keys in frontend code
- **CORS Configuration**: Ensure backend CORS settings allow frontend domain
- **Input Validation**: Sanitize user inputs before sending to API
- **Error Messages**: Don't expose sensitive information in error messages

---

**🎨 Frontend Component of the HackRX Project - V2 Enhanced**
