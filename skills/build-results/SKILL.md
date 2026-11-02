---
name: build-results
description: Generate offline family trees, cited HTML reports, and GEDCOM exports from reviewed family-history registers.
---

# Build results

Read ../../guides/policy.md and ../../guides/results.md. Use the evidence and GEDCOM references in ../../vendor/ex-ussr-kinship-research/references/ for reasoning and exchange limits.

Audit the external case before output. Run ../../scripts/build_results.py --case-dir <case> and ../../scripts/export_gedcom.py --case-dir <case> --out <case>/output/tree.ged. Use --root-person only for a person present in the selected output view. Existing files require --overwrite.

Default output excludes living and unknown-status people. Use --private-output only for explicitly requested private results. Inspect visible text, embedded data, citations, and media before sharing; no command publishes results. Never copy a real case into examples/.

Check that every displayed relation has the recorded evidence status and citations, conflicting candidates remain distinct, unsupported pedigree edges are not asserted in GEDCOM, and the result opens offline. Explain any exchange loss, unknown parent roles, and unanswered questions. Leave the canonical registers authoritative.
