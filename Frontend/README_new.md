# HackRX Frontend

## Overview

Simple HTML/CSS/JavaScript frontend for the HackRX Document Processing Platform. This provides a clean, modern interface to interact with the FastAPI backend without the complexity of React or other frameworks.

## Features

- **Pure HTML/CSS/JS** - No build process required
- **Modern UI Design** - Glass morphism effects and responsive layout
- **API Integration** - Direct integration with FastAPI backend
- **Document Processing** - Upload documents and ask questions
- **Real-time Status** - API status monitoring
- **Local Storage** - Processing history saved locally
- **Export Results** - Download results as JSON

## Quick Start

### Run with main.py (Recommended)

```bash
# From the main project directory
python main.py
```

This will start both the FastAPI backend (port 8000) and serve the HTML frontend (port 3000).

### Open HTML directly

```bash
# Just open the HTML file in your browser
start index.html
```

Note: You'll need to manually start the backend server and update the API URL in the HTML file.

## File Structure

```
Frontend/
├── index.html          # Main application interface
└── README.md          # This file
```

## API Integration

The frontend communicates with these backend endpoints:

- `GET /api/v1/` - API status check
- `POST /api/v1/hackrx/run` - Document processing
- `GET /docs` - FastAPI documentation
- `GET /redoc` - Alternative API documentation

## Customization

### Update API Base URL

Edit the `baseUrl` variable in index.html:

```javascript
const baseUrl = "http://localhost:8000"; // Change this if needed
```

### Modify Styling

All CSS is embedded in the HTML file for simplicity. Look for the `<style>` section to customize colors, layout, and animations.

## Browser Compatibility

Works on all modern browsers including Chrome, Firefox, Safari, and Edge. Mobile responsive design included.

## No Dependencies

This frontend has zero external dependencies and requires no build process. Simply edit the HTML file and refresh your browser.
