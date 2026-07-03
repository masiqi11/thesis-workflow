# 端到端工作流指南：从题目输入到终稿输出

本文回答一个问题：**用户手里只有"论文题目 + 项目背景"时，如何走完全流程拿到
一份内容准确、引用真实、格式合规的毕业论文终稿。**

契约细节见 [`TEMPLATES.md`](TEMPLATES.md)；术语定义见 [`TERMINOLOGY.md`](TERMINOLOGY.md)；
Team 协作见 [`TEAM_ORCHESTRATION.md`](TEAM_ORCHESTRATION.md)。

---

## 一图流

```text
输入：论文题目 + 项目背景 (+ 学校格式规范)
  │
  ▼
① /thesis-intake ─── 题目分析 + 需求采集
  │   闸门 G1：题目可行（至少一个研究问题有证据）且"必须补充"为空
  ▼
② /thesis-data ───── 实验数据落盘 + 引用论文收集
  │   闸门 G2：metric_tables 有源可溯；核心文献 downloaded/metadata-only
  ▼
③ /thesis-outline ── 章节结构 + 论文类型 + 字数预算
  │   闸门 G3：每章证据源绑定；预算 ±5%
  ▼
④ /thesis-assets ─── 图表资产 + 数据溯源
  │   闸门 G4：每张实验图有脚本 + 数据源（data_provenance）
  ▼
⑤ /thesis-write ──── 逐章撰写（边写边插图）
  │   闸门 G5：本章 unverified ≤ 30%
  ▼
⑥ /thesis-content ── 内部一致性（对照代码与 metric_tables，离线）
  │   闸门 G6：零 high 级发现
  ▼
⑦ /thesis-citations ─ 引用真值核验（联网，独占）
  │   闸门 G7：unresolved_fake_risk.md 为空
  ▼
⑧ /thesis-audit ──── AI 风险总审（消费 G6/G7 报告，不重复联网）
  │   闸门 G8：P0 = 0
  ▼
⑨ /thesis-reduce ─── 降重（可选；锚点保护；改后同步证据映射）
  │   闸门 G9：anchor_preserved 全 yes；无 _reduced.md 残留
  ▼
⑩ /thesis-format ─── 10 维度排版检查（最后一道文本闸门）
  │   闸门 G10：format_audit = PASS
  ▼
⑪ /thesis-build ──── 复查 G1/G7/G8/G9/G10 后生成 docx/pdf
  ▼
⑫ /thesis-defense ── 答辩材料（只用已验证断言）
  ▼
⑬ /thesis-sync ───── 一致性同步 + 归档
  │
输出：thesis/release/ 终稿 + 全程证据链
```

任何时点运行 `python tools/check_gates.py --thesis-dir thesis` 可机器校验
G1/G7/G8/G9/G10 五个关键闸门。

---

## 顺序为什么是这样

三条不可交换的依赖：

1. **audit 在 reduce 前** —— 降重只改 audit 标注的 P2 段落。没有审查结果，
   降重无从知道哪里能动、哪里是事实锚点。
2. **reduce 在 format 前** —— 降重改文本。若排版检查先跑，改写后的分页、
   引用位置、字数全部失效，检查报告变成废纸。
3. **format 在 build 前且是最后一道文本闸门** —— 任何再动正文的步骤之后，
   排版检查必须重跑。

> 历史教训：v0.3.0 及以前的状态机是 `format → audit → reduce`，导致
> "P0 清零才可排版"的闸门在逻辑上永远无法生效。v0.4.0 起废弃。

---

## 准确性与真实性如何保证（证据链五段闭环）

| 环节 | 机制 | 防什么 |
|---|---|---|
| 数字入库 | `metric_tables.md` 每个数字必须带 `source_file` 指针（②） | 编造实验数据 |
| 断言出稿 | 每条关键断言写入 `chapter_evidence_map.md`，unverified > 30% 拒稿（⑤） | 幻觉式写作 |
| 引用上桌 | 每篇文献 title/author/year/venue 四字段联网对账，fake-risk 阻断（⑦） | 虚空引用 |
| 图表溯源 | 实验图必须有生成脚本 + 数据源；无法溯源 = P0（④⑧） | 不可复现的图 |
| 改写不漂移 | 降重后强制同步证据映射；锚点变动即回退（⑨） | 降重毁证据 |

