# AI signature phrases — trigger words & concrete replacements

A reference for `/thesis-reduce` (and for writers during `/thesis-write`). These are
words and structures that mark **templated, machine-flat** academic prose. The fix is
never to swap in a synonym and move on — it is to replace hollow phrasing with a
specific claim, number, citation, or the author's own analysis. That genuinely
improves the writing; a lower AI-detection score is a side effect of better prose,
not the goal.

> This file lists *writing-quality* signals only. It contains no detector-evasion
> techniques (no invisible characters, homoglyphs, or docx-run tricks) — those do not
> improve the paper and are out of scope (see `prompts/reduce_prompt.md` §Scope boundary).

## 中文高频 AI 痕迹词

### 机械连接词（最高风险）
| 痕迹写法 | 问题 | 改法 |
|---|---|---|
| 首先…其次…再次…最后 | 机械递进，段段同构 | 按逻辑自然过渡；用因果/对比/递进的**语义**衔接，而非序号词 |
| 值得注意的是 / 值得一提的是 | 空转，无信息 | 直接陈述那个"值得注意"的事实本身 |
| 综上所述 / 总而言之 / 总的来说 | 段末套话 | 给出具体结论数字或判断，不用起头套话 |
| 此外 / 另外（连续出现） | 平铺堆叠 | 合并相关点，或用具体逻辑关系替代 |

### 学术空话（要挂具体证据）
| 痕迹写法 | 改法 |
|---|---|
| 研究表明 / 大量研究表明 | 指名到具体文献 + 年份 + 结论数值（"Zhang 等[3]在 X 数据集上将 mIoU 提升到 0.83"） |
| 具有重要意义 / 具有重要价值 | 说清楚对谁、在什么场景下、带来什么可量化的改变 |
| 随着…的快速发展 / 在当今时代 | 删掉起头，直接进入本段的具体命题 |
| 越来越多的研究 / 广泛应用 | 给出范围与出处，或改为具体计数 |
| 有效地 / 显著地（无数据支撑） | 补上幅度（"降低 3.2 个百分点"），否则删副词 |

### 结构模板痕迹
| 痕迹写法 | 改法 |
|---|---|
| 本文从 A、B、C 三个方面展开 | 不预告结构；让章节顺序自己承担导航 |
| 本节将从以下几点进行阐述 | 直接进入第一点 |
| 段段等长、段段总分总 | 长短段交替、有详有略、图文交叉打破文本墙 |

## English high-risk phrases

| Flagged | Replace with |
|---|---|
| delve into | explore / examine / look at |
| furthermore / moreover（连续） | also, or a concrete logical link |
| it is important to note that | state the fact directly |
| multifaceted / landscape（比喻义） | name the specific aspects / field |
| a wide range of / various | give the actual range or count |
| plays a crucial role | say what it does, measurably |

## 为什么这些会被标记（原理，非技巧）

AI 检测器主要看 **困惑度（perplexity）低** 与 **突发度（burstiness）低**——即用词过于
"平均可预测"、句长过于均匀。上面这些痕迹词恰好是低困惑度的典型来源。所以正确的应对不是
藏字符，而是：

- **句长剧烈变化**：短句（≤15 字）与长句（≥40 字）在同一段交替
- **具体压过抽象**：用真实数据、专有名词、学科术语替换通用表述
- **注入作者自己的判断**：对已有研究给出具体评价或批评（"该方法在小目标上召回偏低，
  本文据此……"）——这是任何检测器都无法替你生成的内容

这些做法让文字真的更好，也真的更像作者本人写的，而不是把 AI 文本伪装成人写。

---

## 来源与取舍

本清单的痕迹词与"困惑度/突发度"原理，吸纳自 `telagod/code-abyss` 项目
`skills/reducing-aigc-detection`（MIT）中**改善写作质量**的部分。

有意**未吸纳**该项目中的检测器规避技术：docx run 层/XML 篡改、隐藏字符与零宽字符
注入、同形字（Latin/Cyrillic/Greek look-alike）替换、humanizer 工具痕迹。原因：
这些手段不改善论文本身，只是把未披露的 AI 文本伪装过检；它们正被检测器作为独立
特征反向标记，且与本项目"证据驱动、真实性优先"的设计哲学直接冲突。
