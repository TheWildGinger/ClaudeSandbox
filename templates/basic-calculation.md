---
name: "Basic Calculation Template"
description: "Simple template for quick calculations"
category: "General"
variables: ["project_name"]
---

# {{project_name}}

## Calculation

### Input Values

```python
%%calc
# Define your parameters here
# Example:
# force = 100 * ureg.kN
# distance = 5 * ureg.meter

print("Define your input parameters above")
```

### Analysis

```python
%%calc
# Perform your calculations here
# Example:
# moment = force * distance
# print(f"Moment: {moment}")

print("Add your calculation steps here")
```

## Results

Document your results here.

## Notes

Add any additional notes or assumptions.
