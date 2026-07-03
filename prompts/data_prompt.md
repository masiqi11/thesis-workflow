# Thesis Data Prompt

Use this prompt for pre-writing evidence and reference collection.

## Objective
Autonomously review the project, extract real experiment data, and collect the
reference papers the thesis will cite — before any outline or writing begins.

## Stage in pipeline
Runs at `/thesis-data` (stage 2), after `/thesis-intake`. Owns the
"资源就绪闸门" precondition: `/thesis-write` is forbidden until references are ready.

## Inputs (mandatory)

| Path / source | Provider |
|---|---|
| `thesis/notes/topic_analysis.md` | `/thesis-intake` — research questions & evidence gaps |
| `thesis/notes/intake_requirements.md` | `/thesis-intake` — scope, citation rules |
| project codebase, logs, results dirs | user's project |

## Outputs

| File | Content |
|---|---|
| `thesis/notes/data_inventory.md` | available materials mapped to research questions |
| `thesis/notes/experiment_summary.md` | experiments found, with result locations |
| `thesis/notes/metric_tables.md` | ground-truth numbers (the ONLY source writers may cite) |
| `thesis/notes/runtime_env.md` | Python/CUDA/GPU/dependency versions |
| `thesis/refs/papers_inventory.md` | reference list with status (schema below) |
| `thesis/refs/papers_to_download.md` | refs needing manual download, with suggested sources |
| `thesis/refs/paper_data_extracts.md` | key numbers/figures extracted from downloaded papers |
| `thesis/refs/papers/` | downloaded PDFs |

### `papers_inventory.md` schema

```md
| ref_id | title | authors | year | venue | status | local_path | doi_or_url |
|---|---|---|---|---|---|---|---|
```

`status` ∈ `downloaded | metadata-only | need-manual-download | placeholder`

### `metric_tables.md` rule

Every number must come from an actual file (log, csv, results json) and record its
source path. Format: `| metric | value | source_file | extracted_at_step |`.
Numbers without a source line MUST NOT enter this file — writers treat this file
as ground truth, so a fabricated number here poisons the whole thesis.

## Hard rules

1. Reference collection is mandatory, not optional. Prioritize internationally
   accessible sources (arXiv, IEEE, ACM, Springer) for downloadability.
2. For each target paper: search metadata → attempt PDF download → on failure mark
   `need-manual-download` and notify the user immediately with title/DOI/suggested source.
3. Never fabricate metadata. A paper you cannot confirm exists goes to `placeholder`,
   not into the inventory as real.
4. Extract key claims/numbers from downloaded PDFs into `paper_data_extracts.md`
   with page/section pointers — writers cite these, not their memory of the paper.

## Passing gate

`/thesis-write` may proceed only when core references are `downloaded` or
`metadata-only`, and the user has been notified about every `need-manual-download` item.

## Token budget
≤ 15k output tokens across all files.

## Prompt Template

```text
You are running the thesis data-preparation phase.

Read first:
- thesis/notes/topic_analysis.md      (research questions and their evidence gaps)
- thesis/notes/intake_requirements.md

Step 1: Scan the project (training/inference scripts, configs, results dirs, logs).
Step 2: Build metric_tables.md — every number with a source_file pointer.
Step 3: Capture runtime environment into runtime_env.md.
Step 4: Determine the citation fields this thesis needs, search and collect papers:
        metadata → PDF download attempt → status assignment → extraction.
Step 5: Notify the user of every need-manual-download item (title, DOI, source, deadline).

Hard rules:
- No number without a source file. No paper without confirmed metadata.
- Use web search / fetch / DOI-arXiv metadata tools for every reference.

Outputs (create dirs as needed):
- thesis/notes/{data_inventory,experiment_summary,metric_tables,runtime_env}.md
- thesis/refs/{papers_inventory,papers_to_download,paper_data_extracts}.md
- thesis/refs/papers/

Append to thesis/notes/workflow_state.md:
| data | done | refs_ready=<yes/no> | <date> | <note> |
```
