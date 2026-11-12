"""One-off migration (2026-11-12): copy the Venue line of each paper card into a `venue`
column of papers/papers.csv, so the catalogue stays the single source of truth."""
import csv
import re
from pathlib import Path

PAPERS = Path(__file__).resolve().parents[1] / "papers"

with open(PAPERS / "papers.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fields = list(reader.fieldnames)
    rows = list(reader)
if "venue" not in fields:
    fields.insert(fields.index("title") + 1, "venue")
for r in rows:
    card = (PAPERS / r["slug"] / "README.md").read_text(encoding="utf-8")
    m = re.search(r"^\| Venue \| (.*?) \|$", card, re.M)
    r["venue"] = m.group(1).strip() if m and m.group(1).strip() != "TODO" else ""
with open(PAPERS / "papers.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
print(sum(bool(r["venue"]) for r in rows), "venues filled of", len(rows))
