# Contributing

Contribute general research resources and corrections with institutional evidence. Real family records, searches, screenshots, exact scan links, personal paths, and correspondence belong in private cases.

For regional archives, edit regional-archives/data/archives.json and its jurisdiction/coverage records. Distinguish authority, repository, branch, and service office. Cite an official directory or finding aid for each factual holding statement. Unknown dates, languages, access, or custody remain explicitly unknown. Record former names and transfers only when sourced.

For other resources, edit resources/sources.json. A general catalogue entry is not independent evidence of an ancestor. Preserve mirrors as related services when they add useful access; merge aliases of the same institution.

Run `python3 scripts/render_catalogue.py` and `python3 scripts/validate_catalogue.py`. Generated Markdown is a view, not a second editable dataset. Include a dated explanation when a region's institution list has been reconciled. Do not mark it complete merely because one archive has a working homepage.

Upstream changes: choose an explicit public commit, review its policy and schema changes, replace the vendored tracked files without modifications, regenerate upstream-lock.json, and run upstream and starter tests. Changes to research methodology belong upstream; project access restrictions remain in guides/policy.md.
