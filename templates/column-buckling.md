---
name: "Column Buckling Analysis"
description: "Euler buckling analysis for a pinned-pinned column"
category: "Structural"
variables: []
---

# Column Buckling Analysis

## Introduction

This calculation determines the critical buckling load for a column using Euler's formula.

## Input Parameters

```python
%%calc
# Column geometry
L = 3.5 * ureg.meter  # Length
d = 200 * ureg.mm     # Diameter

# Material properties
E = 200 * ureg.GPa    # Young's modulus
sigma_y = 250 * ureg.MPa  # Yield strength

print("Column parameters:")
print(f"  Length: {L}")
print(f"  Diameter: {d}")
```

## Section Properties

```python
%%calc
import math

# Calculate second moment of area for circular cross-section
I = (math.pi * d**4) / 64

# Calculate area
A = (math.pi * d**2) / 4

# Radius of gyration
r = sqrt(I / A)

print(f"Second moment of area: {I.to(ureg.mm**4):.2e}")
print(f"Cross-sectional area: {A.to(ureg.mm**2):.2f}")
print(f"Radius of gyration: {r.to(ureg.mm):.2f}")
```

## Critical Buckling Load

```python
%%calc
# Effective length factor for pinned-pinned column
K = 1.0

# Effective length
L_e = K * L

# Euler buckling load
P_cr = (math.pi**2 * E * I) / (L_e**2)

# Convert to kN
P_cr_kN = P_cr.to(ureg.kN)

print(f"Effective length: {L_e}")
print(f"Critical buckling load: {P_cr_kN:.2f}")
```

## Slenderness Ratio

```python
%%calc
# Calculate slenderness ratio
lambda_ratio = L_e / r

print(f"Slenderness ratio: {lambda_ratio:.2f}")

# Check if Euler formula is valid (typically λ > 100)
if lambda_ratio.magnitude > 100:
    print("✓ Euler formula is applicable (λ > 100)")
else:
    print("⚠ Warning: Column may be short - Euler formula may not apply")
```

## Results Summary

| Parameter | Value |
|-----------|-------|
| Critical Load | (see calculation) |
| Slenderness Ratio | (see calculation) |
| Effective Length | (see calculation) |

## Conclusion

The critical buckling load has been calculated using Euler's formula. Ensure that:
1. The column slenderness ratio is sufficient for Euler's formula
2. The applied load is less than the critical load
3. Material yielding is also checked separately
