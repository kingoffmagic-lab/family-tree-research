# Fictional teaching case

All people, dates and records created by this demo are fictional. The `.invalid` source URL is deliberately unusable and is not evidence.

From the toolkit root:

```sh
python3 scripts/demo.py --case-dir ../fictional-private-case
python3 scripts/audit_evidence.py --case-dir ../fictional-private-case
python3 scripts/build_results.py --case-dir ../fictional-private-case
python3 scripts/export_gedcom.py --case-dir ../fictional-private-case --out ../fictional-private-case/output/tree.ged
```

Expect three deceased candidates in the default tree, one asserted father relationship, one hypothetical relationship, and no living teaching person. GEDCOM keeps the hypothetical link as an explanatory note. The files are generated outside this public checkout.
