# Example: thesis-workflow on a graduation project

## Scenario

Topic: 基于 U-Net 的敦煌壁画损伤区域自动分割研究
Type: 算法为主型 · 本科 · 5 章 · 总字数约 20000

## Recommended command chain

```text
/thesis-intake --assist                # 含题目背景分析（第 0 步）
/thesis-data --auto
/thesis-outline --draft
/thesis-assets --auto
/thesis-write chapter=2 --draft        # 相关技术与理论基础
/thesis-write chapter=5 --draft        # 总结与展望（短章先行，验证流水线）
/thesis-content --safe
/thesis-citations --safe               # 真值闸门
/thesis-audit --safe                   # P0 清零后才可降重/排版
/thesis-reduce --safe                  # 可选；锚点保护
/thesis-format --draft                 # 排版检查（最后一道文本闸门）
/thesis-build
```

> 并发约束：同一时刻只允许一个 agent 写一个章节（SKILL.md §/thesis-write）。
> 上面写第二、五章是先后执行；第五章先做是为了在最短链路上验证 intake → audit
> 闭环。

---

## Sample artifacts

下述片段都来自 `--draft` 模式下真实跑过的产物，已脱敏。

### `thesis/notes/intake_requirements.md`（节选）

```md
## 1. 基本信息
- 论文题目: 基于 U-Net 的敦煌壁画损伤区域自动分割研究
- 学历: 本科
- 总字数: 18000–22000
- 论文类型倾向: 算法为主

## 7. 参考文献
- 标准: GB/T 7714-2015
- 文内: 上标 [1]
- 排序: 引用顺序
- 允许 arXiv 与 GitHub: 是（必须给出访问日期）
```

### `thesis/notes/missing_requirements.md`

```md
## 必须补充
- 表题位置（图题已知"图下居中"，表题未给）
## 建议补充
- 各章目标字数上限（学校只给了总字数）
## 说明
未补充前，/thesis-format 不得进入正式排版。
```

### `thesis/refs/papers_inventory.md`（节选）

```md
| ref_id | title | year | venue | status | local_path |
|---|---|---|---|---|---|
| [1] | U-Net: Convolutional Networks for Biomedical Image Segmentation | 2015 | MICCAI | downloaded | refs/papers/ronneberger_2015_unet.pdf |
| [2] | Image Inpainting for Irregular Holes Using Partial Convolutions | 2018 | ECCV | downloaded | refs/papers/liu_2018_partialconv.pdf |
| [3] | 敦煌壁画病害图像分类研究 | 2021 | 计算机工程 | need-manual-download | — |
```

### `thesis/notes/chapter_evidence_map.md`（第 2 章片段）

```md
| claim | source_file | source_loc | status |
|---|---|---|---|
| U-Net 编码器-解码器结构通过跳跃连接保留空间细节 | refs/papers/ronneberger_2015_unet.pdf | §3.1 fig.1 | verified |
| 部分卷积在不规则掩码上优于零填充 | refs/papers/liu_2018_partialconv.pdf | tab.4 | verified |
| 敦煌壁画损伤分布以裂隙与脱落为主 | refs/papers/[3] need-manual-download | — | unverified |
```

### `thesis/notes/reference_truth_report.md`（节选）

```md
| ref_id | title_match | author_match | year_match | venue_match | doi_or_url | status | note |
|---|---|---|---|---|---|---|---|
| [1] | ok | ok | ok | ok | 10.1007/978-3-319-24574-4_28 | verified | — |
| [2] | ok | ok | ok | ok | 10.1007/978-3-030-01252-6_6 | verified | — |
| [3] | ok | ok | ok | partial | — | partial | 期刊卷期未核实 |
```

### `thesis/notes/ai_risk_audit.md`（节选）

```md
## P0 — 必须修复
- 第 4 章 §4.2 未引用即给出 mIoU=0.83 数字（无 metric_tables 支撑）

## P1 — 应修复
- 第 2 章把 "U-Net" 与 "U-net"、"Unet" 三种写法混用（术语漂移）

## P2 — 建议
- 第 5 章"未来工作"部分句式过于模板化，建议改写
```

---

## What this example demonstrates

- Intake-first gating: missing_requirements.md 非空时，下游格式与终稿命令拒绝执行。
- Evidence-driven chapters: 每条断言追溯到具体 source_file:loc。
- Citation truth checking 的标准化输出：title/author/year/venue 四字段对账。
- AI 风险审查按 P0/P1/P2 分级，与 SKILL.md §/thesis-audit 一致。
- 章节并行约束（同时只跑一个章节）与 `--draft` 模式的闭环验证策略。
