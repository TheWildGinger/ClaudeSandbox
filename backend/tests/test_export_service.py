"""Tests for export service - PDF and HTML export."""

import shutil
from pathlib import Path

import pytest
from app.services.export_service import export_service


class TestPandocAvailability:
    """Test Pandoc installation and availability."""

    def test_pandoc_check(self):
        """Test if Pandoc is installed and available."""
        # Check if pandoc is in PATH
        pandoc_path = shutil.which("pandoc")

        if pandoc_path:
            print(f"✓ Pandoc found at: {pandoc_path}")
            assert export_service.pandoc_available is True
        else:
            print("✗ Pandoc NOT found - PDF export will not work")
            print("  To install Pandoc:")
            print("  - Ubuntu/Debian: sudo apt-get install pandoc")
            print("  - macOS: brew install pandoc")
            print("  - Windows: Download from https://pandoc.org/installing.html")
            assert export_service.pandoc_available is False

    def test_exports_directory_exists(self):
        """Test that exports directory is created."""
        assert export_service.exports_dir.exists()
        assert export_service.exports_dir.is_dir()


@pytest.mark.skipif(
    not export_service.pandoc_available, reason="Pandoc not installed - skipping PDF tests"
)
class TestPDFExport:
    """Test PDF export functionality (requires Pandoc)."""

    def setup_method(self):
        """Setup test method - clean exports directory."""
        # Clean up any existing test files
        for file in export_service.exports_dir.glob("test_*.pdf"):
            file.unlink()

    def test_simple_pdf_export(self):
        """Test exporting a simple markdown document to PDF."""
        markdown_content = """
# Test Document

This is a simple test document.

## Section 1

Some content with **bold** and *italic* text.

## Section 2

- List item 1
- List item 2
- List item 3
"""
        output_path = export_service.export_to_pdf(markdown_content, "test_simple")

        assert output_path.exists()
        assert output_path.suffix == ".pdf"
        assert output_path.stat().st_size > 0
        print(f"✓ PDF generated: {output_path} ({output_path.stat().st_size} bytes)")

    def test_pdf_with_math(self):
        """Test PDF export with mathematical equations."""
        markdown_content = """
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
        output_path = export_service.export_to_pdf(markdown_content, "test_math")

        assert output_path.exists()
        assert output_path.suffix == ".pdf"
        assert output_path.stat().st_size > 0
        print(f"✓ PDF with math generated: {output_path} ({output_path.stat().st_size} bytes)")

    def test_pdf_with_metadata(self):
        """Test PDF export with metadata."""
        markdown_content = """
# Project Calculation

This is a calculation document with metadata.
"""
        metadata = {
            "title": "Test Calculation",
            "author": "Test Engineer",
            "date": "2024-11-12",
        }

        output_path = export_service.export_to_pdf(
            markdown_content, "test_metadata", metadata=metadata
        )

        assert output_path.exists()
        assert output_path.suffix == ".pdf"
        print(f"✓ PDF with metadata generated: {output_path}")

    def test_pdf_with_code_blocks(self):
        """Test PDF export with code blocks."""
        markdown_content = """
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
        output_path = export_service.export_to_pdf(markdown_content, "test_code")

        assert output_path.exists()
        assert output_path.stat().st_size > 0
        print(f"✓ PDF with code blocks generated: {output_path}")

    def test_pdf_complex_document(self):
        """Test PDF export with a complex engineering document."""
        markdown_content = """
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
        output_path = export_service.export_to_pdf(markdown_content, "test_complex")

        assert output_path.exists()
        assert output_path.stat().st_size > 0
        print(f"✓ Complex PDF generated: {output_path} ({output_path.stat().st_size} bytes)")

    def test_pdf_filename_without_extension(self):
        """Test that .pdf extension is added if missing."""
        markdown_content = "# Test\n\nSimple test."

        output_path = export_service.export_to_pdf(markdown_content, "test_extension")

        assert output_path.name == "test_extension.pdf"
        assert output_path.exists()

    def test_pdf_filename_with_extension(self):
        """Test that .pdf extension is preserved if provided."""
        markdown_content = "# Test\n\nSimple test."

        output_path = export_service.export_to_pdf(markdown_content, "test_extension2.pdf")

        assert output_path.name == "test_extension2.pdf"
        assert output_path.exists()


@pytest.mark.skipif(
    export_service.pandoc_available, reason="Testing error handling when Pandoc is not available"
)
class TestPDFExportWithoutPandoc:
    """Test PDF export error handling when Pandoc is not installed."""

    def test_pdf_export_fails_without_pandoc(self):
        """Test that PDF export raises error when Pandoc is not available."""
        markdown_content = "# Test\n\nSimple test."

        with pytest.raises(RuntimeError, match="Pandoc is not available"):
            export_service.export_to_pdf(markdown_content, "test_fail")


class TestHTMLExport:
    """Test HTML export functionality."""

    def setup_method(self):
        """Setup test method - clean exports directory."""
        # Clean up any existing test files
        for file in export_service.exports_dir.glob("test_*.html"):
            file.unlink()

    def test_simple_html_export(self):
        """Test exporting a simple markdown document to HTML."""
        markdown_content = """
