# Thesis Intake Prompt

Use this prompt at the very start — the user's raw input is typically just a
**thesis topic + project background**.

## Objective
First analyze the topic against available evidence (Step 0), then collect all
writing, formatting, citation, and delivery rules before any formal drafting begins.

## Stage in pipeline
Runs at `/thesis-intake` (stage 1) — the true entry point of the whole pipeline.
Downstream stages all depend on the four files this prompt writes.

## Step 0: Topic & background analysis (before the questionnaire)

From the topic + background, produce `thesis/notes/topic_analysis.md`:

1. **题目拆解** — research object / method / expected deliverable
2. **研究问题** — 2-4 answerable RQs, each tagged with the evidence type expected
   to answer it (experiment / system implementation / literature comparison)
3. **可行性对照** — for each RQ, check the user's actual materials (code, data,
   results) and mark evidence status: `充分 / 部分 / 缺失`
4. **创新点候选** — 2-3 candidates, each with a named evidence source; candidates
   without evidence are NOT listed (they become indefensible at the defense)
5. **论文类型初判** — 算法为主 / 系统为主 / 均衡型 (confirmed later by /thesis-outline)

**Gate**: if every RQ's evidence status is `缺失`, the topic does not match the
project — tell the user to adjust the topic or supply materials; do not proceed.

### `topic_analysis.md` schema

```md
# Topic Analysis

## 题目拆解
- 研究对象: ...  / 研究方法: ...  / 预期产出: ...

## 研究问题
| RQ | 问题 | 预期证据类型 | 证据现状 |
|---|---|---|---|
| RQ1 | ... | experiment | 充分 |

## 创新点候选
| # | 候选创新点 | 支撑证据来源 |
|---|---|---|

## 论文类型初判
<算法为主 | 系统为主 | 均衡型> — 一句话理由
```

## Inputs
- Thesis topic + project background (the raw entry input).
- User dialogue (eight required topic groups, see prompt template).
- Optional: any school template files the user supplies (`*.docx`, format spec PDFs).

## Outputs (mandatory paths)

| File | Purpose |
|---|---|
| `thesis/notes/topic_analysis.md` | Step 0 output — topic decomposition, RQs, feasibility, innovation candidates |
| `thesis/notes/intake_requirements.md` | All collected answers, organized by the 8 topic groups |
| `thesis/notes/missing_requirements.md` | Items still unanswered; downstream stages must halt if non-empty |
| `thesis/notes/template_requirements.md` | **Single source of truth** for every formatting decision (typography, headings, figure/table, citations) — read by every later stage |

`template_requirements.md` is required (SKILL.md §"模板要求持久化") even if the user
gave no school template; in that case populate it with the project's chosen defaults.

## Output schemas

### `intake_requirements.md`
```md
# Intake Requirements

## 1. 基本信息
- 论文题目: ...
- 学校 / 学院 / 专业: ...
- 学历层次: 本科 | 硕士 | 其他
- 总字数要求: <number range>
- 论文类型倾向: 算法为主 | 系统为主 | 均衡型 | 待 Skill 判断
...
## 8. 终稿交付要求
- 版本: docx | pdf | 查重稿 | 盲审稿 | 答辩稿
```

### `missing_requirements.md`
```md
## 必须补充
- <item>
## 建议补充
- <item>
## 说明
<one paragraph on why automatic extraction failed>
```

### `template_requirements.md`
```md
# Template Requirements (single source of truth)

## 页面与字体
- 页面: A4
- 页边距: 上 2.54 / 下 2.54 / 左 3.17 / 右 3.17 cm
- 正文字体: 宋体 12 / 1.5 倍行距 / 首行缩进 2 字符
## 标题
- 一级: 黑体三号居中
- 二级: 黑体四号
## 图表公式
- 图题: 图下居中, 「图 章号-序号」
- 表题: 表上居中, 三线表
## 参考文献
- 标准: GB/T 7714-2015
- 文内: 上标 [1] / [1,2] / [1-3]
- 文后排序: 引用顺序
## 终稿
- 版本: docx, pdf
```

## Prompt Template

```text
You are running the thesis intake phase.

Step 0 — topic analysis (do this FIRST, from the topic + background the user gave):
- Decompose the topic (object / method / deliverable).
- Derive 2-4 research questions; tag each with expected evidence type.
- Cross-check each RQ against the user's actual materials: 充分/部分/缺失.
- List 2-3 innovation-point candidates WITH evidence sources; drop unsupported ones.
- Give a preliminary thesis-type call (算法/系统/均衡).
- Write thesis/notes/topic_analysis.md.
- GATE: all RQs 缺失 → topic/project mismatch → stop and tell the user.

Then collect all critical requirements before any formal thesis writing starts.
Do not draft formal thesis content yet.

Ask for the following groups in order:
1. Basic information (含 总字数要求、论文类型倾向)
2. Thesis structure requirements
3. Available materials and project evidence
4. Page layout and typography rules
5. Heading numbering rules
6. Figure / table / formula rules
7. Citation and bibliography rules
8. Final deliverable requirements

Token budget: keep total output under 10k tokens. Tabulate where possible; do not
duplicate user answers prose-style across the three output files.

Mandatory outputs (write all four; create parent dirs if missing):
- thesis/notes/topic_analysis.md
- thesis/notes/intake_requirements.md
- thesis/notes/missing_requirements.md
- thesis/notes/template_requirements.md

Append to thesis/notes/workflow_state.md:
| intake | done | topic_feasible=<yes/no>; must_fill=<N> | <date> | — |

Hard rules:
- If critical formatting or citation rules are missing, list them in
  missing_requirements.md and explicitly halt the formal writing chain.
- template_requirements.md is the single source of truth; later stages MUST read it
  before any formatting decision. Even if the user supplied a docx template, restate
  every actionable rule here as text.
- If the user updates a format rule mid-session, update template_requirements.md
  immediately and announce the change.
```
