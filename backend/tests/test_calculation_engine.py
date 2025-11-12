"""Tests for the calculation engine - math evaluation with Pint units."""

import pytest
from app.services.calculation_engine import calculation_engine
from app.models.calculation import CalculationBlock


class TestBasicMathEvaluation:
    """Test basic mathematical operations."""

    def test_simple_arithmetic(self):
        """Test basic arithmetic operations."""
        code = """
a = 10
b = 5
result_add = a + b
result_sub = a - b
result_mul = a * b
result_div = a / b
"""
        block = CalculationBlock(code=code, block_id="test1")
        result = calculation_engine.execute_block(block, {})

        assert result.success is True
        assert result.result["a"] == 10
        assert result.result["b"] == 5
        assert result.result["result_add"] == 15
        assert result.result["result_sub"] == 5
        assert result.result["result_mul"] == 50
        assert result.result["result_div"] == 2.0

    def test_math_functions(self):
        """Test mathematical functions."""
        code = """
import math
x = 16
result_sqrt = sqrt(x)
result_sin = sin(0)
result_cos = cos(0)
result_log = log(math.e)
"""
        block = CalculationBlock(code=code, block_id="test2")
        result = calculation_engine.execute_block(block, {})

        assert result.success is True
        assert result.result["result_sqrt"] == 4.0
        assert abs(result.result["result_sin"]) < 1e-10  # sin(0) ≈ 0
        assert abs(result.result["result_cos"] - 1.0) < 1e-10  # cos(0) ≈ 1
        assert abs(result.result["result_log"] - 1.0) < 1e-10  # log(e) ≈ 1

    def test_output_capture(self):
        """Test that print statements are captured."""
        code = """
x = 42
print(f"The answer is {x}")
print("Multiple lines")
"""
        block = CalculationBlock(code=code, block_id="test3")
        result = calculation_engine.execute_block(block, {})

        assert result.success is True
        assert "The answer is 42" in result.output
        assert "Multiple lines" in result.output


class TestPintUnitCalculations:
    """Test Pint unit-aware calculations."""

    def test_simple_units(self):
        """Test basic unit creation and conversion."""
        code = """
# Define lengths
L1 = 5.0 * ureg.meter
L2 = 100.0 * ureg.centimeter

# Convert and compare
L2_in_meters = L2.to(ureg.meter)
"""
        block = CalculationBlock(code=code, block_id="test4")
        result = calculation_engine.execute_block(block, {})

        assert result.success is True
        assert result.result["L1"]["magnitude"] == 5.0
        assert "m" in result.result["L1"]["units"] or "meter" in result.result["L1"]["units"]
        assert result.result["L2"]["magnitude"] == 100.0
        assert "cm" in result.result["L2"]["units"] or "centimeter" in result.result["L2"]["units"]
        assert result.result["L2_in_meters"]["magnitude"] == 1.0
        assert "m" in result.result["L2_in_meters"]["units"] or "meter" in result.result["L2_in_meters"]["units"]

    def test_unit_arithmetic(self):
        """Test arithmetic operations with units."""
        code = """
# Beam calculation
L = 6.0 * ureg.meter
w = 15.0 * ureg.kN / ureg.meter

# Calculate reaction and moment
R_A = w * L / 2
M_max = w * L**2 / 8
"""
        block = CalculationBlock(code=code, block_id="test5")
        result = calculation_engine.execute_block(block, {})

        assert result.success is True
        # Reaction should be 45 kN
        assert abs(result.result["R_A"]["magnitude"] - 45.0) < 0.01
        assert "kN" in result.result["R_A"]["units"] or "kilonewton" in result.result["R_A"]["units"]
        # Max moment should be 67.5 kN*m
        assert abs(result.result["M_max"]["magnitude"] - 67.5) < 0.01

    def test_unit_conversion(self):
        """Test unit conversions."""
        code = """
# Distance
d_meters = 1000.0 * ureg.meter
d_km = d_meters.to(ureg.kilometer)
d_feet = d_meters.to(ureg.feet)

# Force
F_N = 1000.0 * ureg.newton
F_kN = F_N.to(ureg.kilonewton)
"""
        block = CalculationBlock(code=code, block_id="test6")
        result = calculation_engine.execute_block(block, {})

        assert result.success is True
        assert result.result["d_km"]["magnitude"] == 1.0
        assert abs(result.result["d_feet"]["magnitude"] - 3280.84) < 0.01
        assert result.result["F_kN"]["magnitude"] == 1.0

    def test_dimensional_analysis(self):
        """Test that incompatible units raise errors."""
        code = """
# Try to add incompatible units (should fail)
length = 5.0 * ureg.meter
time = 10.0 * ureg.second
invalid = length + time  # This should fail
"""
        block = CalculationBlock(code=code, block_id="test7")
        result = calculation_engine.execute_block(block, {})

        assert result.success is False
        assert "DimensionalityError" in result.error or "Cannot convert" in result.error