<h1>Test Document</h1>
<p>This is a simple test document.</p>
"""
        output_path = export_service.export_to_html(markdown_content, "test_html_simple")

        assert output_path.exists()
        assert output_path.suffix == ".html"
        assert output_path.stat().st_size > 0

        # Read and verify content
        content = output_path.read_text()
        assert "<!DOCTYPE html>" in content
        assert "Test Document" in content
        print(f"✓ HTML generated: {output_path}")

    def test_html_with_math(self):
        """Test HTML export includes KaTeX for math rendering."""
        markdown_content = """
<h1>Math Test</h1>
<p>Inline math: $E = mc^2$</p>
<p>Display math: $$\\frac{wL^2}{8}$$</p>
"""
        output_path = export_service.export_to_html(markdown_content, "test_html_math")

        assert output_path.exists()

        # Verify KaTeX is included
        content = output_path.read_text()
        assert "katex" in content.lower()
        assert "Math Test" in content
        print(f"✓ HTML with math support generated: {output_path}")

    def test_html_filename_handling(self):
        """Test that .html extension is added if missing."""
        markdown_content = "<h1>Test</h1>"

        output_path = export_service.export_to_html(markdown_content, "test_html_ext")

        assert output_path.name == "test_html_ext.html"
        assert output_path.exists()


class TestExportErrorHandling:
    """Test error handling in export functionality."""

    @pytest.mark.skipif(
        not export_service.pandoc_available, reason="Requires Pandoc for error testing"
    )
    def test_invalid_markdown_content(self):
        """Test handling of invalid content."""
        # Even invalid markdown should not crash the export
        # Pandoc is quite forgiving
        markdown_content = "<<<INVALID>>> {{{ MARKDOWN }}}"

        try:
            output_path = export_service.export_to_pdf(markdown_content, "test_invalid")
            # If it succeeds, that's also acceptable (Pandoc might process it)
            assert output_path.exists()
            print("✓ Export handled invalid markdown gracefully")
        except RuntimeError as e:
            # If it fails, that's expected
            print(f"✓ Export properly rejected invalid content: {e}")


class TestExportIntegration:
    """Integration tests for the export system."""

    def test_export_directory_permissions(self):
        """Test that export directory has correct permissions."""
        assert export_service.exports_dir.exists()
        assert export_service.exports_dir.is_dir()

        # Try to create a test file
        test_file = export_service.exports_dir / "test_permissions.txt"
        test_file.write_text("test")
        assert test_file.exists()

        # Clean up
        test_file.unlink()
        print("✓ Export directory has correct permissions")

    def test_multiple_exports(self):
        """Test that multiple exports don't interfere with each other."""
        content1 = "# Document 1\n\nFirst document."
        content2 = "# Document 2\n\nSecond document."

        path1 = export_service.export_to_html(content1, "test_multi1")
        path2 = export_service.export_to_html(content2, "test_multi2")

        assert path1.exists()
        assert path2.exists()
        assert path1 != path2

        # Verify content is different
        assert "First document" in path1.read_text()
        assert "Second document" in path2.read_text()
        print("✓ Multiple exports work independently")
