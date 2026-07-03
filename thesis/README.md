# thesis/

This directory is created by the thesis-workflow skill during a real project.
It is **not committed to the skill repository** (covered by `.gitignore`).

When you run `/thesis-intake` on your actual thesis project, the skill will
create and populate the following structure here:

```text
thesis/
├── README.md          ← this file (only committed in the skill repo)
│
├── notes/             ← all workflow notes and audit reports (gitignored)
│   ├── workflow_state.md           ← gate status board (log; gate files are truth)
│   ├── topic_analysis.md           ← Step 0: topic decomposition & feasibility
│   ├── template_requirements.md    ← single source of truth for format rules
│   ├── intake_requirements.md
│   ├── missing_requirements.md
│   ├── thesis_outline.md
│   ├── chapter_matrix.md
│   ├── figure_plan.md
│   ├── reference_plan.md
│   ├── data_inventory.md
│   ├── experiment_summary.md
│   ├── metric_tables.md            ← ground-truth numbers (source-file pointers)
│   ├── runtime_env.md
│   ├── assets_manifest.md          ← incl. data_provenance column
│   ├── chapter_evidence_map.md
│   ├── unresolved_issues.md
│   ├── content_audit.md
│   ├── citation_audit.md
│   ├── reference_truth_report.md
│   ├── unresolved_fake_risk.md
│   ├── ai_risk_audit.md
│   ├── claim_evidence_matrix.md
│   ├── prioritized_fix_list.md
│   ├── format_audit.md
│   ├── format_ready_chapters.md
│   ├── reduce_report.md
│   ├── sync_report.md
│   ├── defense_outline.md
│   ├── innovation_points.md
│   └── qa_bank.md
│
├── refs/              ← references and downloaded papers (gitignored)
│   ├── references.md               ← bibliography, maintained by /thesis-write
│   ├── references_checked.md       ← verified bibliography from /thesis-citations
│   ├── papers_inventory.md
│   ├── papers_to_download.md
│   ├── paper_data_extracts.md
│   └── papers/        ← downloaded PDFs
│
├── figures/           ← figure assets (gitignored)
│   ├── *.png / *.jpg / *.svg
│   ├── prompts/       ← drawing prompts for concept diagrams
│   └── scripts/       ← Python scripts generating experiment figures
│
├── chapter_1.md       ← chapter drafts (gitignored via thesis/*.md)
├── chapter_2.md
├── ...
│
└── release/           ← final build outputs (gitignored)
    ├── 毕业论文_<姓名>.docx
    ├── 毕业论文_<姓名>_验收版.docx
    ├── 毕业论文_<姓名>.pdf
    ├── build_manifest.md
    └── ARCHIVE_INDEX.md
```

Gate status at any point:

```bash
python tools/check_gates.py --thesis-dir thesis
```

Full journey guide: [docs/WORKFLOW.md](../docs/WORKFLOW.md).

## Starting a new thesis project

```bash
# Copy the skill to your Claude Code skills directory
cp -r path/to/thesis-workflow ~/.claude/skills/thesis-workflow

# In Claude Code, start the workflow
/thesis-intake --assist
```

The skill will auto-create `thesis/notes/`, `thesis/refs/`, `thesis/figures/`,
and `thesis/release/` as needed. You do not need to create them manually.

## Copying the template_requirements starter

```bash
cp ~/.claude/skills/thesis-workflow/docs/template_requirements_template.md \
   thesis/notes/template_requirements.md
```

Then fill in your school's rules before running `/thesis-intake`.
