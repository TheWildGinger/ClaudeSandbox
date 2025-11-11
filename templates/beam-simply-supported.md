---
name: "Simply Supported Beam"
description: "Analysis of a simply supported beam with uniform distributed load"
category: "Structural"
variables: ["project_name", "engineer_name"]
---

# Simply Supported Beam Analysis

**Project:** {{project_name}}
**Engineer:** {{engineer_name}}
**Date:** {{date}}

## Problem Statement

Analyze a simply supported beam subjected to a uniform distributed load.

## Given Parameters

```python
%%calc
# Beam geometry
L = 6.0 * ureg.meter

# Loading
w = 15.0 * ureg.kN / ureg.meter

# Material properties
E = 200.0 * ureg.GPa
I = 150e6 * ureg.mm**4

print("Beam parameters defined")
```

## Analysis

### Reactions

For a simply supported beam with uniform load:

```python
%%calc
# Calculate reactions (symmetrical)
R_A = w * L / 2
R_B = w * L / 2

print(f"Reaction at A: {R_A:.2f}")
print(f"Reaction at B: {R_B:.2f}")
```

### Maximum Moment

```python
%%calc
# Maximum moment occurs at midspan
M_max = w * L**2 / 8

print(f"Maximum moment: {M_max:.2f}")
```

### Maximum Deflection

```python
%%calc
# Convert I to m^4 for consistency
I_m4 = I.to(ureg.m**4)

# Maximum deflection at midspan
delta_max = (5 * w * L**4) / (384 * E * I_m4)

# Convert to mm for practical units
delta_max_mm = delta_max.to(ureg.mm)

print(f"Maximum deflection: {delta_max_mm:.2f}")
```

## Summary

- Maximum moment: See calculation above
- Maximum deflection: See calculation above
- Reactions are equal due to symmetry

## Free Body Diagram

![Simply Supported Beam FBD](./images/beam-fbd.png)

*Note: Add your own FBD image*
