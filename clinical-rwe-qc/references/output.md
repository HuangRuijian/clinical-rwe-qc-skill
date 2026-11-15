# Input and output contract

Use UTF-8 JSON. The source object contains a `pages` array of objects with a positive integer `page` and string `text`. Use the physical page order of the supplied report. Review OCR against the underlying page. If the report is incomplete, document the gap in the review and withhold an overall appraisal.

The scoring object contains `report_id` and an `items` array. Each item contains `item_id`, integer `score` (0 or 1), nonempty `reason`, and an `evidence` array. Each evidence entry has an integer `page` and nonempty `quote`. Each score of 1 needs at least one excerpt. For a score of 0 an empty array is permitted. Each excerpt must be contiguous on the cited physical page after Unicode and whitespace normalization.

```json
{
  "report_id": "example-report",
  "items": [
    {
      "item_id": 4,
      "score": 1,
      "reason": "The report identifies the source population and how it was enumerated.",
      "evidence": [
        {"page": 2, "quote": "Eligible records came from all consecutive clinic visits."}
      ]
    }
  ]
}
```

The example illustrates one item. A valid score file contains items 1 through 36. The validator prints JSON totals and exits with a nonzero status if a required field, unique identifier, score or page excerpt fails validation. It does not judge whether a quotation substantively meets a criterion. Retain extracted text and score records according to the terms governing the source report.
