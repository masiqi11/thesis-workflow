# Thesis Intake Prompt

Use this prompt when thesis requirements are still incomplete.

## Objective
Collect all writing, formatting, citation, and delivery rules before any formal drafting begins.

## Stage in pipeline
Runs at `/thesis-intake` (stage 1). Downstream stages — `/thesis-data`, `/thesis-outline`,
`/thesis-write`, `/thesis-citations`, `/thesis-audit`, `/thesis-format`, `/thesis-build` —
all depend on the three files this prompt writes.

## Inputs
- User dialogue (eight required topic groups, see prompt template).
- Optional: any school template files the user supplies (`*.docx`, format spec PDFs).

## Outputs (mandatory paths)

| File | Purpose |
|---|---|
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

Your job is to collect all critical requirements before any formal thesis writing starts.
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

Mandatory outputs (write all three; create parent dirs if missing):
- thesis/notes/intake_requirements.md
- thesis/notes/missing_requirements.md
- thesis/notes/template_requirements.md

Hard rules:
- If critical formatting or citation rules are missing, list them in
  missing_requirements.md and explicitly halt the formal writing chain.
- template_requirements.md is the single source of truth; later stages MUST read it
  before any formatting decision. Even if the user supplied a docx template, restate
  every actionable rule here as text.
- If the user updates a format rule mid-session, update template_requirements.md
  immediately and announce the change.
```
