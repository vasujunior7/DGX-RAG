# 🎨 Templates

This directory contains HTML templates and interactive documentation for the HackRX API, featuring comprehensive V1 and V2 API support with enhanced user experience.

## 📁 Structure

```
templates/
├── api_guide.html           # Comprehensive V1/V2 API documentation
├── index.html              # Alternative main interface (if used)
├── components/             # Reusable template components (if any)
└── README.md              # This documentation
```

## 🚀 Components

### `api_guide.html` (V2 Enhanced)

- **Interactive V1/V2 API documentation** served at the root path (`/`)
- **Beautiful, responsive design** with modern CSS and animations
- **Complete endpoint documentation** with live examples and testing
- **V2 features**: API version switching, batch processing demos, metadata display
- **Developer-friendly interface** with copy-to-clipboard functionality

## 🌟 Enhanced Features

### 🎨 Design Elements (V2 Upgraded)

- **Modern Gradient Background** - Enhanced visual design with V2 branding
- **Responsive Layout** - Optimized for desktop, tablet, mobile, and ultra-wide screens
- **Card-Based Interface** - Improved sectioning with V1/V2 differentiation
- **Interactive Elements** - Enhanced hover effects, animations, and transitions
- **Professional Typography** - Upgraded fonts with better readability
- **Dark/Light Mode** - **NEW V2**: Theme switching capability
- **Loading Animations** - **NEW V2**: Smooth loading states for API calls

### 📋 Enhanced Content Sections

1. **API Overview (V2 Enhanced)**

   - Framework information (FastAPI with V1/V2 support)
   - **NEW**: API version comparison table
   - **NEW**: Feature availability matrix
   - Enhanced status indicators with real-time health checks
   - **NEW**: Performance metrics display

2. **V1 API Documentation**

   - Traditional single-document processing
   - Standard request/response examples
   - Backward compatibility information
   - Migration guide to V2

3. **V2 API Documentation (NEW)**

   - **Batch Processing**: Multiple document handling
   - **Enhanced Responses**: Metadata and source attribution
   - **Processing Options**: Configurable parameters
   - **Parallel Processing**: Concurrent operation examples
   - **Advanced Features**: Custom processing workflows

4. **Interactive API Testing (V2 Feature)**

   - **Live API Testing**: Direct API calls from the interface
   - **Version Switching**: Toggle between V1 and V2 endpoints
   - **Request Builder**: Visual request construction
   - **Response Viewer**: Formatted response display with syntax highlighting
   - **History Tracking**: Previous request/response history

5. **Code Examples (Enhanced)**
   - **Multi-language support**: curl, Python, JavaScript, PowerShell
   - **Version-specific examples**: Separate V1 and V2 code samples
   - **Interactive code blocks**: Click-to-copy functionality
   - **Live examples**: Working examples with real API calls

### 🔧 Technical Implementation (V2 Enhanced)

- **Template Engine**: Jinja2 with enhanced context support
- **CSS Framework**: Custom CSS with CSS Grid, Flexbox, and CSS Variables
- **JavaScript**: Modern ES6+ for enhanced interactivity
- **API Integration**: Direct integration with V1/V2 endpoints
- **Real-time Updates**: WebSocket support for live status updates (planned)
- **Performance**: Optimized loading with lazy loading and caching

## 🎯 Comprehensive Endpoint Documentation

### V1 API Endpoints (Documented)

| Method | Endpoint              | Description                           | Status    |
| ------ | --------------------- | ------------------------------------- | --------- |
| `GET`  | `/`                   | Enhanced API guide with V1/V2 support | ✅ Active |
| `GET`  | `/help`               | Basic API information                 | ✅ Active |
| `GET`  | `/api/v1/`            | V1 welcome message and status         | ✅ Active |
| `GET`  | `/api/v1/auth/status` | V1 authentication status              | ✅ Active |
| `POST` | `/api/v1/hackrx/run`  | V1 document processing                | ✅ Active |

### V2 API Endpoints (NEW - Documented)

| Method | Endpoint                  | Description                   | V2 Features                 |
| ------ | ------------------------- | ----------------------------- | --------------------------- |
| `GET`  | `/api/v2/`                | V2 welcome with enhanced info | ✅ Metadata, Status         |
| `GET`  | `/api/v2/auth/status`     | V2 enhanced authentication    | ✅ Permissions, Limits      |
| `POST` | `/api/v2/hackrx/run`      | V2 batch document processing  | ✅ Batch, Metadata, Sources |
| `GET`  | `/api/v2/hackrx/metadata` | Processing metadata endpoint  | ✅ Analytics, Performance   |

