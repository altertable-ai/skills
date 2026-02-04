import asyncio
from collections.abc import Sequence
from pathlib import Path

import litellm
from pydantic import BaseModel

from .models import (
    MAX_RETRIES,
    RETRY_DELAY,
    Issue,
    ScoreBreakdown,
    ScoreResult,
    SkillContent,
)

DEFAULT_MODEL = "gemini/gemini-flash-latest"

PROMPT_TEMPLATE = """You are an expert evaluator of Agent Skills per agentskills.io specification.

Evaluate this skill and score 0-100.

## Rubric (100 points)

### Frontmatter (20 points)
- name: lowercase, hyphens only, 1-64 chars, matches directory name
- description: 1-1024 chars, describes what skill does AND when to use it, includes trigger keywords

### Structure (25 points)
- Step-by-step instructions for agents
- Examples of inputs and outputs
- Common edge cases handled
- Under 500 lines (detailed content in references/)

### Content Quality (35 points)
- Clear, actionable instructions agents can follow
- Concrete examples with expected outcomes
- Good markdown formatting
- Progressive disclosure (main content concise, details in references)

### Edge Cases (10 points)
- Documents common pitfalls and how to avoid them
- Handles error scenarios gracefully
- Includes troubleshooting guidance

### References (10 points)
- Detailed documentation in references/ directory
- Files are focused and under 5000 tokens each
- One level deep (no nested reference chains)

## Skill: {skill_name} ({line_count} lines)
```markdown
{skill_content}
```

## References ({ref_count})
{reference_files}

Respond with JSON only:
{{"score": N, "breakdown": {{"frontmatter": N, "structure": N, "content_quality": N, "pitfalls": N, "references": N}}, "issues": [{{"severity": "critical|major|minor", "message": "..."}}], "suggestions": ["..."]}}"""  # noqa: E501


class EvaluationResponse(BaseModel):
    score: int
    breakdown: ScoreBreakdown
    issues: list[Issue]
    suggestions: list[str]


async def score_skill(skill_path: Path, model: str | None = None) -> ScoreResult:
    skill = SkillContent.from_path(skill_path)
    model_name = model or DEFAULT_MODEL
    response = await _evaluate(skill, model_name)

    return ScoreResult(
        skill_name=skill.name,
        score=response.score,
        breakdown=response.breakdown,
        issues=response.issues,
        suggestions=response.suggestions,
        judge_name=model_name,
    )


async def score_batch(skill_paths: Sequence[Path], model: str | None = None) -> list[ScoreResult]:
    tasks = [score_skill(path, model) for path in skill_paths]
    return await asyncio.gather(*tasks)


async def _evaluate(skill: SkillContent, model: str) -> EvaluationResponse:
    prompt = _build_prompt(skill)

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


def _build_prompt(skill: SkillContent) -> str:
    ref_text = "None"
    if skill.references:
        ref_parts = []
        for name, content in skill.references.items():
            ref_parts.append(f"### {name}\n{content}")
        ref_text = "\n\n".join(ref_parts)

    return PROMPT_TEMPLATE.format(
        skill_name=skill.name,
        skill_content=skill.content,
        line_count=skill.line_count,
        reference_files=ref_text,
        ref_count=len(skill.references),
    )
