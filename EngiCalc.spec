# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller spec file for EngiCalc standalone executable.
This creates a single-file executable that bundles the FastAPI backend
and React frontend into one distributable file.
"""

import sys
from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Get the base directory (parent of backend)
block_cipher = None
spec_dir = Path(SPECPATH)  # Directory containing this spec file
backend_dir = spec_dir / 'backend'
frontend_dir = spec_dir / 'frontend'

# Collect all necessary data files
datas = []

# Add frontend dist folder
frontend_dist = frontend_dir / 'dist'
if frontend_dist.exists():
    datas.append((str(frontend_dist), 'frontend/dist'))
    print(f"✓ Adding frontend from: {frontend_dist}")
else:
    print(f"⚠ Warning: Frontend dist not found at {frontend_dist}")

# Add handcalcs templates (required for LaTeX generation)
handcalcs_data = collect_data_files('handcalcs')
datas.extend(handcalcs_data)

# Add pint unit definitions
pint_data = collect_data_files('pint')
datas.extend(pint_data)

# Collect hidden imports (modules that PyInstaller might miss)
hiddenimports = [
    'uvicorn.logging',
    'uvicorn.loops',
    'uvicorn.loops.auto',
    'uvicorn.protocols',
    'uvicorn.protocols.http',
    'uvicorn.protocols.http.auto',
    'uvicorn.protocols.websockets',
    'uvicorn.protocols.websockets.auto',
    'uvicorn.lifespan',
    'uvicorn.lifespan.on',
    'app.api.calculation',
    'app.api.document',
    'app.api.export',
    'app.api.template',
    'app.core.config',
    'app.services.calculation',
    'app.services.document',
    'app.services.export',
]

# Add all fastapi and pydantic modules
hiddenimports.extend(collect_submodules('fastapi'))
hiddenimports.extend(collect_submodules('pydantic'))
hiddenimports.extend(collect_submodules('pydantic_settings'))
hiddenimports.extend(collect_submodules('starlette'))

a = Analysis(
    [str(backend_dir / 'standalone.py')],
    pathex=[str(backend_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'PIL',
        'tkinter',
        'IPython',
        'notebook',
        'jupyter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='EngiCalc',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Show console window for logs
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon file path here if you have one
)