### Interactive Code Examples (V2 Enhanced)

#### V1 API Example

```bash
# V1 curl example (traditional)
curl -X POST "http://localhost:8000/api/v1/hackrx/run" \
     -H "Authorization: Bearer hackrx_2025_dev_key_123456789" \
     -H "Content-Type: application/json" \
     -d '{
       "documents": "sample.pdf",
       "questions": ["What is this document about?"]
     }'
```

#### V2 API Example (NEW)

```bash
# V2 curl example (enhanced with batch processing)
curl -X POST "http://localhost:8000/api/v2/hackrx/run" \
     -H "Authorization: Bearer hackrx_2025_dev_key_123456789" \
     -H "Content-Type: application/json" \
     -d '{
       "documents": ["doc1.pdf", "doc2.docx", "doc3.txt"],
       "questions": [
         "What are the main themes across all documents?",
         "How do these documents relate to each other?"
       ],
       "options": {
         "include_metadata": true,
         "include_sources": true,
         "max_length": 200,
         "parallel_processing": true
       }
     }'
```

#### Python Examples (V2 Enhanced)

```python
# V2 Python example with enhanced features
import requests

# V2 API call with batch processing
response = requests.post(
    "http://localhost:8000/api/v2/hackrx/run",
    headers={
        "Authorization": "Bearer hackrx_2025_dev_key_123456789",
        "Content-Type": "application/json"
    },
    json={
        "documents": ["doc1.pdf", "doc2.pdf"],
        "questions": ["Analyze the key points"],
        "options": {
            "include_metadata": True,
            "temperature": 0.7
        }
    }
)

# V2 response with enhanced data
result = response.json()
print("Answers:", result["answers"])
print("Sources:", result["sources"])
print("Metadata:", result["metadata"])
```

## 🔧 Enhanced Template Usage

### V2 Template Rendering in FastAPI

```python
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def api_guide(request: Request):
    """Enhanced API guide with V1/V2 support"""
    context = {
        "request": request,
        "api_versions": ["v1", "v2"],
        "current_version": "v2",
        "features": {
            "v1": ["single_document", "basic_processing"],
            "v2": ["batch_processing", "metadata", "enhanced_responses", "parallel_processing"]
        },
        "status": {
            "server": "running",
            "database": "connected",
            "ai_model": "available"
        }
    }
    return templates.TemplateResponse("api_guide.html", context)

@app.get("/api_guide", response_class=HTMLResponse)
def api_guide_alt(request: Request):
    """Alternative API guide endpoint"""
    return templates.TemplateResponse("api_guide.html", {"request": request})
```

### Enhanced Template Variables (V2)

The V2 template supports these enhanced variables:

```python
template_context = {
    "request": request,                    # FastAPI request object (required)
    "api_versions": ["v1", "v2"],         # Available API versions
    "current_version": "v2",              # Default API version
    "features": {                         # Version-specific features
        "v1": ["single_document", "basic_processing"],
        "v2": ["batch_processing", "metadata", "sources", "parallel_processing"]
    },
    "endpoints": {                        # Dynamic endpoint discovery
        "v1": ["/api/v1/", "/api/v1/hackrx/run"],
        "v2": ["/api/v2/", "/api/v2/hackrx/run", "/api/v2/hackrx/metadata"]
    },
    "status": {                          # Real-time status information
        "server": "running",
        "database": "connected",
        "ai_model": "available",
        "cache": "active"
    },
    "metrics": {                         # Performance metrics (V2 feature)
        "requests_today": 1234,
        "avg_response_time": 2.3,
        "uptime": "99.9%"
    }
}
```

## 🎨 Enhanced Styling (V2)

### V2 Color Scheme

```css
:root {
  /* V2 Enhanced Color Palette */
  --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --secondary-gradient: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
  --success-color: #28a745;
  --info-color: #007bff;
  --warning-color: #ffc107;
  --error-color: #dc3545;
  --background: #f8f9fa;
  --surface: #ffffff;
  --text-primary: #2c3e50;
  --text-secondary: #6c757d;
  --border-color: #dee2e6;

  /* V2 Dark Mode Support */
  --dark-background: #1a1a1a;
  --dark-surface: #2d2d2d;
  --dark-text-primary: #ffffff;
  --dark-text-secondary: #b0b0b0;
}
```

