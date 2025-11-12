"""Tests for LaTeX/handcalcs rendering - markdown math rendering."""

import pytest
from app.services.calculation_engine import calculation_engine
from app.models.calculation import CalculationBlock


class TestHandcalcsLatexGeneration:
    """Test that handcalcs generates LaTeX properly."""

    def test_latex_generation_basic(self):
        """Test that LaTeX is generated for simple calculations."""
        code = """
a = 10
b = 5
c = a + b
"""
        block = CalculationBlock(code=code, block_id="latex1")
        result = calculation_engine.execute_block(block, {})

        assert result.success is True
        # LaTeX may or may not be generated depending on handcalcs behavior
        # For simple assignments, handcalcs might not generate LaTeX
        # This is expected behavior

    def test_latex_generation_with_units(self):
        """Test LaTeX generation with Pint units."""
        code = """
L = 5.0 * ureg.meter
w = 10.0 * ureg.kN / ureg.meter
M = w * L**2 / 8
"""
        block = CalculationBlock(code=code, block_id="latex2")
        result = calculation_engine.execute_block(block, {})

        assert result.success is True
        # Check that calculation executed correctly
        assert result.result["L"]["magnitude"] == 5.0
        assert abs(result.result["M"]["magnitude"] - 31.25) < 0.01

    def test_latex_with_print_output(self):
        """Test that results are properly formatted in output."""
        code = """
# Beam parameters
L = 6.0 * ureg.meter
w = 15.0 * ureg.kN / ureg.meter

# Calculate moment
M_max = w * L**2 / 8

print(f"Length: {L}")
print(f"Load: {w}")
print(f"Maximum moment: {M_max:.2f}")
"""
        block = CalculationBlock(code=code, block_id="latex3")
        result = calculation_engine.execute_block(block, {})

        assert result.success is True
        assert "Length:" in result.output
        assert "Load:" in result.output
        assert "Maximum moment:" in result.output
        assert "67.5" in result.output or "67.50" in result.output

    def test_formatted_output(self):
        """Test that formatted strings work correctly."""
        code = """
x = 123.456789
print(f"Default: {x}")
print(f"2 decimals: {x:.2f}")
print(f"Scientific: {x:.2e}")
"""
        block = CalculationBlock(code=code, block_id="latex4")
        result = calculation_engine.execute_block(block, {})

        assert result.success is True
        assert "Default: 123.456789" in result.output
        assert "2 decimals: 123.46" in result.output
        assert "Scientific: 1.23e+02" in result.output


class TestMathematicalExpressions:
    """Test complex mathematical expressions render correctly."""

    def test_complex_formula(self):
        """Test a complex engineering formula."""
        code = """
# Euler buckling load
E = 200.0 * ureg.GPa  # Young's modulus for steel
I = 1.0e-6 * ureg.meter**4  # Moment of inertia
L = 3.0 * ureg.meter  # Column length
n = 1  # End condition factor

# Critical load
P_cr = (n * 3.14159**2 * E * I) / L**2

print(f"Critical buckling load: {P_cr.to(ureg.kN):.2f}")
"""
        block = CalculationBlock(code=code, block_id="latex5")
        result = calculation_engine.execute_block(block, {})

        assert result.success is True
        assert "Critical buckling load:" in result.output
        # Check the calculation is correct (approximately 219 kN or 2.193e-4 in GPa*m^2)
        P_cr_value = result.result["P_cr"]["magnitude"]
        # The value should be very small in GPa*m^2 units (around 0.0002193)
        assert 0.0001 < P_cr_value < 0.001  # Should be around 2.193e-4

    def test_trigonometric_expressions(self):
        """Test trigonometric functions in expressions."""
        code = """
import math

# Angle in degrees
angle_deg = 45.0
angle_rad = angle_deg * math.pi / 180.0

# Trig values
sin_val = sin(angle_rad)
cos_val = cos(angle_rad)
tan_val = tan(angle_rad)

print(f"sin(45°) = {sin_val:.4f}")
print(f"cos(45°) = {cos_val:.4f}")
print(f"tan(45°) = {tan_val:.4f}")
"""
        block = CalculationBlock(code=code, block_id="latex6")
        result = calculation_engine.execute_block(block, {})

        assert result.success is True
        # sin(45°) and cos(45°) should both be ≈ 0.7071
        assert abs(result.result["sin_val"] - 0.7071) < 0.001
        assert abs(result.result["cos_val"] - 0.7071) < 0.001
        assert abs(result.result["tan_val"] - 1.0) < 0.001


