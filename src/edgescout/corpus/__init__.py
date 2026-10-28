"""edgescout corpus: pack metadata plus 50 authored edge-cache security skills.

Skills are authored as plain dicts in ``part1``..``part3`` and loaded once
into the validated :class:`~edgescout.model.Skill` shape.
"""

from __future__ import annotations

from typing import Any

from ..model import skill_from_dict
from .part1 import SKILLS as PART1
from .part2 import SKILLS as PART2
from .part3 import SKILLS as PART3

PACK: dict[str, Any] = {
    "name": "edgescout",
    "version": "1.0.0",
    "category": "web-app",
    "license": "MIT",
    "runtime": "Claude Code, opencode, or any agent runtime that loads SKILL.md files",
    "description": (
        "50 validated edge and web-cache security skills for authorized testing: "
        "CDN and proxy layer fingerprinting, cache-key and cache-policy auditing, "
        "shared-cache leak confirmation, hardening and disclosure, with a "
        "profile-to-audit-plan CLI."
    ),
    "expected_skills": 50,
    "meta_keys": ("phase",),
    "requires_verification": False,
}

PHASE_ORDER = (
    "scope",
    "fingerprint",
    "audit",
    "detect",
    "harden",
    "document",
)

SKILLS: list[Any] = [skill_from_dict(raw) for raw in (*PART1, *PART2, *PART3)]
