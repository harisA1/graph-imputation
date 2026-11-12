"""Create papers/<slug>/ (README.md + CHANGELOG.md) for every row of papers/papers.csv
that has no directory yet, then rebuild papers/INDEX.md. Existing directories are never touched.

Usage (repo root):  python scripts/scaffold_papers.py
"""
import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers"
TEMPLATE = PAPERS / "_template"

CATEGORIES = {
    "A": "A - missing node attributes",
    "B": "B - incomplete features and structure",
    "C": "C - incomplete multi-view",
    "D": "D - general data imputation",
    "E": "E - fairness with missing attributes",
}


def main() -> None:
    with open(PAPERS / "papers.csv", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    readme_t = (TEMPLATE / "README.md").read_text(encoding="utf-8")
    changelog_t = (TEMPLATE / "CHANGELOG.md").read_text(encoding="utf-8")
    created = 0
    for r in rows:
        d = PAPERS / r["slug"]
        if d.exists():
            continue
        d.mkdir()
        text = (
            readme_t.replace("{METHOD}", r["method"] or r["slug"])
            .replace("{TITLE}", r["title"])
            .replace("{AUTHOR}", r["author"])
            .replace("{YEAR}", r["year"])
            .replace("{CATEGORY}", CATEGORIES.get(r["category"], r["category"]))
            .replace("{PRIORITY}", r["priority"])
            .replace("{PDF}", r["pdf"])
        )
        (d / "README.md").write_text(text, encoding="utf-8", newline="\n")
        (d / "CHANGELOG.md").write_text(changelog_t, encoding="utf-8", newline="\n")
        created += 1
    print(f"created {created} paper directories")
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build_index.py")], check=True)


if __name__ == "__main__":
    main()
