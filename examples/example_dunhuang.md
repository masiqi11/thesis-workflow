# Example: thesis-workflow on a graduation project

## Scenario

Topic: 基于 U-Net 的敦煌壁画损伤区域自动分割研究

## Recommended command chain

```text
/thesis-intake --assist
/thesis-data --auto
/thesis-outline --draft
/thesis-assets --auto
/thesis-write chapter=5 --draft
/thesis-write chapter=2 --draft
/thesis-content --safe
/thesis-citations --safe
/thesis-format --draft
/thesis-audit --safe
/thesis-build
```

## What this example demonstrates

- Intake before formal writing
- Evidence-driven chapter generation
- Citation truth checking
- Format gating before final build
