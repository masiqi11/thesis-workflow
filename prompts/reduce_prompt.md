# Thesis Reduce Prompt

Use this prompt for targeted plagiarism-reduction (降重) rewriting that preserves
all factual anchors, experiment numbers, and citation bindings.

## Objective
Reduce repetition and AI-fingerprint patterns in flagged paragraphs without
drifting conclusions, metrics, model names, or dataset names.

## Stage in pipeline
Runs at `/thesis-reduce` (stage 10), after `/thesis-audit` clears P0 items.
Never run before audit — rewriting on unverified content invalidates the evidence map.

## Inputs (mandatory)

| Path | Provider |
|---|---|
| `thesis/*.md` | `/thesis-write` — chapters to reduce |
| `thesis/notes/ai_risk_audit.md` | `/thesis-audit` — P2 "机械化" flags and locations |
| `thesis/notes/chapter_evidence_map.md` | `/thesis-write` — claim ↔ evidence bindings |
| `thesis/notes/template_requirements.md` | `/thesis-intake` — style constraints |

If the audit reports any unresolved P0, halt and return an error — do not rewrite.

## Outputs

| File | Content |
|---|---|
| `thesis/<chapter>_reduced.md` | Rewritten chapter; overwrites draft only after user approval |
| `thesis/notes/reduce_report.md` | Per-paragraph change log (see schema below) |

### `reduce_report.md` schema

```md
| chapter | §section | change_type | original_first_10_words | new_first_10_words | anchor_preserved |
|---|---|---|---|---|---|
| 4 | §4.2 | sentence_restructure | 首先，本文将数据集划分为… | 数据集按 8:1:1 比例划分为… | yes |
| 2 | §2.1 | passive_to_active | 该方法被广泛应用于… | 研究者广泛将该方法用于… | yes |
```

`change_type` ∈ `sentence_restructure | passive_to_active | connector_removal |
synonym_substitution | paragraph_merge | paragraph_split | other`

`anchor_preserved`: must be `yes` for every row; if `no`, do not ship that change.

## Fact anchor invariants (hard rules)

These must not change across any rewrite:

| Category | Examples — do not alter |
|---|---|
| Metrics | mIoU = 0.83, Recall = 0.91, FPS = 24 |
| Dataset names | Dunhuang-Mural 2023, COCO val2017 |
| Model names | U-Net, ResNet-50, YOLOv8n |
| Citation bindings | [1], [2-4], inline `(Zhang et al., 2021)` |
| Experiment claims tied to evidence | "训练集 8000 张" bound to data_inventory.md |

If a rewrite would mutate any of the above: skip it and log in `reduce_report.md`.

## AI fingerprint patterns to target (P2 flags from audit)

1. **机械递进**: "首先/其次/再次/此外/最后" in consecutive sentences → replace with
   semantic transitions or remove connectors entirely
2. **等长对称段落**: every paragraph ≈ same length → vary with short+long alternation
3. **总分总套式**: opening → 3 bullets → closing echo in every paragraph → break with
   figures, direct data statements, or single-focus paragraphs
4. **空洞起首**: "随着 X 的快速发展" / "在当今时代" / "越来越多的研究表明" →
   open with a specific claim, number, or citation instead
5. **过度被动**: 4+ consecutive passive sentences → convert ≥2 to active voice

Address only patterns flagged as P2 in `ai_risk_audit.md` for this session.
Do not proactively hunt unflagged text — scope creep corrupts the evidence map.

## Rewriting principles

- Vary sentence length: mix short (≤15 chars) and long (≥40 chars) sentences in same paragraph.
- Prefer concrete data over abstract description: "mIoU 提升 3.2 个百分点" over
  "实验结果表明性能有所提升".
- Interleave figures/tables: if two consecutive text-only paragraphs can reference
  a figure, add the reference.
- Use domain terminology precisely: never substitute a technical term with a synonym
  if it changes the precise meaning.

## Token budget
Process one chapter per invocation, ≤ 15k tokens output.

## Prompt Template

```text
You are rewriting chapter {N} for plagiarism reduction.

Read first:
- thesis/notes/ai_risk_audit.md       (find P2 flags for chapter {N})
- thesis/notes/chapter_evidence_map.md (fact anchors — do not alter these)
- thesis/{chapter_file}.md             (source to rewrite)

Pre-flight check: if ai_risk_audit.md contains unresolved P0 items, halt immediately.

For each P2-flagged paragraph in chapter {N}:
1. Identify the change_type.
2. Rewrite, preserving all fact anchors (metrics, model names, dataset names, citations).
3. Verify anchor_preserved = yes before logging.
4. Log to reduce_report.md.

Do NOT touch paragraphs not flagged in ai_risk_audit.md.

Output budget ≤ 15k tokens.

Outputs:
- thesis/{chapter_file}_reduced.md
- append rows to thesis/notes/reduce_report.md
```