### Enhanced Typography (V2)

```css
/* V2 Typography System */
.typography-system {
  --font-family-primary: "Inter", "Segoe UI", "Roboto", sans-serif;
  --font-family-mono: "JetBrains Mono", "Fira Code", "Courier New", monospace;

  --font-size-xs: 0.75rem; /* 12px */
  --font-size-sm: 0.875rem; /* 14px */
  --font-size-base: 1rem; /* 16px */
  --font-size-lg: 1.125rem; /* 18px */
  --font-size-xl: 1.25rem; /* 20px */
  --font-size-2xl: 1.5rem; /* 24px */
  --font-size-3xl: 1.875rem; /* 30px */
  --font-size-4xl: 2.25rem; /* 36px */
}
```

### Responsive Layout (V2 Enhanced)

```css
/* V2 Responsive Grid System */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.grid {
  display: grid;
  gap: 1.5rem;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}

/* Enhanced Breakpoints */
@media (max-width: 480px) {
  .grid {
    grid-template-columns: 1fr;
  }
}

@media (min-width: 768px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 1440px) {
  .grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

## 🔄 V2 Customization Guide

### Adding New V2 Sections

1. **Add HTML Structure with V2 Features**:

```html
<div class="api-section" data-version="v2">
  <div class="section-header">
    <h2>🆕 V2 New Feature</h2>
    <span class="version-badge v2">V2 Only</span>
  </div>
  <div class="feature-content">
    <p>Your V2 enhanced content here</p>
    <div class="code-example">
      <button class="copy-btn" onclick="copyCode(this)">📋 Copy</button>
      <pre><code>// V2 example code</code></pre>
    </div>
  </div>
</div>
```

2. **Add Corresponding CSS**:

```css
.api-section[data-version="v2"] {
  border-left: 4px solid var(--info-color);
  background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
}

.version-badge.v2 {
  background: var(--info-color);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: bold;
}
```

### API Version Switching (V2 Feature)

```html
<!-- API Version Selector -->
<div class="version-selector">
  <label>Choose API Version:</label>
  <select id="apiVersionSelector" onchange="switchApiVersion(this.value)">
    <option value="v1">API v1 (Stable)</option>
    <option value="v2" selected>API v2 (Enhanced)</option>
  </select>
</div>

<script>
  function switchApiVersion(version) {
    // Hide/show version-specific content
    document.querySelectorAll("[data-version]").forEach((el) => {
      el.style.display = el.dataset.version === version ? "block" : "none";
    });

    // Update code examples
    updateCodeExamples(version);

    // Update endpoint URLs
    updateEndpointUrls(version);
  }

  function updateCodeExamples(version) {
    const baseUrl =
      version === "v2"
        ? "http://localhost:8000/api/v2"
        : "http://localhost:8000/api/v1";

    document.querySelectorAll(".endpoint-url").forEach((el) => {
      el.textContent = el.textContent.replace(
        /\/api\/v[12]/,
        `/api/${version}`
      );
    });
  }
</script>
```

### Interactive API Testing (V2 Feature)

```html
<!-- Interactive API Tester -->
<div class="api-tester" data-version="v2">
  <h3>🧪 Live API Testing</h3>
  <form id="apiTestForm">
    <div class="form-group">
      <label>API Version:</label>
      <select name="version">
        <option value="v1">v1</option>
        <option value="v2" selected>v2</option>
      </select>
    </div>

    <div class="form-group">
      <label>Documents (V2: comma-separated):</label>
      <input type="text" name="documents" placeholder="doc1.pdf, doc2.txt" />
    </div>

    <div class="form-group">
      <label>Questions (one per line):</label>
      <textarea
        name="questions"
        rows="3"
        placeholder="What is the main topic?
Who are the authors?"
      ></textarea>
    </div>

    <div class="form-group v2-only">
      <label>V2 Options:</label>
      <div class="checkbox-group">
        <label
          ><input type="checkbox" name="include_metadata" checked /> Include
          Metadata</label
        >
        <label
          ><input type="checkbox" name="include_sources" checked /> Include
          Sources</label
        >
        <label
          ><input type="checkbox" name="parallel_processing" /> Parallel
          Processing</label
        >
      </div>
    </div>

    <button type="submit">🚀 Test API</button>
  </form>

  <div id="apiResponse" class="response-display"></div>
</div>

