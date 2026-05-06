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
- 输入：用户口述要求、学校规范、模板说明、文字版格式条目
- 输出：`intake_requirements.md`、`missing_requirements.md`、`template_requirements.md`
- 通过条件：关键格式规则已明确，缺失项不含"必须补充"，模板要求已持久化到文件

### `/thesis-data`
- 输入：项目代码、实验日志、结果目录、截图入口、环境信息、论文主题与研究方向
- 输出：`data_inventory.md`、`experiment_summary.md`、`metric_tables.md`、`runtime_env.md`、`papers_inventory.md`、`papers_to_download.md`、`paper_data_extracts.md`、`thesis/refs/papers/`
- 通过条件：关键实验指标、数据集规模、运行环境、可用图表已落盘；引用论文已检索收集，至少核心文献为 `metadata-only` 或 `downloaded` 状态；需手动下载的文献已通知用户

### `/thesis-outline`
- 输入：intake 结果、项目证据、材料清单、学历层次与学校字数要求
- 输出：`thesis_outline.md`（含字数规划表）、`chapter_matrix.md`、`figure_plan.md`、`reference_plan.md`
- 通过条件：每章目标、证据源、图表源、参考文献源已绑定；论文类型已识别；各章字数预算已明确且总字数符合学校要求

### `/thesis-assets`
- 输入：图表原图、截图、表格数据、图号规划
- 输出：`assets_manifest.md`、规范化后的 `thesis/figures/*`
- 通过条件：图号连续、图题明确、正文引用可追踪、低质量图片已剔除

### `/thesis-write`
- 输入：outline、证据矩阵、图表计划、章节目标字数、`template_requirements.md`、`papers_inventory.md`、`figure_plan.md`、`chapter_matrix.md`
- 输出：章节 Markdown、`chapter_evidence_map.md`
- 通过条件：每章均附证据来源，未证实内容已显式标记；正文与图表强耦合，图号与图题已内联；引用文献状态已同步；本章 unverified 占比 ≤ 30%（超过即拒绝出稿，回退给 researcher 补证据）

### `/thesis-content`
- 输入：全文章节、代码实现、实验结果、系统截图
- 输出：`content_audit.md`
- 通过条件：模型名、数据集、参数、指标、系统功能口径一致

### `/thesis-citations`
- 输入：正文引用、参考文献列表、联网搜索结果
- 输出：`citation_audit.md`、`reference_truth_report.md`、`references_checked.md`
- 通过条件：不存在 `fake-risk` 未处置条目，正文与文后引用双向闭合

### `/thesis-format`
- 输入：Markdown 章节、图表资产、明确的文字版格式规则、模板文件（可选）
- 输出：Word 验收版、`format_audit.md`
- 通过条件：标题、目录、页码、图表题、参考文献、分页均符合规则

### `/thesis-audit`
- 输入：全文、项目代码、实验数据、`citation_audit.md`、`reference_truth_report.md`
- 输出：`ai_risk_audit.md`、`claim_evidence_matrix.md`、`prioritized_fix_list.md`
- 通过条件：P0 清零，P1 已修复或显式降级说明
- 与 `/thesis-citations` 边界：`/thesis-audit` 不重复执行联网真值核验，
  仅消费 `reference_truth_report.md`，做跨章/跨段一致性与"断言↔证据"的复核。

### `/thesis-reduce`
- 输入：查重高风险段落、原文、事实锚点、引用锚点
- 输出：`reduce_report.md`
- 通过条件：事实、数值、术语、引用未漂移，重复表述显著下降

### `/thesis-build`
- 输入：已通过审查的正文、图表、引用、格式脚本
- 输出：正式版 docx/pdf、`thesis/release/`
- 通过条件：生成成功，可打开，无目录错乱与资源缺失

### `/thesis-defense`
- 输入：终稿、实验亮点、系统截图、创新点
- 输出：`defense_outline.md`、`innovation_points.md`、`qa_bank.md`
- 通过条件：能直接支撑答辩讲稿与问答准备

### `/thesis-sync`
- 输入：最新终稿、图表、文献、答辩材料、notes
- 输出：同步后的 `release/` 与 notes 索引
- 通过条件：正文、图表、文献、终稿版本一致
