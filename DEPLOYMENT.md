# EngiCalc Windows Deployment Guide

This guide explains how to create a standalone version of EngiCalc for Windows desktop deployment and testing.

## Table of Contents

1. [Overview](#overview)
2. [Option 1: Single Executable (Recommended)](#option-1-single-executable-recommended)
3. [Option 2: Portable Package](#option-2-portable-package)
4. [Testing the Deployment](#testing-the-deployment)
5. [Troubleshooting](#troubleshooting)

---

## Overview

EngiCalc can be deployed on Windows in two ways:

- **Option 1**: Single `.exe` file (using PyInstaller) - Best for distribution
- **Option 2**: Portable folder with launcher script - Easier to debug

Both options:
- Bundle the FastAPI backend and React frontend together
- Auto-open a web browser when launched
- Store user data in `%USERPROFILE%\EngiCalc` (e.g., `C:\Users\YourName\EngiCalc`)
- Don't require any manual installation or configuration

---

## Option 1: Single Executable (Recommended)

This creates a single `EngiCalc.exe` file that contains everything needed to run the application.

### Requirements

- Windows 10 or 11
- Python 3.10, 3.11, 3.12, 3.13, or 3.14
- Node.js 16+ and npm
- Internet connection (for initial setup)

### Build Steps

1. **Open Command Prompt** (or PowerShell) in the project root directory

2. **Run the build script**:
   ```cmd
   build-windows.bat
   ```

3. **Wait for the build to complete** (5-10 minutes)
   - Frontend will be built first
   - Backend dependencies will be installed
   - PyInstaller will bundle everything into an .exe

4. **Find your executable**:
   ```
   backend\dist\EngiCalc.exe
   ```

### File Size

The executable will be approximately **50-100 MB** depending on dependencies.

### Usage

1. Copy `EngiCalc.exe` to any location (e.g., your Desktop)
2. Double-click to run
3. A console window will appear showing startup logs
4. Your default browser will open automatically to `http://127.0.0.1:8000`
5. Start creating engineering calculations!

### Data Storage

- Documents: `%USERPROFILE%\EngiCalc\documents`
- Templates: `%USERPROFILE%\EngiCalc\templates`
- Exports: `%USERPROFILE%\EngiCalc\exports`
- A sample document is created automatically on first run

### Stopping the Application

Press `Ctrl+C` in the console window or simply close the console window.

---

## Option 2: Portable Package

This creates a folder with all necessary files and a launcher script. Easier to debug if something goes wrong.

### Requirements

Same as Option 1, plus:
- Poetry (Python package manager)

### Build Steps

1. **Install Poetry** (if not already installed):
   ```cmd
   pip install poetry
   ```

2. **Run the portable package script**:
   ```cmd
   create-portable-package.bat
   ```

3. **Find your package**:
   ```
   EngiCalc-Portable\
   ```

### Package Contents

```
EngiCalc-Portable/
├── backend/              # Python backend code
├── frontend/             # Built React frontend
└── Start-EngiCalc.bat   # Double-click to run
```

### Usage

1. Copy the entire `EngiCalc-Portable` folder anywhere
2. Double-click `Start-EngiCalc.bat`
3. First run will install dependencies (this takes a few minutes)
4. Browser opens automatically
5. Start working!

### Advantages

- Can see what files are included
- Easier to debug issues
- Can modify code if needed
- Faster startup (no unpacking needed)

### Disadvantages

- Multiple files instead of one
- Larger total size
- Dependencies install on first run

---

## Testing the Deployment

### Quick Test Checklist

After building, test these features:

1. **Launch** - Double-click the .exe or .bat file
   - [ ] Console window appears
   - [ ] No error messages
   - [ ] Browser opens automatically

2. **UI Loads** - Check the browser
   - [ ] EngiCalc interface appears
   - [ ] Sidebar shows documents
   - [ ] Sample document is created

3. **Edit Document** - Try the editor
   - [ ] Can type in the editor
   - [ ] Preview updates in real-time
   - [ ] LaTeX math renders correctly

4. **Run Calculation** - Test the calculation engine
   ```python
   %%calc
   L = 5.0 * ureg.meter
   F = 100 * ureg.kN
   stress = F / (L ** 2)
   print(f"Stress: {stress}")
   ```
   - [ ] Calculation executes
   - [ ] Results appear in preview
   - [ ] Units are handled correctly

5. **Save Document**
   - [ ] Click "Save" button
   - [ ] Success message appears
   - [ ] Document persists after reload

6. **Export PDF** (requires Pandoc)
   - [ ] Click "Export PDF"
   - [ ] PDF downloads
   - [ ] PDF contains calculations with LaTeX

7. **Shutdown**
   - [ ] Close browser
   - [ ] Press Ctrl+C in console
   - [ ] Application exits cleanly

### Known Limitations

1. **PDF Export requires Pandoc**
   - Not bundled with the executable
   - Users must install Pandoc separately from https://pandoc.org/
   - Alternative: Export functionality will show an error message

2. **First-time startup is slow**
   - The .exe needs to unpack to a temp directory
   - Subsequent runs are faster

3. **Windows Defender might flag the .exe**
   - PyInstaller executables are sometimes flagged as suspicious
   - This is a false positive
   - Add an exception if needed

4. **Console window stays open**
   - This is intentional - shows logs for debugging
   - Can be hidden by changing `console=False` in `EngiCalc.spec`

---

## Troubleshooting

### Build Fails on Windows

**Error**: `poetry not found`
```cmd
pip install poetry
```

**Error**: `npm not found`
- Install Node.js from https://nodejs.org/

**Error**: `Python version mismatch`
- Install Python 3.10-3.14 from https://www.python.org/
- Make sure to check "Add Python to PATH" during installation

### Executable Won't Run

**Error**: `MSVCP140.dll missing`
- Install Visual C++ Redistributable: https://aka.ms/vs/17/release/vc_redist.x64.exe

**Error**: `Failed to execute script`
- Run from Command Prompt to see error details
- Check if antivirus is blocking it

**Browser doesn't open**
- Manually navigate to `http://127.0.0.1:8000`
- Check if port 8000 is already in use

### Calculations Don't Work

**Error**: `ureg not defined`
- This is expected - use `ureg` in calc blocks
- Example: `L = 5 * ureg.meter`

**Error**: Python syntax error
- Check your Python code syntax
- Make sure the code block has `%%calc` magic comment

### PDF Export Fails

**Error**: `Pandoc not found`
- Install Pandoc from https://pandoc.org/installing.html
- Restart EngiCalc after installing

**Error**: `pdflatex not found`
- Install a LaTeX distribution:
  - MiKTeX (Windows): https://miktex.org/
  - TeX Live (cross-platform): https://www.tug.org/texlive/

---

## Distribution

### Sharing the Executable

1. Build on Windows (can't cross-compile)
2. Test thoroughly
3. Share `EngiCalc.exe` file via:
   - Email (if < 25MB)
   - Google Drive / Dropbox
   - USB drive
   - Internal file server

### For Multiple Users

Consider creating a batch file installer:

```batch
@echo off
echo Installing EngiCalc...
copy EngiCalc.exe "%USERPROFILE%\Desktop\EngiCalc.exe"
echo.
echo EngiCalc installed to Desktop!
echo Double-click EngiCalc.exe to run.
pause
```

### Version Management

Add version info to the executable by creating `version_info.txt`:

```
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(0, 1, 0, 0),
    prodvers=(0, 1, 0, 0),
    OS=0x40004,
    fileType=0x1,
  ),
  kids=[
    StringFileInfo([
      StringTable('040904B0', [
        StringStruct('CompanyName', 'Your Company'),
        StringStruct('FileDescription', 'EngiCalc - Engineering Calculations'),
        StringStruct('FileVersion', '0.1.0'),
        StringStruct('ProductName', 'EngiCalc'),
        StringStruct('ProductVersion', '0.1.0'),
      ])
    ]),
  ]
)
```

Then update `EngiCalc.spec`:
```python
exe = EXE(
    ...
    version='version_info.txt',
    ...
)
```

---

## Next Steps

1. **Build the executable on your Windows desktop**
2. **Test all features thoroughly**
3. **Gather user feedback**
4. **Iterate based on feedback**

For development improvements, see the main README.md.

For issues or questions, please create a GitHub issue.
