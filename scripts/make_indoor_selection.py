"""All training photos except the indoor groups from my own drop list.

Writes track_a_variants/indoor/selection.csv. The indoor groups are the rows
of track_a/dropped.csv with one of the reasons below; every other photo stays.
"""
import csv
import gzip
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDOOR = {"many shopping mall interiors", "Sunflower occupation: indoors", "fire brigade series: indoors"}

with gzip.open(ROOT / "results/starter_files.txt.gz", "rt") as f:
    train = [l.strip()[len("train/"):] for l in f if l.startswith("train/")]
with open(ROOT / "track_a/dropped.csv", newline="", encoding="utf-8") as f:
    out = {r["path"] for r in csv.DictReader(f) if r["reason"] in INDOOR}
keep = [p for p in train if p not in out]
with open(ROOT / "track_a_variants/indoor/selection.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["path"])
    w.writerows([p] for p in keep)
print(f"{len(keep)} of {len(train)} training photos; {len(out)} indoor photos left out")
