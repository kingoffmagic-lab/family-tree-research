# Result conventions

The canonical upstream registers remain the source of research state. The renderer runs their audit before building a view. Integrity errors stop generation; evidence warnings remain visible and do not cause artificial status promotion.

The offline tree displays recorded parent and spouse edges and supports zoom, search, and person details. Hypotheses and unresolved edges are visually distinct. A person's identity and an edge's status are separate.

Default sharing mode uses only explicitly deceased people and a minimal field set. It omits free-form biographies, local media, and artifacts linked to excluded people. Known excluded names are redacted from displayed citations. Private mode can include all registered people. Neither mode publishes anything. Manually inspect citations and URLs before sharing.

GEDCOM 5.5.1 uses UTF-8. Parent-child families are emitted only for single-source or stronger, non-contradicted relationships; other relationships remain explanatory notes. Explicit father/mother relationship types or optional documented `sex` CSV values supply exchange roles. When a parent role is unknown, the export preserves an ASSO/RELA association rather than inventing a father or mother. This is an exchange limitation: review associations in the receiving program. A family container does not assert marriage; marriage is added only from an explicit spouse relationship. Household-only links do not become biological parentage.

Output paths must be outside the toolkit and cannot overwrite register files or supplied originals. Existing output files require --overwrite. For GEDCOM, source citations refer back to evidence IDs; the CSV registers retain the full uncertainty model which GEDCOM cannot represent losslessly.

The interactive tree and cited report share one offline file: `output/report.html`.

Gramps import remains an outstanding release check; the fictional export was independently parsed with ged4py.
