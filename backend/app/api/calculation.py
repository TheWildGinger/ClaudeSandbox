"""Calculation API endpoints."""

import logging

from fastapi import APIRouter, HTTPException

from app.models.calculation import CalculationRequest, CalculationResponse, CalculationResult
from app.services.calculation_engine import calculation_engine

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/execute", response_model=CalculationResponse)
async def execute_calculations(request: CalculationRequest) -> CalculationResponse:
    """Execute calculation blocks.

    Args:
        request: Calculation request with blocks and context

    Returns:
        Calculation response with results
    """
    try:
        results = []
        context = request.context.copy()

        # Execute blocks sequentially, maintaining context
        for block in request.blocks:
            result = calculation_engine.execute_block(block, context)
            results.append(result)

            # Update context with successful results
            if result.success and result.result:
                # Filter out serialized Pint quantities for context
                # Keep original Pint objects in context for subsequent calculations
                for key, value in result.result.items():
                    if isinstance(value, dict) and "magnitude" in value and "units" in value:
                        # Reconstruct Pint quantity
                        context[key] = (
                            value["magnitude"] * calculation_engine.ureg(value["units"])
                        )
                    else:
                        context[key] = value

        # Serialize the final context for JSON response
        serialized_context = {
            k: calculation_engine._serialize_value(v) for k, v in context.items()
        }

        return CalculationResponse(results=results, final_context=serialized_context)

    except Exception as e:
        logger.error(f"Calculation execution error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Calculation execution failed: {str(e)}")


@router.post("/validate")
async def validate_code(code: str) -> dict:
    """Validate Python code without executing it.

    Args:
        code: Python code to validate

    Returns:
        Validation result
    """
    try:
        compile(code, "<string>", "exec")
        return {"valid": True, "error": None}
    except SyntaxError as e:
        return {
            "valid": False,
            "error": f"Syntax error at line {e.lineno}: {e.msg}",
        }
    except Exception as e:
        return {
            "valid": False,
            "error": str(e),
        }
