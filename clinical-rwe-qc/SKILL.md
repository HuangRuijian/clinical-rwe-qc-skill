---
name: clinical-rwe-qc
description: Appraise reporting of real-world studies within clinical comprehensive evaluation of medicines. Apply 36 criteria across five domains and return binary judgments with page-level evidence. Use for report quality appraisal and expert review of appraisal outputs.
---

# Clinical real-world study reporting appraisal

Read [the scoring guide](references/scoring-guide.md) before assigning scores. For ambiguous boundaries, consult [the synthetic examples](references/synthetic-examples.md). Appraise the real-world study component of a complete report and its supplied appendices. Keep its observations and analyses separate from evidence cited from other studies, and distinguish completed methods from plans.

## Prepare the source

1. Inventory the report's PDF pages, counting the first physical page as 1. Use available PDF text extraction and inspect image-only pages, tables and figures that may contain evidence. Correct extraction or OCR against the page before using doubtful text.
2. Save the evidence-bearing text locally as `pages.json`, following [the output contract](references/output.md). Keep physical page numbers when the printed numbering differs. Record missing or unreadable pages. Stop short of a full-report score when material pages or appendices are unavailable.

## Score and verify

1. Use all 36 items once in item order. Search across methods, results, tables and appendices where relevant. Use 1 when the report contains criterion-specific evidence and 0 when the criterion is unmet, unsupported in the supplied report, or inapplicable. Explain the distinction in the reason. Keep the denominator fixed at 36.
2. For a score of 1, include at least one short verbatim excerpt in the source language and its physical PDF page number. Explain what the excerpt supports. For 0, document the missing information or reason the criterion fails. An excerpt for a 0 is optional and can show contrary evidence. Separate a claim made by the report from independently confirmed implementation.
3. Write `scores.json` using the output contract. Run `python3 scripts/validate_scores.py pages.json scores.json` relative to the skill folder, using the actual paths to the two inputs. Resolve validation errors against the source and rerun. Use the validator's domain totals. If asked to produce a review table, include those totals and the item reasons and excerpts.
4. Flag borderline ratings for expert review. The output concerns reporting against this instrument. Decisions on clinical effectiveness, treatment choice and policy adoption require a separate evaluation.
