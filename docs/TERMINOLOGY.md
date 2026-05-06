# Terminology — Audit Concepts

SKILL.md 与 prompts/audit_prompt.md 多次出现"幻觉""虚空引用""术语漂移"等术语。
本文档给出可执行定义与正反例，避免主观判定。

## 幻觉 (Hallucination)
**定义**：正文出现项目代码、实验或日志中不存在的实现细节、模块名、API 调用、超参数。

| 类别 | 反例（正文写法） | 现实（项目实际） | 判定 |
|---|---|---|---|
| 不存在的模块 | "本系统实现了 `data.augment.MixupCutmix` 模块" | `grep -r MixupCutmix` 无结果 | P0 幻觉 |
| 不存在的超参 | "学习率 schedule 采用 cosine restart" | 训练脚本只有 `lr=1e-3` 常数 | P0 幻觉 |
| 夸大的能力 | "系统支持端到端训练-推理一体化部署" | 仓库无部署脚本 | P0 幻觉 |
| 合理简化 | "采用标准 Adam 优化器" 而代码用默认参数 | 简化但事实正确 | 不是幻觉 |

**检测方法**：claim_evidence_matrix.md 中 `source_file = —` 且 `status = unverified`
但出现在结论/摘要/创新点的，必须标 P0。

## 虚空引用 (Fake Reference / Phantom Citation)
**定义**：参考文献条目中作者、题名、年份、会议/期刊或 DOI 至少一项明显错误，
或经 ≥3 次搜索无法在公开可信来源（出版社官网、DOI、arXiv）确认存在。

| 类别 | 反例 | 判定 |
|---|---|---|
| 作者拼凑 | "Zhang Y, Wang H. Deep Foo. NeurIPS 2024" + 0 命中 | fake-risk |
| 年份漂移 | 引用论文真实是 2018，正文写 2021 | partial（metadata_mismatch） |
| 会议错配 | 实际发表在 ICCV，正文写 CVPR | partial（venue_unverified → 修正后 verified） |
| 仅 DOI 缺失但论文真实存在 | NeurIPS 2020 真实论文，仅未填 DOI | verified（reason: 可补 DOI） |

**检测**：由 `/thesis-citations`（citation_checker_prompt.md）独占。`/thesis-audit`
只读 `reference_truth_report.md`，不重复联网核验。

## 术语漂移 (Terminology Drift)
**定义**：同一概念在论文不同位置出现 ≥2 种写法，导致读者或评审误以为是不同对象。

| 漂移类别 | 反例（同一论文中混用） | 判定 |
|---|---|---|
| 模型名 | "U-Net" / "U-net" / "Unet" | P1（如核心模型名）；P2（如非核心） |
| 数据集名 | "Dunhuang-Mural" / "敦煌壁画数据集" / "DM 数据集" | P1（首次定义后必须固定一种） |
| 指标名 | "mIoU" / "Mean IoU" / "平均交并比" | P2（同一段落内统一即可） |
| 合理变体 | "卷积神经网络（CNN）" 首次定义后简称 CNN | 不是漂移 |
| 中英文混合 | 摘要写 "U-Net"，正文写 "U 形网络" | P1 |

**检测建议**：对核心术语建立词表，正则扫描 `\bU-?[Nn]et\b` 等变体。

## 数值不一致 (Metric Inconsistency)
**定义**：同一指标在摘要、正文、表格、结论中出现差异。

| 反例 | 判定 |
|---|---|
| 摘要写 "mIoU 达到 0.83"，结论写 "mIoU 0.85" | P0 |
| 表 4 显示 0.832，正文写 "约 0.83" | 不是不一致（合理四舍五入，应注明 round 规则） |
| 实验章给出 0.83，未在摘要复述 | 不是不一致（缺失而非冲突） |

## 句式机械化 (AI Fingerprint)
**定义**：连续段落均使用 "首先/其次/再次/此外/最后" 或对称编号、等长句式，
触发 AI 检测高分。

正面参考：段落长短交替；过渡靠语义而非连接词；具体数据替代空话；
图文交叉打破文本墙（详见 SKILL.md §"降低 AI 率写作规范"）。
