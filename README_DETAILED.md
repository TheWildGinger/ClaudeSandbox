# EngiCalc - Engineering Calculation Tool

A modern, Python-powered engineering calculation and documentation tool designed to replace tools like MathCAD with a better, more flexible workflow.

## Overview

EngiCalc combines the power of Python calculations with beautiful markdown-based documentation, live math rendering, and professional PDF export capabilities.

### Key Features

- **Markdown-Based Documents**: Write calculations in familiar markdown format
- **Python Calculation Engine**: Execute Python code with full unit support (Pint library)
- **Live Preview**: See your calculations and results update in real-time
- **Math Rendering**: Beautiful equation rendering with KaTeX
- **PDF Export**: Generate professional PDF documents with Pandoc
- **Template System**: Reusable calculation templates for common tasks
- **Unit-Aware**: Automatic unit conversion and validation
- **LLM-Ready**: Architecture designed for future AI assistant integration

## Architecture

```
┌─────────────────────────────────────┐
│   Frontend (React + TypeScript)     │
│   - Monaco Editor                   │
│   - Live Preview with KaTeX         │
│   - Template Browser                │
└─────────────────────────────────────┘
                 │
                 │ REST API + WebSocket
                 ▼
┌─────────────────────────────────────┐
│   Backend (FastAPI + Python)        │
│   - Calculation Engine (Pint)       │
│   - Document Manager                │
│   - Export Engine (Pandoc)          │
│   - Template Manager                │
└─────────────────────────────────────┘
                 │
                 ▼
        ┌───────────────┐
        │  File System  │
        │  - Documents  │
        │  - Templates  │
        │  - Exports    │
        └───────────────┘
```

## Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework
- **Python 3.10+**: Calculation engine
- **Pint**: Unit-aware calculations
- **Handcalcs**: LaTeX equation rendering
- **Pandoc**: PDF export (external dependency)

### Frontend
- **React 18**: UI framework
- **TypeScript**: Type-safe development
- **Vite**: Fast build tool
- **Monaco Editor**: VS Code editor component
- **KaTeX**: Fast math rendering
- **Zustand**: Lightweight state management

## Installation

### Prerequisites

1. **Python 3.10+**
   ```bash
   python --version  # Should be 3.10 or higher
   ```

2. **Node.js 18+**
   ```bash
   node --version  # Should be 18 or higher
   ```

3. **Poetry** (Python dependency manager)
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

4. **Pandoc** (for PDF export - optional but recommended)
   - **Ubuntu/Debian**: `sudo apt-get install pandoc texlive-latex-base texlive-latex-extra`
   - **macOS**: `brew install pandoc basictex`
   - **Windows**: Download from https://pandoc.org/installing.html

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ClaudeSandbox
   ```

2. **Install backend dependencies**
   ```bash
   cd backend
   poetry install
   ```

3. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   ```

## Running the Application

You need to run both the backend and frontend servers:

### Terminal 1: Backend Server

```bash
cd backend
poetry run python -m app.main
```

The backend will start on `http://localhost:8000`

### Terminal 2: Frontend Development Server

```bash
cd frontend
npm run dev
```

The frontend will start on `http://localhost:5173`

### Access the Application

Open your browser to: **http://localhost:5173**

## Usage

### Creating a New Document

1. Click "New Document" in the sidebar
2. Edit the YAML frontmatter with your project information
3. Write your calculations using markdown and Python code blocks

### Writing Calculations

Use Python code blocks with `%%calc` marker:

````markdown
```python
%%calc
# Define parameters with units
length = 5.0 * ureg.meter
force = 100 * ureg.kN

# Calculate moment
moment = force * length

print(f"Moment: {moment}")
```
````

### Available Units

The `ureg` (unit registry) provides access to all units:

- Length: `ureg.meter`, `ureg.mm`, `ureg.inch`, `ureg.foot`
- Force: `ureg.N`, `ureg.kN`, `ureg.lbf`
- Pressure: `ureg.Pa`, `ureg.MPa`, `ureg.psi`
- And many more...

### Using Templates