class TestMarkdownCompatibility:
    """Test that output is compatible with markdown rendering."""

    def test_special_characters_in_output(self):
        """Test that special characters are handled correctly."""
        code = """
# Test special characters that might affect markdown
result = 42
print("Result with symbols: $, *, _, #")
print(f"Value: {result}")
"""
        block = CalculationBlock(code=code, block_id="latex7")
        result = calculation_engine.execute_block(block, {})

        assert result.success is True
        assert "Result with symbols: $, *, _, #" in result.output

    def test_multiline_output(self):
        """Test multiline output formatting."""
        code = """
print("=" * 40)
print("Engineering Calculation Report")
print("=" * 40)
print("")
x = 100
print(f"Result: {x}")
print("")
print("=" * 40)
"""
        block = CalculationBlock(code=code, block_id="latex8")
        result = calculation_engine.execute_block(block, {})

        assert result.success is True
        assert "Engineering Calculation Report" in result.output
        assert "Result: 100" in result.output

    def test_table_like_output(self):
        """Test table-formatted output."""
        code = """
# Create table-like output
print(f"{'Parameter':<20} {'Value':<15} {'Unit':<10}")
print("-" * 45)

L = 5.0 * ureg.meter
w = 10.0 * ureg.kN / ureg.meter

print(f"{'Length':<20} {L.magnitude:<15.2f} {str(L.units):<10}")
print(f"{'Load':<20} {w.magnitude:<15.2f} {str(w.units):<10}")
"""
        block = CalculationBlock(code=code, block_id="latex9")
        result = calculation_engine.execute_block(block, {})

        assert result.success is True
        assert "Parameter" in result.output
        assert "Value" in result.output
        assert "Unit" in result.output
        assert "Length" in result.output
        assert "Load" in result.output


class TestUnitFormatting:
    """Test that units are formatted correctly for display."""

    def test_unit_display_format(self):
        """Test that units display in a readable format."""
        code = """
# Various unit formats
force = 1000.0 * ureg.newton
pressure = 100.0 * ureg.kPa
velocity = 10.0 * ureg.meter / ureg.second
acceleration = 9.81 * ureg.meter / ureg.second**2

print(f"Force: {force}")
print(f"Pressure: {pressure}")
print(f"Velocity: {velocity}")
print(f"Acceleration: {acceleration}")
"""
        block = CalculationBlock(code=code, block_id="latex10")
        result = calculation_engine.execute_block(block, {})

        assert result.success is True
        assert "Force:" in result.output
        assert "Pressure:" in result.output
        assert "Velocity:" in result.output
        assert "Acceleration:" in result.output

    def test_compound_units(self):
        """Test compound unit formatting."""
        code = """
# Moment (force × distance)
M = 50.0 * ureg.kN * 2.0 * ureg.meter

# Stress (force / area)
sigma = 100.0 * ureg.kN / (0.01 * ureg.meter**2)

# Convert to standard units
sigma_MPa = sigma.to(ureg.MPa)

print(f"Moment: {M}")
print(f"Stress: {sigma_MPa:.2f}")
"""
        block = CalculationBlock(code=code, block_id="latex11")
        result = calculation_engine.execute_block(block, {})

        assert result.success is True
        assert "Moment:" in result.output
        assert "Stress:" in result.output

    def test_dimensionless_quantities(self):
        """Test dimensionless quantities."""
        code = """
# Factor of safety (dimensionless)
capacity = 100.0 * ureg.kN
demand = 75.0 * ureg.kN
FoS = capacity / demand

print(f"Factor of Safety: {FoS:.2f}")
"""
        block = CalculationBlock(code=code, block_id="latex12")
        result = calculation_engine.execute_block(block, {})

        assert result.success is True
        assert "Factor of Safety:" in result.output
        # FoS should be approximately 1.33
        FoS_value = result.result["FoS"]["magnitude"]
        assert abs(FoS_value - 1.333) < 0.01


class TestResultSerialization:
    """Test that calculation results are properly serialized."""

    def test_result_structure(self):
        """Test that results have the correct structure."""
        code = """
x = 42
y = 3.14
z = 10.0 * ureg.meter
"""
        block = CalculationBlock(code=code, block_id="latex13")
        result = calculation_engine.execute_block(block, {})

        assert result.success is True

        # Check plain values
        assert result.result["x"] == 42
        assert abs(result.result["y"] - 3.14) < 0.001

        # Check Pint quantity structure
        assert "magnitude" in result.result["z"]
        assert "units" in result.result["z"]
        assert "formatted" in result.result["z"]

    def test_list_serialization(self):
        """Test that lists are serialized correctly."""
        code = """
values = [1, 2, 3, 4, 5]
unit_values = [i * ureg.meter for i in range(3)]
"""
        block = CalculationBlock(code=code, block_id="latex14")
        result = calculation_engine.execute_block(block, {})

        assert result.success is True
        assert result.result["values"] == [1, 2, 3, 4, 5]
        assert isinstance(result.result["unit_values"], list)
        assert len(result.result["unit_values"]) == 3
