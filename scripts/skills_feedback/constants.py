from __future__ import annotations

from enum import IntEnum


class ExitCode(IntEnum):
    OK = 0
    ERROR = 1


SKILLS_CONFIG_FILENAME = ".skills-config.yaml"
FEEDBACK_DIR_NAME = ".skills-feedback"
RATINGS_FILENAME = "ratings.json"
PROPOSALS_FILENAME = "proposals.json"
SKILL_FILENAME = "SKILL.md"
