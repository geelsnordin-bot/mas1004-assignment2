"""The photographer or channel of every training photo, from data/starter/ATTRIBUTION.csv.

Writes results/groups.csv.gz (path, source, group), so that a selection can
limit how many photos of one series it keeps without the photos at hand.
"""
import csv
import gzip
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATTRIBUTION = ROOT / "data" / "starter" / "ATTRIBUTION.csv"
OUT = ROOT / "results" / "groups.csv.gz"


def main():
    with open(ATTRIBUTION, newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["file"].startswith("train/")]
    OUT.parent.mkdir(exist_ok=True)
    with gzip.open(OUT, "wt", newline="") as f:
        w = csv.writer(f)
        w.writerow(["path", "source", "group"])
        w.writerows([r["file"][len("train/"):], r["source"], r["group"]] for r in rows)
    print(f"wrote {OUT.relative_to(ROOT)} ({len(rows)} training photos, "
          f"{len({r['group'] for r in rows})} groups)")


if __name__ == "__main__":
    main()
