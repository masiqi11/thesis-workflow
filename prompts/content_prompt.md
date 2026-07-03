# Thesis Content Prompt

Use this prompt for internal consistency checking of the full thesis.

## Objective
Verify that facts, terminology, parameters, metrics, and claims are consistent
across chapters AND consistent with the real project (code + results).

## Stage in pipeline
Runs at `/thesis-content` (stage 6), after all chapters are drafted and before
`/thesis-citations`. Boundary vs later stages:
- `/thesis-content` = internal consistency + code-reality match (offline, no web)
- `/thesis-citations` = reference truth (online)
- `/thesis-audit` = AI-risk synthesis over both reports

## Inputs (mandatory)

| Path | Provider |
|---|---|
| `thesis/*.md` | `/thesis-write` — all chapters |
| `thesis/notes/chapter_evidence_map.md` | `/thesis-write` |
| `thesis/notes/metric_tables.md` | `/thesis-data` — ground-truth numbers |
| project codebase | user's project |

## Checks

1. **模型名一致**：same model referred to identically everywhere (cf. docs/TERMINOLOGY.md)
2. **数据集口径一致**：sizes/splits identical in abstract, body, tables, conclusion
3. **参数一致**：hyperparameters in text match configs/scripts in the codebase
4. **指标一致**：every metric in text matches `metric_tables.md` exactly (rounding rule stated)
5. **功能与代码匹配**：claimed system capabilities exist in the code (grep/read to confirm)
6. **摘要-正文-结论口径统一**：no claim appears in abstract/conclusion that the body doesn't support

## Output

### `thesis/notes/content_audit.md` schema

```md
# Content Audit

Status: PASS | FAIL

## Findings

| id | chapter | §loc | type | detail | severity |
|---|---|---|---|---|---|
| C-1 | 4 | §4.2 | metric_mismatch | text says mIoU 0.85, metric_tables says 0.83 | high |
| C-2 | 3 | §3.1 | code_mismatch | claims Redis cache; no redis usage in codebase | high |
| C-3 | 2 | §2.3 | term_drift | "U-Net" vs "Unet" (2 occurrences) | low |

## Summary
- high: N (block progression until fixed)
- low: M (pass to /thesis-audit as P2 candidates)
```

`type` ∈ `metric_mismatch | code_mismatch | param_mismatch | dataset_mismatch |
term_drift | scope_overclaim`

## Passing gate
Zero `high` findings. `low` findings are forwarded, not blocking.

## Token budget
≤ 12k output tokens.

## Prompt Template

```text
You are running the thesis content-consistency check.

Read first:
- thesis/*.md
- thesis/notes/chapter_evidence_map.md
- thesis/notes/metric_tables.md

Then verify against the actual codebase (grep/read — no web access needed):
1. every metric in text ↔ metric_tables.md
2. every claimed capability ↔ code reality
3. every hyperparameter ↔ config/script values
4. terminology and dataset counts consistent across abstract/body/conclusion

Output: thesis/notes/content_audit.md using the schema in this prompt.
Do not edit chapters; report only.

Append to thesis/notes/workflow_state.md:
| content | done | consistent=<yes/no> | <date> | high=<N> low=<M> |
```
