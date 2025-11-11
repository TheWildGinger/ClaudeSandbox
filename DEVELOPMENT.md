# EngiCalc Development Guide

## Quick Start for Developers

### Prerequisites

- Python 3.10+
- Node.js 18+
- Poetry (Python package manager)
- Pandoc (optional, for PDF export)

### First-Time Setup

1. **Clone and navigate to the project**
   ```bash
   git clone <repo-url>
   cd ClaudeSandbox
   ```

2. **Backend setup**
   ```bash
   cd backend
   poetry install
   cp .env.example .env
   ```

3. **Frontend setup**
   ```bash
   cd ../frontend
   npm install
   ```

### Running in Development Mode

**Terminal 1 - Backend:**
```bash
cd backend
poetry run python -m app.main
# Server runs on http://localhost:8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
# Server runs on http://localhost:5173
```

**Access:** http://localhost:5173

## Project Structure

### Backend (`/backend`)

```
backend/
├── app/
│   ├── api/              # API endpoints
│   │   ├── calculation.py    # Calculation execution
│   │   ├── document.py       # Document CRUD
│   │   ├── export.py         # PDF/HTML export
│   │   └── template.py       # Template management
│   ├── core/             # Configuration and utilities
│   │   └── config.py
│   ├── models/           # Pydantic models
│   │   ├── calculation.py
│   │   ├── document.py
│   │   └── template.py
│   ├── services/         # Business logic
│   │   ├── calculation_engine.py    # Core calculation engine
│   │   ├── document_service.py
│   │   ├── export_service.py
│   │   └── template_service.py
│   └── main.py           # FastAPI application
├── tests/
└── pyproject.toml
```

### Frontend (`/frontend`)

```
frontend/
├── src/
│   ├── components/
│   │   ├── Editor.tsx        # Monaco editor wrapper
│   │   ├── Preview.tsx       # Markdown + calculation preview
│   │   ├── Sidebar.tsx       # Document/template browser
│   │   └── Toolbar.tsx       # Top toolbar with actions
│   ├── services/
│   │   └── api.ts            # API client (axios)
│   ├── stores/
│   │   └── documentStore.ts  # Zustand state management
│   ├── types/
│   │   └── index.ts          # TypeScript definitions
│   ├── styles/
│   │   └── index.css         # Global styles + Tailwind
│   ├── App.tsx
│   └── main.tsx
├── package.json
├── vite.config.ts
└── tsconfig.json
```

## Key Technologies

### Backend Stack

- **FastAPI**: Modern, fast web framework with automatic OpenAPI docs
- **Pint**: Unit-aware calculations (e.g., `5 * ureg.meter`)
- **Handcalcs**: Converts Python calculations to LaTeX equations
- **python-frontmatter**: YAML frontmatter parsing
- **Pandoc**: External tool for PDF generation

### Frontend Stack

- **React 18**: UI framework
- **TypeScript**: Type safety
- **Vite**: Fast build tool and dev server
- **Monaco Editor**: VS Code editor component
- **React-Markdown**: Markdown rendering with plugins
- **KaTeX**: Fast math rendering (LaTeX)
- **Zustand**: Lightweight state management
- **Axios**: HTTP client
- **Tailwind CSS**: Utility-first CSS

## Development Workflows

### Adding a New API Endpoint

1. **Define the model** in `backend/app/models/`
   ```python
   class MyRequest(BaseModel):
       field: str
   ```

2. **Create the service logic** in `backend/app/services/`
   ```python
   class MyService:
       def do_something(self, input: str) -> str:
           return input.upper()
   ```

3. **Add the API route** in `backend/app/api/`
   ```python
   @router.post("/my-endpoint")
   async def my_endpoint(request: MyRequest):
       result = my_service.do_something(request.field)
       return {"result": result}
   ```

4. **Register the router** in `backend/app/main.py`
   ```python
   app.include_router(my_router, prefix="/api/my", tags=["my"])
   ```

5. **Add TypeScript types** in `frontend/src/types/index.ts`
   ```typescript
   export interface MyRequest {
       field: string
   }
   ```

6. **Add API client method** in `frontend/src/services/api.ts`
   ```typescript
   export const myApi = {
       doSomething: async (field: string) => {
           const response = await api.post('/my/my-endpoint', { field })
           return response.data
       }
   }
   ```

### Adding a New React Component

1. Create component in `frontend/src/components/MyComponent.tsx`
2. Import and use in parent component
3. Add types if needed in `types/index.ts`
4. Style with Tailwind CSS classes

### Modifying the Calculation Engine

The calculation engine is in `backend/app/services/calculation_engine.py`.

**Key methods:**
- `create_execution_namespace()`: Sets up Python execution environment
- `execute_block()`: Executes a single calculation block
- `_try_generate_latex()`: Attempts to generate LaTeX with handcalcs

