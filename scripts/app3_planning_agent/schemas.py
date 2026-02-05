"""
Pydantic models for the Multi-Step Planning Agent.

Defines structured schemas for:
- Step: Individual action items with dependencies
- Plan: Complete structured plan with steps
- Critique: Review feedback with gaps, risks, and improvements
"""

from pydantic import BaseModel, Field


class Step(BaseModel):
    """A single step in the plan with dependencies and metadata."""

    number: int = Field(..., description="Step number (1-indexed)")
    title: str = Field(..., description="Brief title for the step")
    description: str = Field(..., description="Detailed description of what to do")
    depends_on: list[int] = Field(
        default_factory=list,
        description="List of step numbers this step depends on"
    )
    estimated_minutes: int = Field(..., description="Estimated time to complete in minutes")
    category: str = Field(
        ...,
        description="Category: 'research', 'execution', or 'review'"
    )


class Plan(BaseModel):
    """A complete structured plan for achieving a goal."""

    goal: str = Field(..., description="The original goal being planned for")
    steps: list[Step] = Field(..., description="Ordered list of steps to achieve the goal")
    total_estimated_minutes: int = Field(
        ...,
        description="Total estimated time for all steps"
    )


class Critique(BaseModel):
    """Critical review of a plan identifying issues and improvements."""

    gaps: list[str] = Field(
        default_factory=list,
        description="Logical gaps or missing steps in the plan"
    )
    risks: list[str] = Field(
        default_factory=list,
        description="Potential risks or obstacles"
    )
    suggested_improvements: list[str] = Field(
        default_factory=list,
        description="Specific suggestions to improve the plan"
    )
