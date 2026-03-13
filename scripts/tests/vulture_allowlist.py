from skills_feedback.api import (  # noqa: F401
    apply,
    check,
    propose_add_skill,
    propose_modify_skill,
    propose_remove_skill,
    rate,
)
from skills_feedback.cli import Propose, SkillsFeedback  # noqa: F401
from skills_feedback.models import Proposal  # noqa: F401

# API module public functions
rate
propose_add_skill
propose_modify_skill
propose_remove_skill
apply
check

# CLI methods called by Python Fire
_p = Propose()
_p.add
_p.modify
_p.remove

_sf = SkillsFeedback()
_sf.propose
_sf.rate
_sf.apply

# Pydantic model fields
Proposal.proposed_by
Proposal.proposed_at
