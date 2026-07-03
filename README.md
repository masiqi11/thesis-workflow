# thesis-workflow

[![Version](https://img.shields.io/badge/version-v0.4.0-blue.svg)](https://github.com/masiqi11/thesis-workflow/releases)
[![CI](https://github.com/masiqi11/thesis-workflow/actions/workflows/ci.yml/badge.svg)](https://github.com/masiqi11/thesis-workflow/actions/workflows/ci.yml)
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
├── SKILL.md
├── README.md
├── README_EN.md
├── DESIGN.md
├── INSTALL.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── .github/
│   └── workflows/
│       └── ci.yml              ← pytest on push/PR
├── docs/
│   ├── PRD.md
│   ├── WORKFLOW.md             ← 端到端指南：题目输入 → 终稿输出
│   ├── KNOWN_ISSUES.md
│   ├── TEMPLATES.md
│   ├── TEAM_ORCHESTRATION.md
│   ├── TERMINOLOGY.md
│   └── template_requirements_template.md
├── prompts/                    ← 13 个子 Skill 全覆盖（见 prompts/README.md）
│   ├── README.md
│   ├── intake_prompt.md        ← 含题目背景分析（第 0 步）
│   ├── data_prompt.md
│   ├── outline_prompt.md
│   ├── assets_prompt.md
│   ├── writer_prompt.md
│   ├── content_prompt.md
│   ├── citation_checker_prompt.md
│   ├── audit_prompt.md
│   ├── reduce_prompt.md
│   ├── format_prompt.md
│   ├── build_prompt.md
│   ├── defense_prompt.md
│   └── sync_prompt.md
├── tools/
│   ├── README.md
│   ├── build_thesis.py
│   ├── collect_assets.py
│   ├── verify_citations.py
│   └── check_gates.py          ← 一键校验全部流程闸门
├── tests/
│   ├── test_build_thesis.py
│   ├── test_collect_assets.py
│   ├── test_verify_citations.py
│   └── test_check_gates.py
├── thesis/
│   └── README.md               ← 全流水线产物路径说明
└── examples/
   └── example_dunhuang.md
```

## 核心命令

13 个子 Skill 的完整定义请见 [SKILL.md](SKILL.md#子-skill-总览)。
推荐执行链见下节；契约与 Team 协作细则见 [docs/TEMPLATES.md](docs/TEMPLATES.md)
与 [docs/TEAM_ORCHESTRATION.md](docs/TEAM_ORCHESTRATION.md)。

## 推荐执行链

```text
/thesis-intake (含题目背景分析)
  -> /thesis-data (含引用论文收集)
  -> /thesis-outline (含字数预算)
  -> /thesis-assets
  -> /thesis-write (资源就绪闸门)
  -> /thesis-content
  -> /thesis-citations (真值闸门)
  -> /thesis-audit (P0 清零闸门)
  -> /thesis-reduce (锚点保护，可选)
  -> /thesis-format (排版检查闸门)
  -> /thesis-build
  -> /thesis-defense
  -> /thesis-sync
```

> 顺序铁律：审查在降重前（降重消费审查的 P2 标记），降重在排版前
> （改文本后排版检查必须重跑）。完整流程指南见 [docs/WORKFLOW.md](docs/WORKFLOW.md)。

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

### v0.4.0

- **修正执行顺序（重要）**：审查 → 降重 → 排版 → 终稿；废弃旧的"排版在审查前"
  顺序（该顺序使 P0 闸门无法生效）
- 新增题目背景分析入口（intake 第 0 步：题目拆解/研究问题/可行性/创新点候选）
- 13 个子 Skill 全部配备 prompt 模板（新增 data/assets/content/build/defense/sync 六个）
- 新增机器可查闸门：`workflow_state.md` 状态板 + `tools/check_gates.py`（含 19 个测试）
- 真实性链条闭环：降重后强制同步证据映射；实验图必须记录数据溯源；
  build 前自行复查全部闸门
- 新增 `docs/WORKFLOW.md` 端到端指南；`thesis/refs/references.md` 路径统一
- 修复 `.gitignore` 未忽略章节草稿的问题

### v0.3.0

- 新增 GitHub Actions CI（pytest，Python 3.10/3.11/3.12）
- 新增 outline / reduce / format 三个 prompt 模板
- 新增 `thesis/` 目录骨架说明
- helper tools 重写：类型注解、logging、独立退出码；新增 15 个 pytest 用例

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
