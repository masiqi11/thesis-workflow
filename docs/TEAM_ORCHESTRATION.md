# Team Orchestration

何时启用、如何分工、如何收敛。SKILL.md 不再内联这些细则，所有 Team 模式细节集中在此。

## 何时使用 Team 模式

- 整篇论文重写或多章并行（>=2 章同时推进）
- 长上下文任务出现目标漂移（参见 KNOWN_ISSUES #11）
- 需要在写作期间并行做引用核验或证据扫描

不需要 Team 的场景：单章修订、格式调整、单文件审查 — Team 反而增加协调成本。

## 角色与铁律

### `lead`
- 只做总控、分章、统一术语与口径
- 不直接并发改同一章节文件
- 汇总时必须输出：章节状态、证据覆盖、剩余风险

### `researcher`
- 只查证据，不扩写结论
- 必须回报：代码/日志/图表/文献来源路径
- 对未证实内容必须标 `unverified`

### `writer`
- 只改分配章节文件
- 不得跨章改标题、图号、引用编号
- 每段关键结论后要能追溯到证据源
- **同一时刻只允许一个 writer 改一个章节**（chapter-level mutex）

### `citation-checker`
- 只核引用真实性与编号闭环
- 不负责润色正文
- 必须标注文献状态：`verified / partial / unverified / fake-risk`
- 是 `reference_truth_report.md` 的唯一作者；`/thesis-audit` 只读不写

### `reviewer`
- findings 优先
- 无问题明确写 `no findings`
- 只审错，不扩写，不重构

## Team 启动模板

```text
角色：<lead/researcher/writer/citation-checker/reviewer>
目标：<本轮唯一目标>
可写文件：<仅列分配文件>
禁止事项：不得扩域；不得修改未分配文件；不得编造证据
交付必须包含：
1. 完成内容
2. 使用的证据源
3. 未证实内容
4. 验证命令或核验动作
```

## Team 收敛清单

每轮 Team 结束前 lead 必须逐项检查：

- 是否存在多 agent 同写一文件
- 是否有未回报证据源的段落
- 是否有 `fake-risk` 文献未处置
- 是否有图号/表号改动未同步正文
- 是否有结论超出实验支撑

任何一项未通过都不得进入下一阶段。
