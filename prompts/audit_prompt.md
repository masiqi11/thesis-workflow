# Thesis Audit Prompt

Use this prompt when the full thesis needs AI-risk and evidence review.

## Objective
Detect hallucinated implementation claims, fabricated experiments, inconsistent
metrics, terminology drift, and unsupported conclusions.

## Stage in pipeline
Runs at `/thesis-audit` (stage 8), after `/thesis-citations` (stage 7) and BEFORE
`/thesis-reduce` (stage 9) and `/thesis-format` (stage 10) — reduce consumes this
audit's P2 flags, and format requires this audit's P0 count to be zero.

Consumes — does NOT regenerate — the citation truth report. Reference fact-checking
is owned exclusively by `/thesis-citations` (citation_checker_prompt.md). If audit
finds suspect refs, it logs them to `prioritized_fix_list.md` and refers back; it
does not call search/fetch tools itself.

## Inputs (mandatory file paths)

| Path | Provider |
|---|---|
| `thesis/*.md` | `/thesis-write` — full chapter drafts |
| `thesis/notes/chapter_evidence_map.md` | `/thesis-write` — claim ↔ evidence rows |
| `thesis/notes/citation_audit.md` | `/thesis-citations` — citation closure check |
| `thesis/notes/reference_truth_report.md` | `/thesis-citations` — per-ref truth status |
| `thesis/notes/metric_tables.md` | `/thesis-data` — ground-truth experiment numbers |
| project codebase + experiment logs | user / `/thesis-data` |

## Outputs

| File | Purpose |
|---|---|
| `thesis/notes/ai_risk_audit.md` | findings grouped by dimension (see below) |
| `thesis/notes/claim_evidence_matrix.md` | full claim → evidence join (extends chapter_evidence_map) |
| `thesis/notes/prioritized_fix_list.md` | ordered fix queue |

### `ai_risk_audit.md` schema

```md
## P0 — must-fix (blocks build)
- [chapter §section] <finding> — evidence: <pointer>
## P1 — should-fix (blocks final review)
- ...
## P2 — nice-to-fix (style/terminology)
- ...
```

### `claim_evidence_matrix.md` schema

```md
| chapter | claim | source_file | source_loc | status | severity |
|---|---|---|---|---|---|
```

`status` enum (joins with chapter_evidence_map): `verified | partial | unverified | fake-risk`
`severity` enum: `P0 | P1 | P2 | none`.

### `prioritized_fix_list.md` schema

```md
1. [P0] chapter 4 §4.2: mIoU=0.83 lacks supporting metric_tables row
2. [P0] chapter 2 §2.3: ref [7] flagged fake-risk in reference_truth_report.md — replace or remove
3. [P1] chapter 3 §3.1: terminology drift "U-Net" vs "Unet" (3 occurrences)
4. [P2] chapter 5: 句式过于模板化
```

## Severity decision rules

| Severity | Trigger |
|---|---|
| **P0** | Fake implementation, fake experiment number, ref flagged `fake-risk` and unprocessed, claim with `unverified` status that is also load-bearing in conclusion/abstract |
| **P1** | Metric value inconsistent across abstract/body/conclusion, wrong figure interpretation, ref status = `partial` and chapter relies on it |
| **P2** | Terminology drift not affecting meaning, vague wording, sentence templates flagged by AI-risk regex |

P0 must be cleared before `/thesis-format`. P1 must be cleared or explicitly downgraded
with rationale before `/thesis-build`. P2 is advisory.

## Audit dimensions
1. implementation vs code reality
2. experiment claims vs actual outputs (`metric_tables.md`)
3. metrics consistency across abstract/body/conclusion
4. terminology consistency (see docs/TERMINOLOGY.md for examples of drift)
5. figure/table interpretation correctness
6. unsupported or exaggerated conclusions
7. cross-reference with `reference_truth_report.md` (do **not** re-verify, only flag
   unprocessed `fake-risk` / `partial` refs that the chapter depends on)
8. figure data provenance: every `source_type = python_script` figure in
   `figure_plan.md` must have a script under `thesis/figures/scripts/` whose data
   source traces to `metric_tables.md` or a real results file — a plot with no
   traceable data source is a P0 (fabricated experiment visual)

## Token budget
≤ 20k output tokens total across all three files.

## Prompt Template

```text
You are the thesis auditor.

Read these inputs first:
- thesis/*.md
- thesis/notes/chapter_evidence_map.md
- thesis/notes/citation_audit.md
- thesis/notes/reference_truth_report.md
- thesis/notes/metric_tables.md

Boundaries:
- You consume reference_truth_report.md; you do NOT call search/fetch tools to
  re-verify references. If a ref looks suspect but is marked verified, log a P1
  pointing back to /thesis-citations.
- You do not edit chapter files; you only produce audit reports.

Apply the severity table from this prompt to assign P0/P1/P2.
Output budget ≤ 20k tokens.

Outputs:
- thesis/notes/ai_risk_audit.md     (findings by P0/P1/P2)
- thesis/notes/claim_evidence_matrix.md  (full claim ↔ evidence join)
- thesis/notes/prioritized_fix_list.md   (ordered fix queue)
```
