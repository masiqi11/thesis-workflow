# Templates — Intake Questionnaire & Sub-skill I/O Contracts

本文档抽取自 SKILL.md，集中存放可复用模板。修改这里即可同步影响所有阶段。

## `/thesis-intake` 标准问卷

建议按以下顺序采集，未答完不得进入正式正文。

```md
# 论文写作需求采集表

## A. 基本信息
- 论文题目：
- 学校/学院/专业：
- 学历层次：
- 作者姓名：
- 指导教师：
- 截止时间：
- 总字数要求：
- 论文类型（算法为主/系统为主/均衡型/不确定）：

## B. 结构要求
- 固定章节数：
- 必要项（默认包含，除非明确排除）：中文摘要、英文 Abstract、目录、结论、致谢、参考文献
- 是否需要前言：
- 是否需要附录：

## C. 材料来源
- 是否基于现有项目反推：
- 可用材料清单：
- 已定稿部分：
- 待重写部分：

## D. 排版规则
- 页面大小：
- 页边距：
- 正文字体字号：
- 标题字体字号：
- 行距/段距：
- 首行缩进：
- 页码规则：

## E. 标题编号
- 一级标题：
- 二级标题：
- 三级标题：
- 四级标题：
- 目录层级：

## F. 图表公式
- 图题位置：
- 表题位置：
- 图表编号格式：
- 三线表规则：
- 公式编号规则：

## G. 引用规则
- 文献标准（如 GB/T 7714-2015、APA、IEEE）：
- 编号制/作者年制：
- 文内引用标记格式（如 `[1]`、`[1,2]`、`[1-3]`、`(作者, 年)`）：
- 引用标记位置（标点前/后、上标/平标）：
- 文后排序方式：
- 网页/GitHub/arXiv 是否允许：
- 参考文献条目必需字段：

## H. 交付要求
- 输出版本：
- 是否需要盲审稿：
- 是否需要查重稿：
- 是否需要答辩 PPT：
```

## 子 Skill 输入/输出契约

### `/thesis-intake`
- 输入：论文题目 + 项目背景（原始入口）、用户口述要求、学校规范、模板说明、文字版格式条目
- 输出：`topic_analysis.md`（题目拆解/研究问题/可行性/创新点候选）、`intake_requirements.md`、`missing_requirements.md`、`template_requirements.md`
- 通过条件：至少一个研究问题证据现状非"缺失"；关键格式规则已明确，缺失项不含"必须补充"，模板要求已持久化到文件

### `/thesis-data`
- 输入：项目代码、实验日志、结果目录、截图入口、环境信息、论文主题与研究方向
- 输出：`data_inventory.md`、`experiment_summary.md`、`metric_tables.md`、`runtime_env.md`、`papers_inventory.md`、`papers_to_download.md`、`paper_data_extracts.md`、`thesis/refs/papers/`
- 通过条件：关键实验指标、数据集规模、运行环境、可用图表已落盘；引用论文已检索收集，至少核心文献为 `metadata-only` 或 `downloaded` 状态；需手动下载的文献已通知用户

### `/thesis-outline`
- 输入：intake 结果、项目证据、材料清单、学历层次与学校字数要求
- 输出：`thesis_outline.md`（含字数规划表）、`chapter_matrix.md`、`figure_plan.md`、`reference_plan.md`
- 通过条件：每章目标、证据源、图表源、参考文献源已绑定；论文类型已识别；各章字数预算已明确且总字数符合学校要求

### `/thesis-assets`
- 输入：图表原图、截图、表格数据、`figure_plan.md`
- 输出：`assets_manifest.md`（含 `data_provenance` 列）、规范化后的 `thesis/figures/*`、
  实验图生成脚本 `thesis/figures/scripts/*.py`
- 通过条件：图号连续、图题明确、正文引用可追踪、低质量图片已剔除；
  每张实验数据图的 `data_provenance` 指向真实数据文件（无法溯源的图不得入库）

### `/thesis-write`
- 输入：outline、证据矩阵、图表计划、章节目标字数、`template_requirements.md`、`papers_inventory.md`、`figure_plan.md`、`chapter_matrix.md`
- 输出：章节 Markdown、`chapter_evidence_map.md`、`thesis/refs/references.md`（增量维护）、`unresolved_issues.md`
- 通过条件：每章均附证据来源，未证实内容已显式标记；正文与图表强耦合，图号与图题已内联；引用文献状态已同步；本章 unverified 占比 ≤ 30%（超过即拒绝出稿，回退给 researcher 补证据）

### `/thesis-content`
- 输入：全文章节、代码实现、实验结果、系统截图
- 输出：`content_audit.md`
- 通过条件：模型名、数据集、参数、指标、系统功能口径一致

