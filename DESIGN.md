# thesis-workflow 设计文档

## 设计概述

### 目标

- 提供一套可复用、可公开分发的通用论文写作工作流，而非绑定单一学校模板。
- 在正式写作前强制完成需求采集与格式澄清。
- 用证据矩阵约束正文内容，降低幻觉、虚空引用与数值漂移。
- 在长链任务中支持 Agent Team 分工，降低上下文污染与目标漂移。
- 支持从 Markdown / 素材 / 实验结果到 Word / PDF 终稿的完整闭环。

### 非目标

- 不试图仅凭 doc/docx 模板自动完整提取全部学校排版规则。
- 不替代学校正式模板规范；若文字版规则缺失，只停在 assist/draft 阶段。
- 不允许在证据不足时编造实验、系统功能或参考文献。

## 架构设计

### 整体架构

```text
用户要求 / 模板文字规则
          │
          v
   /thesis-intake
          │
   requirements 完整？
      ├─ 否 -> missing_requirements.md -> 停止正式写作
      └─ 是
          v
     /thesis-data -> /thesis-outline -> /thesis-assets
          │             │                 │
          └─────────────┴──────────────┐
                                       v
                                /thesis-write
                                       │
                                /thesis-content   （内部一致性，离线）
                                       │
                                /thesis-citations （引用真值，联网独占）
                                       │
                                /thesis-audit     （AI 风险总审，P0 清零闸门）
                                       │
                                /thesis-reduce    （可选降重，锚点保护）
                                       │
                                /thesis-format    （最后一道文本闸门）
                                       │
                                /thesis-build     （复查全部闸门后独占产出 docx/pdf）
                                       │
                            /thesis-defense -> /thesis-sync
```

### 核心组件

- **Intake Gate**：采集结构、格式、图表、引用、交付要求，决定是否允许进入正式链路。
- **Evidence Pipeline**：从代码、实验、日志、图表、截图与文献中抽取证据，建立章节绑定关系。
- **Writing Pipeline**：按章节产出 Markdown，并要求关键结论可回溯到证据源。
- **Audit Pipeline**：分开核查内容一致性、文献真实性、AI 风险与格式合规性。
- **Build Pipeline**：把已审查内容生成 Word/PDF，并同步 release 目录。
- **Team Orchestrator**：在多章并行时管理角色、文件所有权与收敛流程。

## 设计决策

### 决策记录

| 日期 | 决策 | 理由 | 影响 |
|------|------|------|------|
| 2026-04-01 | intake 先行 | 学校格式和结构不明时，返工成本最高 | 正式写作被强制后移 |
| 2026-04-01 | 证据驱动写作 | 论文最常见风险是编造实现、实验和引用 | 每章必须绑定证据源 |
| 2026-04-01 | 引用核验与 AI 风险审查拆开 | 二者关注点不同 | 审查颗粒度更清晰 |
| 2026-04-01 | 多章写作优先 Team 模式 | 长上下文容易导致目标漂移与术语混写 | 需要角色边界与文件所有权 |
| 2026-04-01 | GitHub-ready packaging | 便于公开分发、复用与维护 | 需要 README/INSTALL/examples/prompts/tools |

### 技术选型

- **文档层**：Markdown + `SKILL.md`
- **执行层**：Claude Code tools / MCP / local scripts
- **原因**：工作流既需要明确规则，又需要保留跨项目复用性与局部自动化能力。

## 目录设计理由

- `SKILL.md`：真实入口与执行契约
- `README.md` / `README_EN.md`：面向 GitHub 的公开首页
- `DESIGN.md`：解释为什么这样设计
- `INSTALL.md`：本地安装与 GitHub 发布说明
- `docs/`：产品与长期设计资料
- `prompts/`：可复用提示词片段
- `tools/`：本地辅助脚本
- `examples/`：演示一个真实论文项目的调用链

## 权衡取舍

### 已知限制