<script>
  document
    .getElementById("apiTestForm")
    .addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData(e.target);
      const version = formData.get("version");

      // Build request based on API version
      const payload = {
        documents:
          version === "v2"
            ? formData
                .get("documents")
                .split(",")
                .map((s) => s.trim())
            : formData.get("documents").trim(),
        questions: formData
          .get("questions")
          .split("\n")
          .filter((q) => q.trim()),
      };

      if (version === "v2") {
        payload.options = {
          include_metadata: formData.get("include_metadata") === "on",
          include_sources: formData.get("include_sources") === "on",
          parallel_processing: formData.get("parallel_processing") === "on",
        };
      }

      // Make API call
      try {
        const response = await fetch(`/api/${version}/hackrx/run`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer hackrx_2025_dev_key_123456789",
          },
          body: JSON.stringify(payload),
        });

        const result = await response.json();
        document.getElementById(
          "apiResponse"
        ).innerHTML = `<pre><code>${JSON.stringify(
          result,
          null,
          2
        )}</code></pre>`;
      } catch (error) {
        document.getElementById(
          "apiResponse"
        ).innerHTML = `<div class="error">Error: ${error.message}</div>`;
      }
    });
</script>
```

## 📊 Template Performance (V2)

### Loading Optimization

- **Lazy Loading**: Images and heavy content loaded on demand
- **CSS Minification**: Compressed stylesheets for faster loading
- **JavaScript Bundling**: Optimized script loading
- **CDN Support**: Ready for CDN deployment
- **Caching Headers**: Proper cache control for static assets

### Accessibility (WCAG 2.1 Compliant)

- **Semantic HTML**: Proper heading structure and landmarks
- **Keyboard Navigation**: Full keyboard accessibility
- **Screen Reader Support**: ARIA labels and descriptions
- **Color Contrast**: WCAG AA compliant color combinations
- **Focus Management**: Visible focus indicators

### Browser Support

- **Modern Browsers**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Progressive Enhancement**: Graceful degradation for older browsers
- **Mobile Optimization**: Touch-friendly interface
- **Print Styles**: Optimized for printing

---

**🎨 Enhanced Template System for HackRX V2 API Documentation**

</div>
```

2. **Add corresponding CSS** (if needed):

```css
.new-section {
  /* Your styles */
}
```

### Modifying Endpoints

Update the endpoint documentation section:

```html
<div class="endpoint">
  <h3>
    <span class="method post">POST</span>
    <span class="url">/api/v1/new-endpoint</span>
  </h3>
  <div class="description">Description of your new endpoint</div>
</div>
```

### Changing Colors

Modify the CSS variables:

```css
:root {
  --primary-color: #your-color;
  --secondary-color: #your-color;
  --accent-color: #your-color;
}
```

## 📱 Responsive Design

The template is fully responsive:

### Breakpoints

- **Desktop**: > 1200px (full layout)
- **Tablet**: 768px - 1200px (adjusted grid)
- **Mobile**: < 768px (stacked layout)

### Mobile Features

- **Touch-friendly**: Large clickable areas
- **Readable text**: Appropriate font sizes
- **Optimized spacing**: Comfortable touch targets
- **Horizontal scrolling**: For code examples

## 🧪 Testing the Template

### Local Testing

1. **Start the server**:

   ```bash
   python main.py
   ```

2. **Visit the page**:
   - Open http://localhost:8000/
   - Check responsive design by resizing window
   - Test all links and interactive elements

### Browser Compatibility

- **Chrome**: Full support
- **Firefox**: Full support
- **Safari**: Full support
- **Edge**: Full support
- **Mobile browsers**: Optimized for mobile

## 🔧 Performance

### Optimization Features

- **Inline CSS**: No external CSS files to load
- **Inline JavaScript**: Minimal JS for interactivity
- **Optimized Images**: No heavy images used
- **Clean HTML**: Semantic, efficient markup

### Loading Speed

- **Fast rendering**: All assets inline
- **Small file size**: ~11KB HTML file
- **No dependencies**: No external libraries

## 📋 Maintenance

### Updating Documentation

When adding new API endpoints:

1. **Update endpoint sections** in the HTML
2. **Add examples** for new endpoints
3. **Update quick start guide** if needed
4. **Test all links** and examples

### Content Updates

- **Version numbers**: Update in header and footer
- **API information**: Keep descriptions current
- **Examples**: Ensure examples work with current API
- **Links**: Verify all internal/external links

---

**Web Interface Templates for the HackRX API**
