# thesis-workflow

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