最后 build（⑪）不信任任何口头"已通过"——它自己重查一遍闸门文件。

---

## 各阶段产物速查

| 阶段 | 关键产物 | 谁消费 |
|---|---|---|
| ① intake | `topic_analysis.md`、`template_requirements.md`（格式唯一真相源）、`missing_requirements.md` | 所有后续阶段 |
| ② data | `metric_tables.md`（数字唯一真相源）、`papers_inventory.md` | ⑤⑥⑧ |
| ③ outline | `thesis_outline.md`、`chapter_matrix.md`、`figure_plan.md` | ④⑤ |
| ④ assets | `assets_manifest.md`（含 data_provenance） | ⑤⑧⑩ |
| ⑤ write | 章节 md、`chapter_evidence_map.md`、`refs/references.md` | ⑥⑦⑧ |
| ⑥ content | `content_audit.md` | ⑧ |
| ⑦ citations | `reference_truth_report.md`（引用真值唯一权威）、`unresolved_fake_risk.md` | ⑧⑪ |
| ⑧ audit | `ai_risk_audit.md`、`prioritized_fix_list.md` | ⑨⑩⑪ |
| ⑨ reduce | 合并后的章节文件、`reduce_report.md`、同步后的证据映射 | ⑩ |
| ⑩ format | `format_audit.md`（PASS/FAIL/BLOCKED） | ⑪ |
| ⑪ build | `release/` docx/pdf、`build_manifest.md` | ⑫⑬ |
| ⑫ defense | `defense_outline.md`、`innovation_points.md`、`qa_bank.md` | 用户 |
| ⑬ sync | `sync_report.md`、`ARCHIVE_INDEX.md` | 归档 |

每阶段完成后向 `thesis/notes/workflow_state.md` 追加一行状态
（schema 见 [`TEMPLATES.md`](TEMPLATES.md#工作流状态板-workflow_statemd)）。
状态板是日志；真相源永远是闸门文件本身。

---

## 常见失败与恢复路径

| 症状 | 所在闸门 | 恢复动作 |
|---|---|---|
| 题目与项目对不上（所有 RQ 证据缺失） | G1 | 调整题目或补材料，重跑 ① |
| 核心文献下载不了 | G2 | 按 `papers_to_download.md` 手动下载后重跑 ②收尾 |
| 某章 unverified 超 30% | G5 | 回给 researcher 补证据，不硬写 |
| 引用被标 fake-risk | G7 | 按 `unresolved_fake_risk.md` 建议换文献或删引改写 |
| audit 报 P0 | G8 | 按 `prioritized_fix_list.md` 顺序修复，重审 |
| 降重把事实改漂了 | G9 | 回退该段（reduce_report 有原句），重新改写 |
| format 报 FAIL | G10 | 修 FAIL 项重查；**不要**跳过直接 build |
| build 后发现正文改过 | ⑬ sync 检出 | 按 sync_report 提示重跑 ⑩→⑪ |
| Word 文件被占用 | ⑪ | 关闭 Word 或输出 `_验收版.docx` |

---

## 最小可行路径（时间紧张时）

不可跳过的骨架：① intake → ② data → ③ outline → ⑤ write → ⑦ citations →
⑧ audit → ⑩ format → ⑪ build。

可酌情简化的：④ assets（图少时并入 ⑤）、⑥ content（并入 ⑧）、⑨ reduce
（查重压力小则跳过）、⑫⑬（答辩前再做）。

**任何情况下不可跳过的三关**：引用真值核验（⑦）、P0 清零（⑧）、排版检查（⑩）。
跳过它们省下的时间，会在盲审和答辩时加倍还回来。
