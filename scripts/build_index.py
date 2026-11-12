"""Regenerate papers/INDEX.md from papers/papers.csv.

Usage (repo root):  python scripts/build_index.py
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers"

CATEGORIES = {
    "A": "A. Graphs with missing node attributes",
    "B": "B. Graphs with incomplete features and structure",
    "C": "C. Incomplete multi-view learning",
    "D": "D. General data imputation",
    "E": "E. Fairness with missing attributes",
}


def main() -> None:
    with open(PAPERS / "papers.csv", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    lines = [
        "# Paper index",
        "",
        "Generated from `papers.csv` by `scripts/build_index.py`. Do not edit by hand.",
        "",
        f"{len(rows)} papers. Priority 5 = highest (from Haris's reading markers).",
        "",
    ]
    for code, name in CATEGORIES.items():
        group = sorted(
            (r for r in rows if r["category"] == code),
            key=lambda r: (-int(r["priority"]), r["year"], r["slug"]),
        )
        if not group:
            continue
        lines += [f"## {name} ({len(group)})", "", "| Paper | Method | Year | Title | Priority | Status |", "|---|---|---|---|---|---|"]
        for r in group:
            lines.append(
                f"| [{r['slug']}]({r['slug']}/) | {r['method'] or '-'} | {r['year']} | {r['title']} | {r['priority']} | {r['status']} |"
            )
        lines.append("")
    (PAPERS / "INDEX.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"wrote papers/INDEX.md ({len(rows)} papers)")


if __name__ == "__main__":
    main()