- **模板解析限制**：doc/docx 模板只能辅助观察样式，不能替代文字版格式规则。
- **联网依赖**：文献真实性核查需要搜索/网页抓取能力。
- **证据完备性依赖项目状态**：若日志、结果图、截图缺失，正文可信度会下降。
- **Helper tools 为 starter assets**：仓库内脚本只提供最小可复用骨架，不是完整论文引擎。

### 技术债务

- prompts 仍可继续细分到 outline / format / reduce / defense 等阶段。
- tools 仍可继续接入 docx 渲染、DOI 查询、图像清洗、公式转图等自动化脚本。
- 未来可补 CI 校验，检查文档结构、示例存在性与脚本基本可执行性。

## 安全考量

### 风险模型

- **虚假引用**：题目、作者、年份、会议或 DOI 不存在。
- **虚假实验/虚假实现**：正文声称完成的模块、实验或指标在代码和结果目录中无证据。
- **多 Agent 扩域写入**：多个 Agent 修改同一章节，造成图号、术语和结论冲突。
- **格式误判**：仅凭模板视觉观察就误以为已掌握全部学校规范。

### 防护措施

- requirements 未齐时，禁止进入正式写作 / 正式排版 / 终稿构建。
- 关键结论必须挂证据源，并标注验证状态。
- 引用状态采用 `verified / partial / unverified / fake-risk` 分级。
- 通过 lead / researcher / writer / citation-checker / reviewer 做职责隔离。
- build 前强制经过 content / citations / audit / format 校验。

## 版本路线

### v0.1.0

- 完成 GitHub-ready 仓库结构
- 完成主 Skill 规范与执行契约
- 提供基础 prompts 与 helper tools 骨架
- 提供安装文档、产品说明与示例

### v0.2.0

- `/thesis-data` 强制收集引用论文，并引入"资源就绪闸门"
- 正文与图表强耦合（边写边插图）
- 格式要求持久化到 `template_requirements.md`
- 字数预算规划（按算法/系统/均衡型差异化分配）
- 降低 AI 率写作规范（禁止机械递进、对称编号等指纹）
- 摘要、Abstract、目录、致谢改为默认必要项
- 修复 17 条历史问题（见 `docs/KNOWN_ISSUES.md`）

### v0.3.0（当前版本）

- 新增 3 个 prompt 模板（`outline_prompt`、`reduce_prompt`、`format_prompt`）
  → 7 个子 Skill 现有对应 prompt，覆盖率从 33% 提升至 58%
- 新增 GitHub Actions CI，Push/PR 自动运行 pytest（Python 3.10/3.11/3.12）
- 新增 `thesis/` 目录骨架与 README，明确全流水线产物路径
- `outline_prompt` 内置论文类型识别逻辑（算法/系统/均衡型），解决 P2-5 归属问题
- `reduce_prompt` 定义事实锚点不变式与 AI 指纹改写分类
- `format_prompt` 定义 10 维度格式检查表与 PASS/FAIL/BLOCKED 状态机
- helper tools 全面重写：类型注解、logging、独立退出码、可测试结构
- 15 个 pytest 用例覆盖三个工具的正/反例与 CLI 退出码

### v0.4.0（当前版本）

- **修正执行顺序**：audit → reduce → format → build（旧的 format-在-audit-前
  顺序使 P0 闸门在逻辑上无法生效，已废弃）
- 新增题目背景分析入口（intake 第 0 步），工作流入口正式定义为
  "论文题目 + 项目背景"
- 13/13 子 Skill 全部配备 prompt 模板（补齐 data/assets/content/build/defense/sync）
- 机器可查闸门：`workflow_state.md` 状态板 + `tools/check_gates.py`
- 真实性链条闭环：降重同步证据映射、图表数据溯源、build 前置复查
- 新增 `docs/WORKFLOW.md` 端到端指南

### v0.5.0（规划）

- docx 渲染辅助脚本（从 Markdown 生成 Word 并校验样式）
- DOI/arXiv 元数据批量查询脚本
- 图像清洗与尺寸规范化辅助脚本
- `check_gates.py` 扩展：校验 `workflow_state.md` 与闸门文件的一致性
