# Draft and release checklist

1. Run catalogue validation, generated-page checks, unit tests, upstream tests, and the upstream checksum check. Review every source gap rather than changing statuses to make a test pass.
2. Review the release file inventory. Scan for private case paths, personal research names, exact family record URLs, tokens, metadata, and embedded media. Keep case-specific screening terms outside this repository. Inspect binary files and the vendored dependency separately; upstream attribution is retained.
3. Regenerate the fictional example outputs; examine tree, report, GEDCOM, and privacy filtering. Use an independent GEDCOM parser and perform an import in Gramps when available. Record limitations in RELEASE_STATUS.md.
4. Reconcile official regional institution lists and publish unresolved coverage, including stale directory entries and renamed branches. A blocked website stays listed with its limitation.
5. Prepare a private GitHub draft with fresh history. Public publication is a separate user decision. Do not enable public hosting for real cases or upload the private extraction evidence.

Network link checks are optional, separate from deterministic CI, and produce a review report outside the toolkit. A failure never deletes data.
