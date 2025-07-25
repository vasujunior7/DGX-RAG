# 🎨 Templates

This directory contains HTML templates for the web interface of the HackRX API.

## 📁 Structure

```
templates/
└── api_guide.html           # Main API documentation page
```

## 🚀 Components

### `api_guide.html`

- **Interactive API documentation** served at the root path (`/`)
- **Beautiful, responsive design** with modern CSS
- **Complete endpoint documentation** with examples
- **Quick start guide** for developers

## 🌟 Features

### 🎨 Design Elements

- **Modern Gradient Background** - Eye-catching visual design
- **Responsive Layout** - Works on desktop, tablet, and mobile
- **Card-Based Interface** - Easy-to-read sections
- **Interactive Elements** - Hover effects and animations
- **Professional Typography** - Clean, readable fonts

### 📋 Content Sections

1. **API Overview**

   - Framework information (FastAPI)
   - Key features and capabilities
   - Status indicators

2. **Endpoint Documentation**

   - All available API endpoints
   - HTTP methods with color-coded badges
   - Request/response examples
   - Detailed descriptions

3. **Quick Start Guide**

   - curl examples
   - Python requests examples
   - Copy-friendly code blocks

4. **Interactive Links**
   - Direct links to Swagger UI (`/docs`)
   - Links to ReDoc (`/redoc`)
   - Navigation to other endpoints

### 🔧 Technical Implementation

- **Template Engine**: Jinja2
- **CSS Framework**: Custom CSS with modern features
- **JavaScript**: Vanilla JS for interactivity
- **Responsive Design**: CSS Grid and Flexbox
- **Font Family**: Arial with fallbacks

## 🎯 Endpoint Documentation

The template documents all API endpoints:

### Documented Endpoints

| Method | Endpoint             | Description              |
| ------ | -------------------- | ------------------------ |
| `GET`  | `/`                  | API guide (this page)    |
| `GET`  | `/help`              | Basic API information    |
| `GET`  | `/api/v1/`           | V1 welcome message       |
| `POST` | `/api/v1/hackrx/run` | Main document processing |

### Code Examples

The template includes working examples:

```bash
# curl example
curl -X POST "http://localhost:8000/api/v1/hackrx/run" \
     -H "Content-Type: application/json" \
     -d '{"documents": "...", "questions": [...]}'
```

```python
# Python example
import requests
response = requests.post("http://localhost:8000/api/v1/hackrx/run", json=data)
```

## 🔧 Template Usage

### Rendering in FastAPI

```python
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("api_guide.html", {"request": request})
```

### Template Variables

The template uses these variables:

- `request` - FastAPI request object (required by Jinja2)
- Additional variables can be passed in the context dictionary

## 🎨 Styling

### Color Scheme

- **Primary**: Blue gradient (`#667eea` to `#764ba2`)
- **Secondary**: Dark blue (`#2c3e50`, `#3498db`)
- **Success**: Green (`#28a745`)
- **Info**: Light blue (`#007bff`)
- **Background**: White with subtle shadows

### Typography

- **Headers**: Clean, modern sans-serif
- **Body**: Readable Arial with good line spacing
- **Code**: Monospace font (`Courier New`)

### Layout

- **Container**: Centered with max-width for readability
- **Grid**: CSS Grid for responsive card layouts
- **Cards**: Elevated design with subtle shadows
- **Spacing**: Consistent margins and padding

## 🔄 Customization

### Adding New Sections

1. **Add HTML structure**:

```html
<div class="section">
  <h2>🆕 New Section</h2>
  <p>Your content here</p>
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
