# Reporting checklist for real-world studies

This repository contains a Codex skill for reviewing real-world study reports in clinical comprehensive evaluation of medicines. A review records 36 ratings across five domains. Each positive rating cites an excerpt and its PDF page so a reviewer can inspect the evidence.

## Getting started

Copy the [clinical-rwe-qc folder](clinical-rwe-qc/) into a project's `.agents/skills/` directory. Open the project in Codex and give it access to the report you want to review. [Codex skill setup](https://developers.openai.com/codex/skills)

> Use $clinical-rwe-qc to review report.pdf. Save the 36 ratings with their reasons, source excerpts and physical page numbers. Report the five domain scores and flag borderline judgments.

The [scoring guide](clinical-rwe-qc/references/scoring-guide.md) defines the rules. The [file format](clinical-rwe-qc/references/output.md) describes how to record page text and ratings. Try the validator with the fictional report from the repository root. It requires Python 3.

```sh
python3 clinical-rwe-qc/scripts/validate_scores.py examples/synthetic-pages.json examples/synthetic-scores.json
```

The example scores 23 out of 36. The script checks that all items are present and that each excerpt occurs on the assigned page. Reviewers decide whether the cited text supports each rating.

## Relation to the study

The study used a frozen guide with examples from the development reports. This repository keeps the item numbering, scoring scale and evidence requirements, with rewritten instructions and fictional examples. The study's performance estimates apply to the frozen guide.

The criteria follow the 2024 [quality-control guideline](https://doi.org/10.12458/HDPR.202408073) and its [commentary](https://doi.org/10.12458/HDPR.202408074). The checklist assesses what a study reports. Clinical effectiveness and treatment recommendations require separate assessments.
