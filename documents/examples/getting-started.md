---
project: "EngiCalc Tutorial"
engineer: "Getting Started"
date: "2025-11-11"
revision: "1.0"
title: "Getting Started with EngiCalc"
---

# Getting Started with EngiCalc

Welcome to EngiCalc! This document will help you understand how to use the tool for engineering calculations.

## Features

EngiCalc provides:

- **Markdown-based documents** with YAML frontmatter for metadata
- **Live calculation execution** using Python with unit support
- **Math rendering** using KaTeX for beautiful equations
- **PDF export** for professional documentation
- **Template system** for reusable calculations

## Writing Calculations

### Basic Calculation Block

Use triple backticks with `python` and include `%%calc` to mark a calculation block:

\`\`\`python
%%calc
# Define values with units
length = 5.0 * ureg.meter
width = 3.0 * ureg.meter

# Calculate area
area = length * width

print(f"Area: {area}")
\`\`\`

### Using Units

EngiCalc uses the Pint library for unit-aware calculations:

\`\`\`python
%%calc
# Common units
force = 100 * ureg.kN
distance = 2.5 * ureg.meter
pressure = 50 * ureg.MPa

# Unit conversion
force_N = force.to(ureg.N)
print(f"Force in Newtons: {force_N}")
\`\`\`

### Available Units

Common engineering units available:

- **Length**: meter (m), millimeter (mm), foot (ft), inch (in)
- **Force**: newton (N), kilonewton (kN), pound_force (lbf)
- **Pressure**: pascal (Pa), megapascal (MPa), psi
- **Mass**: kilogram (kg), pound (lb)
- **Area**: meter**2, mm**2, etc.
- **Volume**: meter**3, liter, gallon

## Mathematical Notation

You can use LaTeX math notation for equations:

Inline math: $F = ma$

Display math:

$$\sigma = \frac{F}{A}$$

$$M_{max} = \frac{wL^2}{8}$$

## Document Structure

### Frontmatter

Always include YAML frontmatter at the top:

\`\`\`yaml
---
project: "Project Name"
engineer: "Your Name"
date: "2025-11-11"
revision: "A"
---
\`\`\`

### Headings

Use markdown headings to structure your document:

\`\`\`markdown
# Main Title
## Section
### Subsection
\`\`\`

### Images

Include images using markdown syntax:

\`\`\`markdown
![Description](./images/diagram.png)
\`\`\`

## Example Calculation

Here's a complete example:

\`\`\`python
%%calc
# Cantilever beam analysis
L = 4.0 * ureg.meter      # Beam length
P = 50.0 * ureg.kN        # Point load at end
E = 200.0 * ureg.GPa      # Young's modulus
I = 80e6 * ureg.mm**4     # Second moment of area

# Maximum moment (at fixed end)
M_max = P * L

# Maximum deflection (at free end)
# Convert I to m^4
I_m4 = I.to(ureg.m**4)
delta_max = (P * L**3) / (3 * E * I_m4)
delta_mm = delta_max.to(ureg.mm)

print(f"Maximum moment: {M_max:.2f}")
print(f"Maximum deflection: {delta_mm:.2f}")
\`\`\`

## Tips

1. **Save Often**: Click the "Save" button to save your work
2. **Export to PDF**: Use "Export PDF" to generate professional documentation
3. **Use Templates**: Start from templates in the sidebar for common calculations
4. **Units Are Key**: Always include units with `ureg.unit_name`
5. **Check Results**: The preview pane shows results in real-time

## Next Steps

- Explore the templates in the sidebar
- Try creating your own calculations
- Export your work to PDF
- Organize your calculations in separate documents

Happy calculating!
