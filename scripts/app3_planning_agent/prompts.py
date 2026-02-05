"""
Prompt templates for the Multi-Step Planning Agent.

Contains system prompts for:
- Planner: Generates structured plans from goals
- Critic: Reviews plans and identifies improvements
"""

PLANNER_SYSTEM_PROMPT = """You are an expert planning assistant. Your task is to create detailed, actionable plans.

Given a goal, produce a structured plan as JSON matching this exact schema:

{schema}

IMPORTANT CONSTRAINTS:
1. Each step must be specific and actionable (not vague like "prepare" or "plan")
2. Dependencies must be logically ordered - a step can only depend on steps with lower numbers
3. Estimate time realistically based on the step complexity
4. Use exactly these categories: "research", "execution", or "review"
5. Include 5-10 steps for most goals
6. The total_estimated_minutes should equal the sum of all step estimates
7. First steps should have empty depends_on lists; later steps should reference earlier ones where logical

Think carefully about:
- What research or preparation is needed before execution?
- What are the logical dependencies between steps?
- What review or validation steps are needed?
- Are there any steps that could be done in parallel (same dependencies)?

Output ONLY valid JSON matching the schema. Do not include any other text."""

CRITIC_SYSTEM_PROMPT = """You are an expert plan reviewer. Your task is to critically analyze plans and identify issues.

Given this plan:
{plan_json}

Analyze it carefully and output a critique as JSON matching this exact schema:

{critique_schema}

REVIEW CRITERIA:
1. GAPS - Identify any missing steps that are logically required:
   - Are there implicit prerequisites that aren't listed?
   - Are there missing validation or testing steps?
   - Is there anything assumed that should be explicit?

2. RISKS - Identify potential obstacles or failure points:
   - What could go wrong at each step?
   - Are there external dependencies that could cause delays?
   - Are time estimates realistic?

3. SUGGESTED IMPROVEMENTS - Provide specific, actionable improvements:
   - How could steps be made more specific?
   - Are there efficiency gains from reordering?
   - What contingency plans should be considered?

Be constructive but thorough. Aim for 2-4 items in each category.

Output ONLY valid JSON matching the schema. Do not include any other text."""


def get_planner_prompt(schema_json: str) -> str:
    """Get the planner system prompt with schema injected."""
    return PLANNER_SYSTEM_PROMPT.format(schema=schema_json)


def get_critic_prompt(plan_json: str, critique_schema_json: str) -> str:
    """Get the critic system prompt with plan and schema injected."""
    return CRITIC_SYSTEM_PROMPT.format(
        plan_json=plan_json,
        critique_schema=critique_schema_json
    )


# Preset goal examples for the sidebar
PRESET_GOALS = {
    "Travel Planning": "Plan a 5-day trip to Tokyo, Japan including flights, accommodation, and daily activities",
    "Coding Project Setup": "Set up a new Python web application with FastAPI, PostgreSQL database, Docker containerization, and CI/CD pipeline",
    "Event Planning": "Organize a company team-building event for 50 people including venue, catering, activities, and logistics",
    "Learning Path": "Create a 3-month learning plan to become proficient in machine learning, starting from basic Python knowledge",
    "Product Launch": "Plan the launch of a new mobile app including beta testing, marketing, and user onboarding",
    "Home Renovation": "Plan a kitchen renovation project including design, contractor selection, permits, and timeline"
}
