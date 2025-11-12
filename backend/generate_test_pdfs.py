"""Script to generate all test PDF outputs for review."""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.export_service import export_service


def generate_test_pdfs():
    """Generate all PDF test outputs."""

    # 1. Simple PDF export
    simple_content = """
# Test Document

This is a simple test document.

## Section 1

Some content with **bold** and *italic* text.

## Section 2

- List item 1
- List item 2
- List item 3
"""
    output = export_service.export_to_pdf(simple_content, "test_simple")
    print(f"✓ Generated: {output} ({output.stat().st_size} bytes)")

    # 2. PDF with math
    math_content = """
# Engineering Calculation

## Beam Analysis

The maximum moment for a simply supported beam with uniform load is:

$$M_{max} = \\frac{wL^2}{8}$$

Where:
- $w$ is the uniform load (kN/m)
- $L$ is the span length (m)

### Example Calculation

Given:
- $w = 10$ kN/m
- $L = 6$ m

Calculate:
$$M_{max} = \\frac{10 \\times 6^2}{8} = 45 \\text{ kN·m}$$
"""
    output = export_service.export_to_pdf(math_content, "test_math")
    print(f"✓ Generated: {output} ({output.stat().st_size} bytes)")

    # 3. PDF with metadata
    metadata_content = """
# Project Calculation

This is a calculation document with metadata.
"""
    metadata = {
        "title": "Test Calculation",
        "author": "Test Engineer",
        "date": "2024-11-12",
    }
    output = export_service.export_to_pdf(metadata_content, "test_metadata", metadata=metadata)
    print(f"✓ Generated: {output} ({output.stat().st_size} bytes)")

    # 4. PDF with code blocks
    code_content = """
# Calculation with Code

## Python Calculation

```python
# Simply supported beam
L = 6.0  # meters
w = 15.0  # kN/m

# Maximum moment
M_max = w * L**2 / 8
print(f"Maximum moment: {M_max:.2f} kN·m")
```

## Results

The calculation shows that the maximum moment is 67.50 kN·m.
"""
    output = export_service.export_to_pdf(code_content, "test_code")
    print(f"✓ Generated: {output} ({output.stat().st_size} bytes)")

    # 5. Complex engineering document
    complex_content = """
---
title: Structural Analysis Report
author: Engineering Team
date: 2024-11-12
---

# Project Overview

This document presents the structural analysis for the beam design.

## Design Parameters

| Parameter | Value | Unit |
|-----------|-------|------|
| Span | 8.0 | m |
| Load | 12.0 | kN/m |
| Material | Steel | - |

## Calculations

### Support Reactions

For a simply supported beam with uniform load:

$$R_A = R_B = \\frac{wL}{2}$$

Substituting values:

$$R_A = R_B = \\frac{12.0 \\times 8.0}{2} = 48.0 \\text{ kN}$$

### Maximum Moment

$$M_{max} = \\frac{wL^2}{8} = \\frac{12.0 \\times 8.0^2}{8} = 96.0 \\text{ kN·m}$$

### Maximum Shear

$$V_{max} = \\frac{wL}{2} = 48.0 \\text{ kN}$$

## Python Verification

```python
# Beam parameters
L = 8.0 * ureg.meter
w = 12.0 * ureg.kN / ureg.meter

# Reactions
R_A = w * L / 2
print(f"Reaction: {R_A:.2f}")

# Maximum moment
M_max = w * L**2 / 8
print(f"Max moment: {M_max:.2f}")
```

## Conclusions

1. Support reactions: 48.0 kN
2. Maximum moment: 96.0 kN·m
3. Maximum shear: 48.0 kN

All values are within acceptable limits.
"""
    output = export_service.export_to_pdf(complex_content, "test_complex")
    print(f"✓ Generated: {output} ({output.stat().st_size} bytes)")

    print(f"\n✓ All PDFs generated successfully!")
    print(f"✓ Location: {export_service.exports_dir}")


if __name__ == "__main__":
    if not export_service.pandoc_available:
        print("✗ Error: Pandoc is not available!")
        sys.exit(1)

    generate_test_pdfs()