1. Click the "Templates" tab in the sidebar
2. Select a template
3. A new document will be created from the template
4. Customize as needed

### Exporting to PDF

1. Ensure your document is saved
2. Click "Export PDF" in the toolbar
3. PDF will be downloaded to your browser

**Note**: PDF export requires Pandoc to be installed.

## Project Structure

```
ClaudeSandbox/
├── backend/
│   ├── app/
│   │   ├── api/              # API route handlers
│   │   │   ├── calculation.py
│   │   │   ├── document.py
│   │   │   ├── export.py
│   │   │   └── template.py
│   │   ├── core/             # Core configuration
│   │   │   └── config.py
│   │   ├── models/           # Data models
│   │   │   ├── calculation.py
│   │   │   ├── document.py
│   │   │   └── template.py
│   │   ├── services/         # Business logic
│   │   │   ├── calculation_engine.py
│   │   │   ├── document_service.py
│   │   │   ├── export_service.py
│   │   │   └── template_service.py
│   │   └── main.py           # FastAPI app entry point
│   ├── tests/
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── Editor.tsx
│   │   │   ├── Preview.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── Toolbar.tsx
│   │   ├── services/         # API client
│   │   │   └── api.ts
│   │   ├── stores/           # State management
│   │   │   └── documentStore.ts
│   │   ├── types/            # TypeScript types
│   │   │   └── index.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
├── documents/                # User documents
├── templates/                # Calculation templates
├── exports/                  # Exported PDFs
└── README.md
```

## API Documentation

When the backend is running, access the interactive API docs at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development

### Backend Development

```bash
cd backend

# Run with auto-reload
poetry run python -m app.main

# Run tests
poetry run pytest

# Format code
poetry run black app/
poetry run ruff app/
```

### Frontend Development

```bash
cd frontend

# Run dev server
npm run dev

# Build for production
npm run build

# Format code
npm run format

# Lint
npm run lint
```

## Future Enhancements

### Phase 2 (Planned)
- Desktop packaging (PyWebView or Tauri)
- Advanced template variable substitution
- Figure/equation auto-numbering and referencing
- Table of contents generation
- WebSocket for live collaboration

### Phase 3 (LLM Integration)
- AI assistant for writing calculations
- Natural language to calculation conversion
- Automatic verification and validation
- Intelligent template suggestions

## Architecture for LLM Integration

The system is designed to support future LLM integration:

### API Endpoints for LLM Agents

```python
# Future endpoints
POST /api/llm/read_document      # Get current document state
POST /api/llm/insert_calculation # Insert calculation block
POST /api/llm/modify_block       # Update existing block
POST /api/llm/execute_validate   # Run and verify results
GET  /api/llm/context            # Get surrounding context
```

### Configuration

```yaml
# config/llm.yaml
providers:
  - name: anthropic
    api_key: ${ANTHROPIC_API_KEY}
    model: claude-sonnet-4
  - name: openai
    api_key: ${OPENAI_API_KEY}
    model: gpt-4
  - name: local
    endpoint: http://localhost:11434/v1
    model: codellama
```

## Troubleshooting

### PDF Export Not Working

**Error**: "Pandoc is not available"

**Solution**: Install Pandoc:
- Ubuntu/Debian: `sudo apt-get install pandoc texlive-latex-base`
- macOS: `brew install pandoc basictex`
- Windows: Download from https://pandoc.org/

### Calculation Errors

**Error**: "name 'ureg' is not defined"

**Solution**: The calculation engine automatically provides `ureg`. Make sure you're using `%%calc` marker in your code block.

### Frontend Not Connecting to Backend

**Error**: API calls failing

**Solution**:
1. Ensure backend is running on port 8000
2. Check browser console for CORS errors
3. Verify proxy settings in `vite.config.ts`

## Contributing

This is currently a personal project, but contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Inspired by MathCAD, SMath, and Jupyter notebooks
- Built with modern web technologies
- Designed for engineering professionals

## Contact

For questions, issues, or suggestions, please open an issue on GitHub.

---

**EngiCalc** - Engineering calculations, done right.
