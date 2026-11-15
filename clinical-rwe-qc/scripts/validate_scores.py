"""Check 36 report judgments against page text and calculate their scores."""

import argparse
import json
from pathlib import Path
import sys
from unicodedata import normalize


DOMAINS = {
    "study_objectives": range(1, 4),
    "study_design": range(4, 11),
    "data_sources_and_preprocessing": range(11, 19),
    "statistical_analysis": range(19, 29),
    "results_and_interpretation": range(29, 37),
}


def normalized(text):
    return " ".join(normalize("NFKC", text).split())


def require(condition, message):
    if not condition:
        raise ValueError(message)


def page_text(document):
    require(isinstance(document, dict), "Source must be a JSON object")
    entries = document.get("pages")
    require(isinstance(entries, list) and entries, "Source must contain a nonempty pages array")
    pages = {}
    for entry in entries:
        require(isinstance(entry, dict), "Each page must be an object")
        page, text = entry.get("page"), entry.get("text")
        require(type(page) is int and page >= 1, "Physical page numbers must be positive integers")
        require(page not in pages, f"Duplicate physical page {page}")
        require(isinstance(text, str), f"Page {page} text must be a string")
        pages[page] = normalized(text)
    require(set(pages) == set(range(1, len(pages) + 1)), "Physical page numbering has gaps")
    return pages


def score_report(source, judgment):
    pages = page_text(source)
    require(isinstance(judgment, dict), "Scores must be a JSON object")
    report_id = judgment.get("report_id")
    require(isinstance(report_id, str) and report_id.strip(), "Provide a report_id")
    items = judgment.get("items")
    require(isinstance(items, list) and len(items) == 36, "Provide all 36 items")

    by_id = {}
    for item in items:
        require(isinstance(item, dict), "Each item must be an object")
        item_id, score = item.get("item_id"), item.get("score")
        require(type(item_id) is int and item_id in range(1, 37), "item_id must be an integer from 1 to 36")
        require(item_id not in by_id, f"Duplicate item {item_id}")
        require(type(score) is int and score in (0, 1), f"Item {item_id} score must be the integer 0 or 1")
        reason = item.get("reason")
        require(isinstance(reason, str) and reason.strip(), f"Item {item_id} needs a reason")
        evidence = item.get("evidence")
        require(isinstance(evidence, list), f"Item {item_id} evidence must be an array")
        require(score == 0 or evidence, f"Item {item_id} has no excerpt for a score of 1")
        for entry in evidence:
            require(isinstance(entry, dict), f"Item {item_id} evidence must be an object")
            page, quote = entry.get("page"), entry.get("quote")
            require(type(page) is int and page in pages, f"Item {item_id} cites an unknown physical page")
            require(isinstance(quote, str) and normalized(quote), f"Item {item_id} has an empty excerpt")
            require(normalized(quote) in pages[page], f"Item {item_id} excerpt was not found on page {page}")
        by_id[item_id] = score

    domains = {
        name: {"score": sum(by_id[number] for number in numbers), "maximum": len(numbers)}
        for name, numbers in DOMAINS.items()
    }
    return {"report_id": report_id, "domain_scores": domains, "total_score": sum(by_id.values()), "maximum": 36}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Prepared page text as JSON")
    parser.add_argument("scores", type=Path, help="Report judgments as JSON")
    args = parser.parse_args()
    try:
        source = json.loads(args.source.read_text(encoding="utf-8"))
        judgments = json.loads(args.scores.read_text(encoding="utf-8"))
        result = score_report(source, judgments)
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
