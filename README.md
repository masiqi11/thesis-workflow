# thesis-workflow

[![Version](https://img.shields.io/badge/version-v0.2.0-blue.svg)](https://github.com/masiqi11/thesis-workflow/releases/tag/v0.2.0)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-purple.svg)](SKILL.md)

中文 | [English](README_EN.md)

> 一个可公开发布的 Claude Code 论文工作流 Skill：覆盖需求采集、证据收集、提纲规划、章节撰写、引用核验、格式审查、AI 风险复核、降重改写与终稿构建。

## 概览

`thesis-workflow` 是一个**通用型论文写作 Skill**，不是绑定某个学校模板的硬编码脚本。

核心铁律只有一句：

**在要求未澄清之前，不进入正式论文撰写与最终排版。**

它适用于：
- 基于现有项目、代码、实验结果反推论文
- 用 Markdown -> Word/PDF 管理整篇论文交付链
- 希望降低幻觉、虚空引用、格式返工与长上下文漂移

## 核心特性

- **需求先行**：未明确结构、格式、引用规则前，阻断正式写作
- **证据驱动**：关键结论应绑定代码、日志、图表、实验、截图或文献来源
- **引用真值核验**：不仅排版参考文献，还要检查文献是否真实存在
- **AI 风险审查**：检查虚构实现、虚构实验、术语漂移、数值不一致
- **Agent Team 协作**：支持 lead / researcher / writer / citation-checker / reviewer 分工
- **格式闸门**：格式规则未锁定时，不允许提前进入 Word 终稿构建
- **降重模式**：在保留事实锚点的前提下做针对性改写
- **论文引用收集**：数据准备阶段强制收集引用论文，优先国外论文便于下载
- **资源就绪闸门**：引用论文、实验数据、图表、证据源未齐备禁止正文撰写
- **正文图表耦合**：边写边插图，禁止先写正文后插图
- **模板要求持久化**：格式要求写入文件，不依赖上下文记忆
- **图表策略区分**：概念图生成提示词，实验数据图用 Python 脚本生成
- **字数预算规划**：按论文类型（算法为主/系统为主/均衡型）差异化分配各章字数
- **降低 AI 率规范**：禁止机械递进、对称编号等 AI 写作指纹
- **GitHub 友好结构**：自带 README、INSTALL、DESIGN、docs、prompts、tools、examples

## 仓库结构

```text
thesis-workflow/
├─ SKILL.md
├─ README.md
├─ README_EN.md
├─ DESIGN.md
├─ INSTALL.md
├─ LICENSE
├─ requirements.txt
├─ .gitignore
├─ docs/
│  └─ PRD.md
├─ prompts/
│  ├─ README.md
│  ├─ intake_prompt.md
│  ├─ writer_prompt.md
│  ├─ citation_checker_prompt.md
│  └─ audit_prompt.md
├─ tools/
│  ├─ README.md
│  ├─ build_thesis.py
│  ├─ collect_assets.py
│  └─ verify_citations.py
└─ examples/
   └─ example_dunhuang.md
```

## 核心命令

```text
/thesis-intake
/thesis-data
/thesis-outline
/thesis-assets
/thesis-write
/thesis-content
/thesis-citations
/thesis-format
/thesis-audit
/thesis-reduce
/thesis-build
/thesis-defense
/thesis-sync
```

## 推荐执行链

```text
/thesis-intake
  -> /thesis-data
  -> /thesis-outline
  -> /thesis-assets
  -> /thesis-write
  -> /thesis-content
  -> /thesis-citations
  -> /thesis-format
  -> /thesis-audit
  -> /thesis-reduce
  -> /thesis-build
  -> /thesis-defense
  -> /thesis-sync
```

## 运行模式

- `--assist`：只分析，不产正式稿
- `--draft`：产草稿，不默认覆盖定稿
- `--auto`：自主审阅项目、自主收集材料
- `--team`：启用多 Agent 协作
- `--team-strict`：严格分文件所有权
- `--safe`：保守审查/改写
- `--aggressive`：更强改写，但不改结论与指标

## 快速开始

1. 将本仓库放到本地 Claude Code skills 目录下
2. 确保根目录存在 `SKILL.md`
3. 从 `/thesis-intake --assist` 开始
4. 在格式规则明确前，不进入 `/thesis-format` 和 `/thesis-build`

## 示例

参考 [examples/example_dunhuang.md](examples/example_dunhuang.md)。

## 安装

见 [INSTALL.md](INSTALL.md)。

## 设计

见 [DESIGN.md](DESIGN.md)。

## 产品说明

见 [docs/PRD.md](docs/PRD.md)。

## 许可证

MIT

## 更新日志

### v0.2.0

- 新增论文引用收集（thesis-data 强制收集，优先国外论文，下载失败通知用户）
- 新增资源就绪闸门（引用/数据/图表/证据源未齐备禁止正文撰写）
- 新增正文与图表强耦合（边写边插图，缺图即补）
- 新增模板要求持久化（写入 template_requirements.md，不依赖上下文记忆）
- 新增图表生成策略区分（概念图→提示词，实验数据图→Python 脚本，截图→实际捕获）
- 新增字数预算规划（按论文类型差异化分配，含各学历层次参考）
- 新增降低 AI 率写作规范（禁止机械递进/对称编号/AI 套话等写作指纹）
- 摘要、Abstract、目录、致谢、参考文献改为默认必要项
- 引用规则细化（文内标记格式、标记位置、条目必需字段）
- 修复 5 个已记录问题（#13-#17）

### v0.1.0

- 初始版本，覆盖完整论文工作流
