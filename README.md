# Family Tree Research

Self-contained agent skill built on [ex-ussr-kinship-research](vendor/ex-ussr-kinship-research/SKILL.md).

[Русский](README.ru.md) · [Regional archives](regional-archives/README.md) · [Other sources](resources/README.md) · [Coverage](regional-archives/COVERAGE.md)

Install the whole folder as `family-tree-research`; see [Claude, Codex and other hosts](guides/compatibility.md). Keep real family data outside this checkout. Python 3.9+; core tools use the standard library.

Tell your agent:

> Read SKILL.md. Help me understand my family tree, identify unsupported relationships, and research the next useful question.

```sh
python3 scripts/init_case.py --case-dir ../my-case --research-question "Who were my ancestor's parents?"
python3 scripts/audit_evidence.py --case-dir ../my-case
python3 scripts/build_results.py --case-dir ../my-case
python3 scripts/export_gedcom.py --case-dir ../my-case --out ../my-case/output/tree.ged
```

Default outputs exclude living and unknown-status people. `--private-output` includes them for private use. Review citations before sharing. Nothing publishes or uploads results.

[Policy](guides/policy.md) · [Outputs](guides/results.md) · [Case workflow](guides/workflows.md)

The archive directory covers 15 former Soviet republics plus Poland and Finland. Coverage is partial; it does not promise all surviving records or open scans.

## Checks

```sh
python3 scripts/validate_catalogue.py
python3 scripts/render_catalogue.py --check
python3 -m unittest discover -s tests
```

Upstream files are pinned in upstream-lock.json. Unused translated READMEs, cover art and eval fixtures are omitted; retained files are unchanged. See [contributing](CONTRIBUTING.md). Upstream: Denis Shiryaev and contributors, [MIT](vendor/ex-ussr-kinship-research/LICENSE).

The interactive tree and cited report share one offline file: `output/report.html`.

Ask relatives which documents exist, who supplied each account, and how exact the dates and place names are. Preserve whole-page originals and work on copies; leave unknowns unknown.

Try the wholly fictional demo with `python3 scripts/demo.py --case-dir ../demo-case`, then run the audit and output commands above. Its people, dates and `.invalid` source are teaching fixtures, not historical evidence.
