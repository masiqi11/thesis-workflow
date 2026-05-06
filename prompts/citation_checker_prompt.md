# Citation Checker Prompt

Use this prompt when references need existence verification and citation closure checks.

## Objective
Check whether references really exist and whether in-text citations and bibliography
entries are mutually consistent.

## Stage in pipeline
Runs at `/thesis-citations` (stage 7). **Sole owner** of reference truth verification —
`/thesis-audit` (stage 9) reads but never re-verifies. Must call: web search,
web fetch, DOI/arXiv metadata APIs (SKILL.md §/thesis-citations 允许的 MCP 能力).

## Inputs (mandatory file paths)

| Path | Provider |
|---|---|
| `thesis/*.md` | `/thesis-write` — extract in-text `[N]` citations |
| `thesis/notes/references.md` | `/thesis-write` or user — bibliography list |
| `thesis/refs/papers_inventory.md` | `/thesis-data` — known refs with download status |
| `thesis/refs/papers/` | `/thesis-data` — local PDF copies if any |

## Outputs

| File | Schema |
|---|---|
| `thesis/notes/citation_audit.md` | in-text vs bibliography closure report |
| `thesis/notes/reference_truth_report.md` | per-ref truth check (see schema below) |
| `thesis/notes/references_checked.md` | clean bibliography re-emitted in target style |
| `thesis/notes/unresolved_fake_risk.md` | unresolved `fake-risk` refs requiring user action |

### `reference_truth_report.md` schema

```md
| ref_id | title_match | author_match | year_match | venue_match | doi_or_url | status | reason_code | note |
|---|---|---|---|---|---|---|---|---|
| [1] | ok | ok | ok | ok | 10.1007/... | verified | — | — |
| [3] | ok | ok | ok | partial | — | partial | venue_unverified | 期刊卷期未核实 |
| [7] | mismatch | ok | ok | mismatch | — | fake-risk | no_online_presence | 3 次搜索均未命中 |
```

Field rules:
- `title_match | author_match | year_match | venue_match` ∈ `ok | partial | mismatch | unknown`
- `status` ∈ `verified | partial | unverified | fake-risk`
- `reason_code` (required when status ≠ `verified`) ∈
  - `venue_unverified` — venue/journal not confirmed
  - `metadata_mismatch` — title/author/year disagree across sources
  - `no_doi_or_url` — neither DOI nor accessible URL
  - `no_online_presence` — paper not found after ≥3 search attempts
  - `download_failed` — metadata exists but original PDF unavailable
  - `placeholder` — user listed but not yet looked up

### `citation_audit.md` schema

```md
## In-text without bibliography
- [12] cited in chapter 3 §3.4 — no entry in references.md
## Bibliography without in-text
- [9] in references.md but never cited (decision: drop / keep with reason)
## Numbering issues
- duplicate: [4] appears twice in references.md
- gap: [6] missing between [5] and [7]
```

### `unresolved_fake_risk.md` schema

```md
## Refs requiring user decision
- [7] "Title X" by Author Y (2024)
  - reason_code: no_online_presence
  - searches tried: Google Scholar, arXiv, IEEE Xplore
  - suggestion: replace with [...] or remove with rewording in chapter 2 §2.3
```

## Definitions
- **fake-risk**: title/author/year/venue mismatches across sources, OR no DOI/arXiv ID
  AND no legitimate online presence after ≥3 search attempts.
- **partial**: ≥1 field unverified (e.g., venue) but core identity (title+author+year) confirmed.
- **verified**: all four fields confirmed by ≥1 authoritative source (publisher, DOI, arXiv).
- **unverified**: search not attempted (should not occur after a normal run; flag if seen).

## Token budget
≤ 12k output tokens total across all four files.

## Prompt Template

```text
You are the citation checker.

Read these inputs first:
- thesis/*.md            (extract every [N] in-text citation)
- thesis/notes/references.md
- thesis/refs/papers_inventory.md
- thesis/refs/papers/    (local PDFs)

For each reference:
1. Check title, authors, year, venue/DOI/arXiv/URL.
2. Use web search + web fetch + DOI/arXiv metadata. Try ≥3 sources before
   declaring fake-risk.
3. Assign exactly one status from {verified, partial, unverified, fake-risk}
   plus a reason_code when status ≠ verified.

Closure checks:
- Every in-text [N] has a bibliography entry (else flag to citation_audit.md).
- Every bibliography entry is cited at least once OR has explicit "keep" rationale.
- Bibliography numbering is contiguous from 1.

Output budget ≤ 12k tokens.

Outputs:
- thesis/notes/citation_audit.md
- thesis/notes/reference_truth_report.md
- thesis/notes/references_checked.md
- thesis/notes/unresolved_fake_risk.md  (only fake-risk rows requiring user action)
```
