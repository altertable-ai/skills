import asyncio
from collections.abc import Sequence
from pathlib import Path

import litellm
from pydantic import BaseModel

from .models import (
    DEFAULT_MODEL,
    MAX_RETRIES,
    RETRY_DELAY,
    Issue,
    ScoreBreakdown,
    ScoreResult,
    SkillContent,
)

litellm.suppress_debug_info = True  # type: ignore[assignment]

PROMPT_TEMPLATE = """You are an expert evaluator of Agent Skills per agentskills.io specification.

## Agent Skills Specification (from agentskills.io)

{spec_context}

## Evaluation Instructions

Evaluate the skill below against the specification and best practices above. Score 0-100.

### Scoring Breakdown (100 points)

- Frontmatter (20): Compliance with spec field constraints, naming, and precise activation triggers
- Structure (25): Concise, executable workflow with ordering only where it affects correctness
- Content Quality (35): Accurate, actionable, non-obvious platform context and clear operation boundaries
- Pitfalls (10): Operational safeguards, permissions, side effects, and easy-to-miss platform behavior
- References (10): Progressive disclosure used well when conditional detail is necessary

Do not reward generic tutorials, arbitrary section checklists, or exhaustive copies of tool parameters. Assume the agent already knows common analytics, SQL, API, and software-engineering concepts. Reward details that are specific to the product and materially change execution. Prefer instructions that defer evolving contracts to live tool schemas or current documentation.

References are optional. Award full reference credit when the entry point is self-contained and no conditional detail warrants a separate file; do not reward references merely for existing.

## Skill: {skill_name} ({line_count} lines)
```markdown
{skill_content}
```

## References ({ref_count})
{reference_files}

Award each dimension a score up to its maximum. The total is their sum.

Respond with JSON only:
{{"breakdown": {{"frontmatter": N, "structure": N, "content_quality": N, "pitfalls": N, "references": N}}, "issues": [{{"severity": "critical|major|minor", "message": "..."}}], "suggestions": ["..."]}}"""  # noqa: E501


class EvaluationResponse(BaseModel):
    breakdown: ScoreBreakdown
    issues: list[Issue]
    suggestions: list[str]


async def score_skill(skill_path: Path, spec_context: str, model: str | None = None) -> ScoreResult:
    skill = SkillContent.from_path(skill_path)
    model_name = model or DEFAULT_MODEL
    response = await _evaluate(skill, model_name, spec_context)

    return ScoreResult(
        skill_name=skill.name,
        score=response.breakdown.total,
        breakdown=response.breakdown,
        issues=response.issues,
        suggestions=response.suggestions,
        judge_name=model_name,
    )


async def score_batch(
    skill_paths: Sequence[Path], spec_context: str, model: str | None = None
) -> list[ScoreResult]:
    tasks = [score_skill(path, spec_context, model) for path in skill_paths]
    return await asyncio.gather(*tasks)


async def _evaluate(skill: SkillContent, model: str, spec_context: str) -> EvaluationResponse:
    prompt = _build_evaluation_prompt(skill, spec_context)

    last_error: Exception | None = None
    for attempt in range(MAX_RETRIES):
        try:
            response = await litellm.acompletion(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                response_format=EvaluationResponse,
            )
            return EvaluationResponse.model_validate_json(response.choices[0].message.content)
        except Exception as err:
            last_error = err
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(RETRY_DELAY * (attempt + 1))

    raise ValueError(f"Failed after {MAX_RETRIES} attempts: {last_error}")


def _build_evaluation_prompt(skill: SkillContent, spec_context: str) -> str:
    ref_text = (
        "\n\n".join(f"### {name}\n{content}" for name, content in skill.references.items())
        or "None"
    )

    return PROMPT_TEMPLATE.format(
        spec_context=spec_context,
        skill_name=skill.name,
        skill_content=skill.content,
        line_count=skill.line_count,
        reference_files=ref_text,
        ref_count=len(skill.references),
    )
