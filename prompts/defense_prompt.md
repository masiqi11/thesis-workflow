# Thesis Defense Prompt

Use this prompt to distill defense materials from the finished thesis.

## Objective
Extract defense outline, innovation points, and a Q&A bank — every item traceable
to thesis content and evidence, so nothing said at the defense outruns the thesis.

## Stage in pipeline
Runs at `/thesis-defense` (stage 12), after `/thesis-build`.

## Inputs (mandatory)

| Path | Provider |
|---|---|
| `thesis/release/毕业论文_*.docx` or `thesis/*.md` | final thesis |
| `thesis/notes/topic_analysis.md` | `/thesis-intake` — original research questions |
| `thesis/notes/claim_evidence_matrix.md` | `/thesis-audit` — what is actually proven |
| `thesis/notes/metric_tables.md` | `/thesis-data` — defensible numbers |
| `thesis/notes/assets_manifest.md` | `/thesis-assets` — presentable figures |

## Outputs

| File | Content |
|---|---|
| `thesis/notes/defense_outline.md` | 10–15 min presentation skeleton |
| `thesis/notes/innovation_points.md` | 2-3 innovation points, each with evidence pointer |
| `thesis/notes/qa_bank.md` | anticipated questions + evidence-backed answers |

### `innovation_points.md` schema

```md
| # | innovation claim | evidence | thesis §loc | risk if challenged |
|---|---|---|---|---|
| 1 | 改进的跳跃连接使小目标分割 mIoU +3.2pt | metric_tables tab.5 消融行 | §4.3 | 需解释与 baseline 对比条件一致性 |
```

Only claims present in `claim_evidence_matrix.md` with `status = verified` may be
listed as innovations. An unverified innovation claim at defense is a P0-class risk.

### `qa_bank.md` schema

```md
## Q: 为什么选 U-Net 而不是 Transformer 系？
A: <2-4 sentence answer>
Evidence: thesis §2.2 对比段；refs [3][7]
Weak spot: 未做 Transformer 基线实验 — 如被追问，承认为未来工作（§5.2 已写）
```

Cover at minimum: motivation, method choice, experiment design, weakest result,
difference from cited related work, and "what did YOU do vs the framework".

## Hard rules

1. Never invent results for the defense that the thesis doesn't contain.
2. Every answer cites a thesis section or evidence file.
3. Explicitly list weak spots with prepared honest responses — evasion reads worse
   than acknowledged limitations.

## Token budget
≤ 12k output tokens.

## Prompt Template

```text
You are preparing thesis defense materials.

Read first:
- thesis chapters (final)
- thesis/notes/{topic_analysis,claim_evidence_matrix,metric_tables,assets_manifest}.md

Produce:
1. defense_outline.md — presentation skeleton mapped to the original research questions
2. innovation_points.md — only verified claims; each with evidence pointer + challenge risk
3. qa_bank.md — Q/A/Evidence/Weak-spot blocks for the mandatory coverage list

Hard rule: no claim beyond the thesis. Cite §loc or evidence file for every answer.

Append to thesis/notes/workflow_state.md:
| defense | done | materials_ready=yes | <date> | — |
```
