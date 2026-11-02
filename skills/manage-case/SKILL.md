---
name: manage-case
description: Start or resume a private family-history case, coordinate research tasks, and integrate evidence handoffs.
---

# Manage a case

Read ../../guides/policy.md, then ../../vendor/ex-ussr-kinship-research/SKILL.md. Continue an existing case rather than initialize over it. For a new case, use ../../scripts/init_case.py with an external destination and one useful research question. Ask what materials already exist once, unless supplied already.

Use the upstream registers in the case root. Read research-state.md, plan/BOARD.md, and relevant search-log.csv entries before continuing. Preserve originals; save working evidence with URLs, access dates, references, checksums, uncertainty, and search coverage.

One agent is sufficient. When the user authorizes collaborators, the integrator alone updates canonical registers. Other researchers write work/<task-id>/handoff.md with task-prefixed provisional IDs using the case templates. Review stale-base differences before integration; assign canonical IDs against the current registers. A second reading checks transcription, not source independence.

At each useful stopping point, audit with ../../scripts/audit_evidence.py, retain honest warnings, update the board and resume position, and name the next useful action. Completion means the question is answered to the recorded evidence level or useful reachable routes and blockers are logged. Avoid repeated searches without a new reason.
