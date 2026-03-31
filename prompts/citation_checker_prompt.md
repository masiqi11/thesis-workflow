# Citation Checker Prompt

Use this prompt when references need existence verification and citation closure checks.

## Objective
Check whether references really exist and whether in-text citations and bibliography entries are mutually consistent.

## Prompt Template

```text
You are the citation checker.

Input:
- in-text citations
- bibliography list
- searchable metadata if available

For each reference:
1. Check title
2. Check authors
3. Check year
4. Check venue / journal / DOI / arXiv / URL
5. Assign one status: verified / partial / unverified / fake-risk

Also check:
- every [n] has a bibliography entry
- every bibliography entry is cited at least once, unless intentionally retained

Output:
- citation_audit.md
- reference_truth_report.md
- unresolved_fake_risk.md
```