### `/thesis-citations`
- 输入：正文引用、`thesis/refs/references.md`、联网搜索结果
- 输出：`citation_audit.md`、`reference_truth_report.md`、`references_checked.md`、`unresolved_fake_risk.md`
- 通过条件：不存在 `fake-risk` 未处置条目（`unresolved_fake_risk.md` 为空），正文与文后引用双向闭合

### `/thesis-audit`
- 输入：全文、项目代码、实验数据、`citation_audit.md`、`reference_truth_report.md`、`figure_plan.md`
- 输出：`ai_risk_audit.md`、`claim_evidence_matrix.md`、`prioritized_fix_list.md`
- 通过条件：P0 清零，P1 已修复或显式降级说明；实验图数据溯源全部可追（脚本 + 数据源）
- 与 `/thesis-citations` 边界：`/thesis-audit` 不重复执行联网真值核验，
  仅消费 `reference_truth_report.md`，做跨章/跨段一致性与"断言↔证据"的复核。

### `/thesis-reduce`（可选；audit 之后、format 之前）
- 输入：`ai_risk_audit.md` 的 P2 标记段落、原文、`chapter_evidence_map.md`（事实锚点）
- 输出：`<chapter>_reduced.md`（确认后替换原章节文件）、`reduce_report.md`、
  **同步更新后的** `chapter_evidence_map.md`
- 通过条件：`reduce_report.md` 全部行 `anchor_preserved = yes`；证据映射 `source_loc`
  与改写后文本一致；无残留 `_reduced.md` 文件

### `/thesis-format`（最后一道文本闸门；任何改文本步骤之后必须重跑）
- 输入：规范章节文件（降重已合并）、图表资产、`template_requirements.md`、`ai_risk_audit.md`（P0 必须为 0）
- 输出：`format_audit.md`（PASS/FAIL/BLOCKED）、`format_ready_chapters.md`
- 通过条件：10 维度检查零 FAIL；本阶段**不产出 docx**（docx/pdf 由 build 独占）

### `/thesis-build`
- 输入：已通过全部闸门的正文、图表、引用
- 前置复查（不信任口头声明，可用 `tools/check_gates.py`）：
  "必须补充"为空 / `unresolved_fake_risk.md` 为空 / P0 = 0 / `format_audit.md` = PASS / 无 `_reduced.md` 残留
- 输出：`thesis/release/` 下正式版 docx/pdf（唯一 docx 产出者）
- 通过条件：生成成功，可打开，无目录错乱与资源缺失

### `/thesis-defense`
- 输入：终稿、实验亮点、系统截图、创新点
- 输出：`defense_outline.md`、`innovation_points.md`、`qa_bank.md`
- 通过条件：能直接支撑答辩讲稿与问答准备

### `/thesis-sync`
- 输入：最新终稿、图表、文献、答辩材料、notes
- 输出：同步后的 `release/` 与 notes 索引、终态 `workflow_state.md`
- 通过条件：正文、图表、文献、终稿版本一致

## 工作流状态板 `workflow_state.md`

每个阶段完成时**追加**一行到 `thesis/notes/workflow_state.md`，使闸门状态机器可查
（`python tools/check_gates.py` 会同时校验本文件与各闸门文件的实际内容，两者不一致
以闸门文件为准并报警）：

```md
# Workflow State

| stage | status | gate | timestamp | note |
|---|---|---|---|---|
| intake | done | topic_feasible=yes; must_fill=0 | 2026-05-01 | — |
| data | done | refs_ready=yes | 2026-05-02 | 2 篇 need-manual-download 已处置 |
| outline | done | evidence_bound=yes; budget_ok=yes | 2026-05-02 | 算法为主型 |
| assets | done | provenance_ok=yes | 2026-05-03 | — |
| write | done | unverified_ratio=12% | 2026-05-05 | 5 章全部出稿 |
| content | done | consistent=yes | 2026-05-05 | — |
| citations | done | fake_risk_open=0 | 2026-05-06 | — |
| audit | done | p0=0; p1=2(已降级) | 2026-05-06 | — |
| reduce | done | anchors_preserved=yes; map_synced=yes | 2026-05-07 | 仅 2/4 章 |
| format | done | format_audit=PASS | 2026-05-07 | — |
| build | done | release_ok=yes | 2026-05-07 | v1 终稿 |
```

字段约定：
- `status` ∈ `pending | in_progress | done | blocked`
- `gate` 为该阶段通过条件的机读摘要（`key=value`，分号分隔）
- 状态板是**日志**不是真相源——真相源永远是各闸门文件本身
  （`missing_requirements.md`、`ai_risk_audit.md`、`format_audit.md` 等）
