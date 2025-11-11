# EngiCalc - Engineering Calculation Tool

> A modern, Python-powered engineering calculation and documentation tool. Think MathCAD, but better.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![React](https://img.shields.io/badge/react-18-blue.svg)

## Overview

EngiCalc is a desktop/web application for creating professional engineering calculations with:

- **Live Python Calculations** with automatic unit conversion
- **Beautiful Math Rendering** using KaTeX
- **Professional PDF Export** via Pandoc
- **Markdown-Based Documents** (git-friendly, plain text)
- **Template System** for reusable calculations
- **Future AI Integration** - architecture ready for LLM assistants

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- Poetry (`curl -sSL https://install.python-poetry.org | python3 -`)
- Pandoc (optional, for PDF export)

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd ClaudeSandbox

# Run the development servers
./run-dev.sh        # Linux/Mac
run-dev.bat         # Windows
```

Visit **http://localhost:5173** to use the application.

## Features

### ✨ Write Calculations in Markdown

```markdown
# Beam Analysis

```python
%%calc
# Define parameters with units
L = 5.0 * ureg.meter
w = 10.0 * ureg.kN / ureg.meter

# Calculate maximum moment
M_max = w * L**2 / 8
print(f"Maximum moment: {M_max}")
```
```

### 📐 Unit-Aware Calculations

Powered by Python's Pint library:
- Automatic unit conversion
- Dimensional analysis
- Error prevention (no more adding meters to seconds!)

### 📄 Professional Documentation

- YAML frontmatter for metadata
- Live preview with math rendering
- Export to PDF with one click
- Version control friendly (plain text)

### 🚀 Developer Friendly

- Modern tech stack (FastAPI + React + TypeScript)
- Clean API for future integrations
- Extensible architecture
- Full API documentation at `/docs`

## Example Calculation

```python
%%calc
# Simply supported beam
L = 6.0 * ureg.meter
w = 15.0 * ureg.kN / ureg.meter

# Reactions
R_A = w * L / 2

# Maximum moment
M_max = w * L**2 / 8

print(f"Reaction: {R_A:.2f}")
print(f"Max moment: {M_max:.2f}")
```

**Output:**
```
Reaction: 45.00 kN
Max moment: 67.50 kN·m
```

## Architecture

```
Frontend (React + Monaco Editor)
         ↓ REST API
Backend (FastAPI + Python)
         ↓
Calculation Engine (Pint + Handcalcs)
         ↓
Export Engine (Pandoc)
```

## Documentation

- **[Detailed README](./README_DETAILED.md)** - Complete documentation
- **[Development Guide](./DEVELOPMENT.md)** - For developers
- **[API Docs](http://localhost:8000/docs)** - When server is running

## Project Structure

```
ClaudeSandbox/
├── backend/          # FastAPI server + calculation engine
├── frontend/         # React + TypeScript UI
├── documents/        # User calculation documents
├── templates/        # Reusable calculation templates
├── exports/          # Generated PDFs
└── run-dev.sh       # Development launcher
```

## Tech Stack

### Backend
- FastAPI - Modern Python web framework
- Pint - Unit-aware calculations
- Handcalcs - LaTeX equation generation
- Pandoc - PDF export

### Frontend
- React 18 + TypeScript
- Monaco Editor (VS Code editor)
- KaTeX (fast math rendering)
- Tailwind CSS

## Roadmap

- [x] **Phase 1: MVP**
  - [x] Basic editor and preview
  - [x] Python calculations with units
  - [x] PDF export
  - [x] Template system

- [ ] **Phase 2: Enhanced Features**
  - [ ] Desktop packaging (PyWebView/Tauri)
  - [ ] Figure auto-numbering
  - [ ] Cross-references
  - [ ] Search functionality

- [ ] **Phase 3: AI Integration**
  - [ ] LLM-assisted calculation writing
  - [ ] Natural language to code
  - [ ] Automatic verification

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

See [DEVELOPMENT.md](./DEVELOPMENT.md) for detailed guidelines.

## License

MIT License - see [LICENSE](./LICENSE) file

## Why EngiCalc?

Existing tools like MathCAD are:
- Expensive ($1500+/year)
- Proprietary formats (not version control friendly)
- Clunky interfaces
- Limited automation

EngiCalc is:
- Free and open source
- Plain text files (git-friendly)
- Modern web technologies
- Built for automation and AI integration

## Screenshots

*Coming soon - the tool is currently in MVP stage*

## Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Documentation**: See [README_DETAILED.md](./README_DETAILED.md)

---

**Built with ❤️ for engineers, by engineers**
