"""Calculation engine service using Pint and Handcalcs."""

import io
import logging
import sys
import time
from contextlib import redirect_stdout
from typing import Any, Dict

import pint
from handcalcs import handcalc

from app.models.calculation import CalculationBlock, CalculationResult

logger = logging.getLogger(__name__)

# Initialize Pint unit registry
ureg = pint.UnitRegistry()
ureg.default_format = "~P"  # Pretty format


class CalculationEngine:
    """Engine for executing Python calculations with units."""

    def __init__(self):
        """Initialize the calculation engine."""
        self.ureg = ureg

    def create_execution_namespace(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Create a namespace for code execution with Pint and common imports.

        Args:
            context: Existing context/variables to include

        Returns:
            Namespace dictionary for exec()
        """
        namespace = {
            # Pint unit registry
            "ureg": self.ureg,
            "Q_": self.ureg.Quantity,
            # Common math imports
            "pi": 3.141592653589793,
            "e": 2.718281828459045,
            # Common functions
            "sqrt": lambda x: x**0.5,
            "abs": abs,
            "min": min,
            "max": max,
            "sum": sum,
            "round": round,
            # Handcalcs decorator
            "handcalc": handcalc,
            # User context
            **context,
        }

        # Import math functions if needed
        try:
            import math

            namespace.update(
                {
                    "sin": math.sin,
                    "cos": math.cos,
                    "tan": math.tan,
                    "asin": math.asin,
                    "acos": math.acos,
                    "atan": math.atan,
                    "atan2": math.atan2,
                    "sinh": math.sinh,
                    "cosh": math.cosh,
                    "tanh": math.tanh,
                    "exp": math.exp,
                    "log": math.log,
                    "log10": math.log10,
                    "sqrt": math.sqrt,
                    "ceil": math.ceil,
                    "floor": math.floor,
                }
            )
        except ImportError:
            logger.warning("Math module not available")

        return namespace

    def execute_block(
        self, block: CalculationBlock, context: Dict[str, Any]
    ) -> CalculationResult:
        """Execute a single calculation block.

        Args:
            block: The calculation block to execute
            context: Existing variable context

        Returns:
            CalculationResult with execution results
        """
        start_time = time.time()

        # Create namespace
        namespace = self.create_execution_namespace(context)

        # Capture stdout
        stdout_capture = io.StringIO()

        try:
            # Execute the code
            with redirect_stdout(stdout_capture):
                exec(block.code, namespace)

            # Extract results (exclude builtins and imports)
            result_vars = {
                k: self._serialize_value(v)
                for k, v in namespace.items()
                if not k.startswith("_")
                and k
                not in [
                    "ureg",
                    "Q_",
                    "pi",
                    "e",
                    "sqrt",
                    "abs",
                    "min",
                    "max",
                    "sum",
                    "round",
                    "handcalc",
                    "sin",
                    "cos",
                    "tan",
                    "asin",
                    "acos",
                    "atan",
                    "atan2",
                    "sinh",
                    "cosh",
                    "tanh",
                    "exp",
                    "log",
                    "log10",
                    "ceil",
                    "floor",
                ]
            }

            # Try to generate LaTeX using handcalcs
            latex = self._try_generate_latex(block.code, namespace)

            execution_time = time.time() - start_time

            return CalculationResult(
                success=True,
                latex=latex,
                result=result_vars,
                output=stdout_capture.getvalue(),
                execution_time=execution_time,
            )

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Calculation error: {e}", exc_info=True)

            return CalculationResult(
                success=False,
                error=f"{type(e).__name__}: {str(e)}",
                output=stdout_capture.getvalue(),
                execution_time=execution_time,
            )

    def _try_generate_latex(self, code: str, namespace: Dict[str, Any]) -> str | None:
        """Attempt to generate LaTeX representation using handcalcs.

        Args:
            code: The Python code
            namespace: Execution namespace

        Returns:
            LaTeX string or None if generation fails
        """
        try:
            # Create a wrapper function for handcalcs
            func_code = f"""
@handcalc(jupyter_display=False)
def _calc():
{chr(10).join('    ' + line for line in code.splitlines())}
    return locals()
"""
            exec(func_code, namespace)
            latex_result = namespace["_calc"]()

            # handcalcs returns tuple (latex, locals)
            if isinstance(latex_result, tuple) and len(latex_result) >= 1:
                return latex_result[0]

            return None

        except Exception as e:
            logger.debug(f"LaTeX generation failed: {e}")
            return None

    def _serialize_value(self, value: Any) -> Any:
        """Serialize a value for JSON response.

        Args:
            value: Value to serialize

        Returns:
            JSON-serializable representation
        """
        # Handle Pint quantities
        if isinstance(value, pint.Quantity):
            return {
                "magnitude": float(value.magnitude),
                "units": str(value.units),
                "formatted": f"{value:~P}",
            }

        # Handle common numeric types
        if isinstance(value, (int, float, str, bool, type(None))):
            return value

        # Handle lists/tuples
        if isinstance(value, (list, tuple)):
            return [self._serialize_value(item) for item in value]

        # Handle dicts
        if isinstance(value, dict):
            return {k: self._serialize_value(v) for k, v in value.items()}

        # Fallback: string representation
        return str(value)


# Singleton instance
calculation_engine = CalculationEngine()
