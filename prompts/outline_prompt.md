# Thesis Outline Prompt

Use this prompt when building the chapter structure, evidence bindings, and word budget.

## Objective
Lock chapter boundaries, bind evidence/figure/reference sources to each chapter,
determine thesis type, and produce a word budget before any formal writing begins.

## Stage in pipeline
Runs at `/thesis-outline` (stage 3). Runs after `/thesis-data` completes and before
`/thesis-assets`. Thesis type identified here is consumed by all downstream stages.

## Inputs (mandatory file paths)

| Path | Provider |
|---|---|
| `thesis/notes/intake_requirements.md` | `/thesis-intake` — requirements, word count, thesis type hint |
| `thesis/notes/template_requirements.md` | `/thesis-intake` — format rules |
| `thesis/notes/data_inventory.md` | `/thesis-data` — available materials |
| `thesis/notes/experiment_summary.md` | `/thesis-data` — metrics and results |
| `thesis/refs/papers_inventory.md` | `/thesis-data` — reference status |

## Thesis type identification

Determine type from `intake_requirements.md` field "论文类型倾向". If "待 Skill 判断",
infer from project evidence:

| Type | Signal |
|---|---|
| 算法为主型 | Core contribution is model/algorithm; experiment chapter is heaviest |
| 系统为主型 | Core contribution is system design/engineering; system chapter is heaviest |
| 均衡型 | Both algorithm and system chapters are major; overall longer |

Write the chosen type into `thesis_outline.md` at the top and propagate to word budget.

## Word budget rules

Total word count from `intake_requirements.md`. Default reference by degree level:

| Degree | Total (body) |
|---|---|
| 专科 | 8 000–12 000 |
| 本科 | 15 000–25 000 |
| 硕士（专硕） | 25 000–35 000 |
| 硕士（学硕） | 30 000–50 000 |

5-chapter undergrad example at ~20 000 words:

| Chapter | Topic | 算法为主 | 系统为主 | 均衡型 |
|---|---|---|---|---|
| 1 | 绪论 | 2500–3500 | 2500–3500 | 2500–3500 |
| 2 | 相关技术与理论基础 | 3000–4000 | 2500–3500 | 3000–4000 |
| 3 | 系统设计与实现 | 2500–3500 | 4000–5500 | 3500–4500 |
| 4 | 实验与结果分析 | 5000–6500 | 2500–3500 | 4000–5000 |
| 5 | 总结与展望 | 1000–1500 | 1000–1500 | 1000–1500 |

Core rule: the chapter carrying the main contribution should be 25–35% of total.

## Outputs

| File | Content |
|---|---|
| `thesis/notes/thesis_outline.md` | Chapter list, thesis type, word budget table, section goals |
| `thesis/notes/chapter_matrix.md` | Per-chapter evidence/figure/reference bindings |
| `thesis/notes/figure_plan.md` | Figure numbering, captions, source (Python script / prompt / screenshot) |
| `thesis/notes/reference_plan.md` | Which papers go in which chapter, preliminary citation order |

### `thesis_outline.md` required sections

```md
# Thesis Outline

## Thesis Type
<算法为主型 | 系统为主型 | 均衡型> — rationale in one sentence

## Word Budget

| Chapter | Title | Target Words | % of Total |
|---|---|---|---|
| 1 | 绪论 | 3000 | 15% |
...

## Chapter Goals
### Chapter 1 — 绪论
Goal: ...
Key sections: 研究背景, 研究现状, 研究内容与贡献, 论文结构

### Chapter 2 — ...
```

### `chapter_matrix.md` schema

```md
| chapter | section | evidence_type | source_path | figure_ids | ref_ids | notes |
|---|---|---|---|---|---|---|
| 3 | 3.2 U-Net 架构 | paper figure | refs/papers/ronneberger_2015_unet.pdf §3.1 | fig3-1 | [1] | draw from paper, not reproduce |
| 4 | 4.1 数据集 | experiment log | notes/data_inventory.md | — | — | report split counts |
```

### `figure_plan.md` schema

```md
| fig_id | caption | chapter | source_type | source_path | status |
|---|---|---|---|---|---|
| fig2-1 | U-Net 编码器-解码器结构示意图 | 2 | prompt | — | planned |
| fig4-1 | 训练损失曲线 | 4 | python_script | tools/plot_loss.py | planned |
| fig3-1 | 系统架构图 | 3 | screenshot | thesis/figures/sys_arch.png | ready |
```

`source_type` ∈ `prompt | python_script | screenshot | paper_figure | user_supplied`

## Passing gate

Before `/thesis-assets` or `/thesis-write` may proceed:
- All chapters have evidence sources bound in `chapter_matrix.md`
- Word budget sums to within 5% of school requirement
- All figures in `figure_plan.md` have a `source_type` (even if status = planned)
- `thesis_outline.md` states the thesis type explicitly

## Token budget
≤ 12k output tokens across all four files.

## Prompt Template

```text
You are building the thesis outline.

Read these inputs first:
- thesis/notes/intake_requirements.md
- thesis/notes/template_requirements.md
- thesis/notes/data_inventory.md
- thesis/notes/experiment_summary.md
- thesis/refs/papers_inventory.md

Step 1: Determine thesis type (算法为主 / 系统为主 / 均衡型).
  - Use the intake field if set; otherwise infer from project evidence.
  - State the type and rationale in thesis_outline.md.

Step 2: Build the word budget table.
  - Use school word count from intake_requirements.md.
  - Apply the distribution table for the identified thesis type.
  - Ensure total ±5% of school requirement.

Step 3: Write chapter goals and section plans.

Step 4: Build chapter_matrix.md — bind evidence, figures, refs to each section.

Step 5: Build figure_plan.md — list every anticipated figure with source_type.

Step 6: Build reference_plan.md — assign papers to chapters.

Output budget ≤ 12k tokens.

Outputs:
- thesis/notes/thesis_outline.md
- thesis/notes/chapter_matrix.md
- thesis/notes/figure_plan.md
- thesis/notes/reference_plan.md
```
