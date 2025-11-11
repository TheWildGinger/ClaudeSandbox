"""Calculation data models."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class CalculationBlock(BaseModel):
    """A single calculation block from the document."""

    id: Optional[str] = None  # Optional identifier
    code: str  # Python code to execute
    language: str = "python"  # For future extensibility


class CalculationResult(BaseModel):
    """Result of executing a calculation block."""

    success: bool
    latex: Optional[str] = None  # LaTeX representation from handcalcs
    result: Optional[Dict[str, Any]] = None  # Variable values after execution
    output: Optional[str] = None  # Stdout/print output
    error: Optional[str] = None  # Error message if failed
    execution_time: float = 0.0  # Seconds


class CalculationRequest(BaseModel):
    """Request to execute calculation(s)."""

    blocks: List[CalculationBlock]
    context: Dict[str, Any] = Field(default_factory=dict)  # Persistent variables between blocks


class CalculationResponse(BaseModel):
    """Response containing calculation results."""

    results: List[CalculationResult]
    final_context: Dict[str, Any]  # Final state of variables
