"""Regenerate papers/INDEX.md and the paper tables in README.md from papers/papers.csv.

Usage (repo root):  python scripts/build_index.py
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers"

CATEGORIES = {
    "A": "Graphs with missing node attributes",
    "B": "Graphs with incomplete features and structure",
    "C": "Incomplete multi-view learning",
    "D": "General data imputation",
    "E": "Fairness with missing attributes",
}
STATUS = {
    "not-started": "planned",
    "in-progress": "in progress",
    "reproduced": "reproduced",
    "partial": "partial",
    "failed": "not reproduced",
    "skipped": "skipped",
}
START, END = "<!-- PAPERS:START -->", "<!-- PAPERS:END -->"


def code_link(url: str) -> str:
    if not url:
        return "-"
    return f"[{url.removeprefix('https://github.com/')}]({url})"


def name(r: dict) -> str:
    return r["method"] or f"{r['author']} et al."


def build_index(rows: list) -> str:
    lines = [
        "# Paper index",
        "",
        "Generated from `papers.csv` by `scripts/build_index.py`. Do not edit by hand.",
        "",
        f"{len(rows)} papers. Priority 5 = highest. Tier 1 = start here "
        "(see [`reports/reproduction-suitability.md`](../reports/reproduction-suitability.md)).",
        "",
    ]
    for code, cat in CATEGORIES.items():
        group = sorted(
            (r for r in rows if r["category"] == code),
            key=lambda r: (int(r["repro_tier"]), -int(r["priority"]), r["year"], r["slug"]),
        )
        if not group:
            continue
        lines += [
            f"## {code}. {cat} ({len(group)})",
            "",
            "| Paper | Method | Venue | Title | Code | Priority | Tier | Status |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for r in group:
            lines.append(
                f"| [{r['slug']}]({r['slug']}/) | {r['method'] or '-'} | {r['venue']} | {r['title']} "
                f"| {code_link(r['code_url'])} | {r['priority']} | {r['repro_tier']} | {r['status']} |"
            )
        lines.append("")
    return "\n".join(lines)


def build_readme_tables(rows: list) -> str:
    lines = []
    for code, cat in CATEGORIES.items():
        group = sorted((r for r in rows if r["category"] == code), key=lambda r: (r["year"], r["slug"]))
        if not group:
            continue
        lines += [
            f"### {cat}",
            "",
            "| Method | Paper | Venue | Official code | Status |",
            "|---|---|---|---|---|",
        ]
        for r in group:
            lines.append(
                f"| [{name(r)}](papers/{r['slug']}/) | {r['title']} | {r['venue']} "
                f"| {code_link(r['code_url'])} | {STATUS.get(r['status'], r['status'])} |"
            )
        lines.append("")
    return "\n".join(lines).rstrip("\n")


def main() -> None:
    with open(PAPERS / "papers.csv", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    (PAPERS / "INDEX.md").write_text(build_index(rows), encoding="utf-8", newline="\n")
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    if START in text and END in text:
        head, rest = text.split(START, 1)
        tail = rest.split(END, 1)[1]
        text = f"{head}{START}\n{build_readme_tables(rows)}\n{END}{tail}"
        readme.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote papers/INDEX.md and README.md tables ({len(rows)} papers)")


if __name__ == "__main__":
    main()