class TestContextPreservation:
    """Test that context is preserved between calculation blocks."""

    def test_context_sharing(self):
        """Test that variables are shared across blocks."""
        # First block
        code1 = """
base = 10.0 * ureg.meter
height = 5.0 * ureg.meter
"""
        block1 = CalculationBlock(code=code1, block_id="test8a")
        result1 = calculation_engine.execute_block(block1, {})

        assert result1.success is True

        # Second block uses variables from first
        code2 = """
area = base * height
"""
        # Reconstruct context (simulating API behavior)
        context = {}
        for key, value in result1.result.items():
            if isinstance(value, dict) and "magnitude" in value and "units" in value:
                context[key] = value["magnitude"] * calculation_engine.ureg(value["units"])
            else:
                context[key] = value

        block2 = CalculationBlock(code=code2, block_id="test8b")
        result2 = calculation_engine.execute_block(block2, context)

        assert result2.success is True
        assert abs(result2.result["area"]["magnitude"] - 50.0) < 0.01


class TestErrorHandling:
    """Test error handling and reporting."""

    def test_syntax_error(self):
        """Test that syntax errors are caught."""
        code = """
x = 10
y = 20 +  # Syntax error
"""
        block = CalculationBlock(code=code, block_id="test9")
        result = calculation_engine.execute_block(block, {})

        assert result.success is False
        assert result.error is not None
        assert "SyntaxError" in result.error

    def test_runtime_error(self):
        """Test that runtime errors are caught."""
        code = """
x = 10
y = x / 0  # Division by zero
"""
        block = CalculationBlock(code=code, block_id="test10")
        result = calculation_engine.execute_block(block, {})

        assert result.success is False
        assert result.error is not None
        assert "ZeroDivisionError" in result.error

    def test_undefined_variable(self):
        """Test that undefined variable errors are caught."""
        code = """
result = undefined_var * 2
"""
        block = CalculationBlock(code=code, block_id="test11")
        result = calculation_engine.execute_block(block, {})

        assert result.success is False
        assert result.error is not None
        assert "NameError" in result.error


class TestEngineeringCalculations:
    """Test realistic engineering calculations."""

    def test_beam_analysis(self):
        """Test a complete beam analysis calculation."""
        code = """
# Simply supported beam with uniform load
L = 8.0 * ureg.meter
w = 12.0 * ureg.kN / ureg.meter

# Support reactions (symmetrical)
R_A = w * L / 2
R_B = w * L / 2

# Maximum moment at center
M_max = w * L**2 / 8

# Maximum shear at supports
V_max = w * L / 2

print(f"Reactions: {R_A:.2f}")
print(f"Max Moment: {M_max:.2f}")
print(f"Max Shear: {V_max:.2f}")
"""
        block = CalculationBlock(code=code, block_id="test12")
        result = calculation_engine.execute_block(block, {})

        assert result.success is True
        assert abs(result.result["R_A"]["magnitude"] - 48.0) < 0.01
        assert abs(result.result["M_max"]["magnitude"] - 96.0) < 0.01
        assert "Reactions: 48.00" in result.output

    def test_stress_calculation(self):
        """Test stress and strain calculations."""
        code = """
# Stress calculation
F = 50.0 * ureg.kN
A = 0.01 * ureg.meter**2
sigma = F / A

# Convert to MPa
sigma_MPa = sigma.to(ureg.MPa)

print(f"Stress: {sigma_MPa:.2f}")
"""
        block = CalculationBlock(code=code, block_id="test13")
        result = calculation_engine.execute_block(block, {})

        assert result.success is True
        assert abs(result.result["sigma_MPa"]["magnitude"] - 5.0) < 0.01

    def test_fluid_mechanics(self):
        """Test fluid mechanics calculations."""
        code = """
# Flow rate calculation
velocity = 2.5 * ureg.meter / ureg.second
diameter = 0.1 * ureg.meter
area = 3.14159 * (diameter / 2)**2
flow_rate = velocity * area

# Convert to liters per second
flow_rate_lps = flow_rate.to(ureg.liter / ureg.second)

print(f"Flow rate: {flow_rate_lps:.2f}")
"""
        block = CalculationBlock(code=code, block_id="test14")
        result = calculation_engine.execute_block(block, {})

        assert result.success is True
        # Flow rate should be approximately 19.6 L/s
        assert abs(result.result["flow_rate_lps"]["magnitude"] - 19.63) < 0.1


class TestPerformance:
    """Test performance and execution time tracking."""

    def test_execution_time_recorded(self):
        """Test that execution time is recorded."""
        code = """
x = sum(range(1000))
"""
        block = CalculationBlock(code=code, block_id="test15")
        result = calculation_engine.execute_block(block, {})

        assert result.success is True
        assert result.execution_time is not None
        assert result.execution_time > 0
        assert result.execution_time < 1.0  # Should be very fast

    def test_large_calculation(self):
        """Test that larger calculations complete successfully."""
        code = """
# Generate some data
data = [i * ureg.meter for i in range(100)]
total = sum(data)
average = total / len(data)
"""
        block = CalculationBlock(code=code, block_id="test16")
        result = calculation_engine.execute_block(block, {})

        assert result.success is True
        assert result.result["average"]["magnitude"] == 49.5