**To add new functionality:**
```python
def execute_block(self, block: CalculationBlock, context: Dict[str, Any]):
    namespace = self.create_execution_namespace(context)

    # Add your custom logic here

    exec(block.code, namespace)
    # ... rest of execution
```

## Testing

### Backend Tests

```bash
cd backend
poetry run pytest
```

**Writing tests:**
```python
# backend/tests/test_calculation.py
import pytest
from app.services.calculation_engine import calculation_engine

def test_basic_calculation():
    block = CalculationBlock(code="result = 5 * 3")
    result = calculation_engine.execute_block(block, {})
    assert result.success
    assert result.result['result'] == 15
```

### Frontend Tests (TBD)

```bash
cd frontend
npm test
```

## API Documentation

With the backend running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These provide interactive API documentation.

## Common Tasks

### Add a New Template

1. Create a markdown file in `templates/`
2. Add YAML frontmatter with metadata:
   ```yaml
   ---
   name: "Template Name"
   description: "What it does"
   category: "Category"
   variables: ["var1", "var2"]
   ---
   ```
3. Write template content with `{{variable}}` placeholders
4. Restart backend (it scans templates on startup)

### Modify PDF Export

Edit `backend/app/services/export_service.py`:

```python
def export_to_pdf(self, markdown_content: str, output_filename: str):
    # Modify pandoc_cmd list to add options
    pandoc_cmd = [
        settings.PANDOC_PATH,
        str(temp_md_path),
        "-o", str(output_path),
        "--pdf-engine=xelatex",  # Change engine
        "-V", "geometry:margin=1.5in",  # Change margins
        # ... add more options
    ]
```

### Add Unit Support

Units are provided by Pint. To add custom units:

```python
# backend/app/services/calculation_engine.py
def __init__(self):
    self.ureg = ureg
    # Add custom units
    self.ureg.define('custom_unit = 1.5 * meter')
```

## Environment Variables

Copy `backend/.env.example` to `backend/.env` and configure:

```env
# Development
DEBUG=True

# Production
DEBUG=False
CORS_ORIGINS=["https://yourdomain.com"]
```

## Code Style

### Python

- **Formatter**: Black (line length 100)
- **Linter**: Ruff
- **Type hints**: Required for public functions

```bash
cd backend
poetry run black app/
poetry run ruff app/
poetry run mypy app/
```

### TypeScript

- **Formatter**: Prettier
- **Linter**: ESLint
- **Style**: Functional components, hooks

```bash
cd frontend
npm run format
npm run lint
```

## Performance Considerations

### Backend

- Calculation timeout: 30 seconds (configurable in `.env`)
- No sandboxing in MVP (trust user code)
- Future: Add timeout per calculation, memory limits

### Frontend

- Monaco editor: Lazy loaded
- Math rendering: KaTeX is fast (~10x faster than MathJax)
- Debounce calculation execution on edit (300ms recommended)

## Security Notes

### MVP Security Posture

- **Code execution**: User code runs with full Python access (LOCAL USE ONLY)
- **File system**: Limited to `documents/`, `templates/`, `exports/` directories
- **No authentication**: Single-user desktop application

### Future Security (for multi-user)

- Add RestrictedPython for code execution
- Add user authentication/authorization
- Sandbox file system access
- Rate limiting on API endpoints

## Debugging Tips

### Backend Debugging

1. **Enable debug logging:**
   ```python
   # app/main.py
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Use FastAPI's automatic docs:**
   Visit http://localhost:8000/docs to test endpoints

3. **Python debugger:**
   ```python
   import pdb; pdb.set_trace()
   ```

### Frontend Debugging

1. **React DevTools**: Install browser extension
2. **Console logging**: Check browser console
3. **Network tab**: Inspect API calls
4. **Vite HMR**: Hot module replacement for fast iteration

## Deployment (Future)

### Desktop Application

Package with PyWebView:
```python
import webview
webview.create_window('EngiCalc', 'http://localhost:8000')
webview.start()
```

Or Tauri (Rust-based, smaller):
```bash
npm install -g @tauri-apps/cli
tauri init
tauri build
```

### Web Application

- Backend: Deploy with Docker/Gunicorn
- Frontend: Build and serve static files
- Requires authentication for multi-user

## Contributing Guidelines

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make changes with clear commit messages
4. Add tests for new functionality
5. Ensure code passes linting: `black`, `ruff`, `eslint`
6. Submit pull request with description

## Roadmap

### Phase 1: MVP ✅
- Basic editor and preview
- Python calculations with units
- PDF export
- Template system

### Phase 2: Enhanced Features
- Desktop packaging
- Figure auto-numbering
- Cross-references
- Table of contents
- Search functionality

### Phase 3: AI Integration
- LLM-assisted calculation writing
- Natural language to code
- Automatic validation
- Smart templates

## Getting Help

- **API Docs**: http://localhost:8000/docs
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions

## License

MIT License - see LICENSE file
