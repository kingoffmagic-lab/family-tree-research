---
name: family-tree-research
description: Research family history, interpret existing trees and documents, distinguish namesakes, and build source-cited kinship trees, especially for the former USSR and Russian Empire. Use for ancestry, historical archive searches, conflicting relationships, and GEDCOM reports; not current-person tracking.
license: MIT
---

# Family Tree Research

One portable skill; all research instructions, catalogues, templates and core scripts are bundled. No separate skill installation, connector, account or API key is required. Live research still requires the host's web tools. Reply in the user's language.

## Load and resolve

Treat the directory containing **this file** as the skill root. Resolve every referenced file from its containing document; invoke scripts by their absolute resolved paths, regardless of the shell's current directory. Do not assume a particular home directory, operating system, browser, model, tool name or skill registry.

Read [policy](guides/policy.md), then the bundled [research engine](vendor/ex-ussr-kinship-research/SKILL.md). Those are ordinary local files: read them directly even if the host cannot invoke nested skills. Project policy governs access and privacy; upstream governs evidence reasoning. Use the pinned copy; check or replace dependencies only for an explicit maintenance request.

## Research loop

1. **Understand the question and inputs.** Ask what materials already exist if not supplied. Read provided trees, GEDCOM, documents and family accounts as leads; preserve originals. Extract people, competing identities, event dates/places, claimed relationships, sources and unresolved links. A tree's assertion is not proof.
2. **Start or resume one private case.** Read [case management](guides/workflows.md). Initialize outside the skill with `scripts/init_case.py --case-dir <case> --research-question <question>`. Resume existing registers and searches instead of resetting them. An old `toolkit_path` is a location hint; if moved, use the currently loaded skill root.
3. **Choose a useful check.** Consult both [regional archives](regional-archives/README.md) and [other sources](resources/README.md) by historical place, event date and record type. Use the [volost lookup](regional-archives/historical/finding-a-volost.md) for changed boundaries or names. Catalogue coverage remains partial; a keyword match is not a custody decision.
4. **Read and preserve evidence.** Use available web, image and document tools. Save permitted local evidence with provenance, date, reference and checksum; log empty and blocked searches. Keep original spellings, uncertain readings and alternatives. Separate namesakes until distinguishing evidence supports an identity decision.
5. **Evaluate each relationship.** Follow the bundled evidence protocol. Separate identity resolution from kinship. Check each edge, source dependence and contradictory records; preserve biological, legal, adoptive and household distinctions. No automatic mergers or confidence percentages.
6. **Audit and explain.** Run `scripts/audit_evidence.py --case-dir <case>`. Integrity errors require correction; honest evidence warnings remain. Explain the sourced relationship chain, alternatives, searched coverage, blocked routes and next useful checks. Save the resume position and avoid repeating searches without a new reason.
7. **Deliver the requested view.** Read [output conventions](guides/results.md) for the offline tree/report and GEDCOM exporter. Default outputs exclude living and unknown-status people. Private output requires the user's request; nothing publishes results.

Continue useful authorized research while optional questions await answers. Stop when the question is answered at its recorded evidence level, useful reachable routes are exhausted, or the user stops the task. A gap is a valid result.

## Host capabilities

- **Files and Python 3.9+:** core scripts use only the standard library. Optional upstream tools document their own dependencies.
- **No shell/Python:** maintain the bundled CSV templates with available file tools; perform the audit rules manually and label the automated audit unrun. Do not claim generated exports or executed checks.
- **No web:** analyze supplied material and local references; identify proposed search routes without claiming they were checked.
- **No reliable image/document reader:** retain the source and mark `needs-vision`; do not invent a reading.
- **No persistent files:** provide a source-cited provisional analysis and say it was not saved as a case. Do not imply durable registers or resumability.

No model delegation is required. For installation or host integration, see [compatibility](guides/compatibility.md).
