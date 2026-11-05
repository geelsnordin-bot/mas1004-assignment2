"""Counts of the starter photos per split, city and source, and a list of every file.

Writes results/inventory_before.csv (split, city, source, photos, groups) and
results/starter_files.txt.gz (one path per line, split/city/name), and prints
the counts. Reads nothing but the file names.
"""
import collections
import csv
import gzip
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import rules  # noqa: E402

STARTER = ROOT / "data" / "starter"
OUT = ROOT / "results"


def source_and_group(name):
    """('youtube', 'youtube_<video id>') for a video frame, ('commons', name) otherwise."""
    stem = Path(name).stem
    source = stem.split("_")[0]
    if source == "youtube":
        return source, stem.rsplit("_", 1)[0]
    return source, stem


def main():
    OUT.mkdir(exist_ok=True)
    rows, paths = [], []
    for split in ("train", "val"):
        photos = collections.Counter()
        groups = collections.defaultdict(set)
        for path, city in rules.list_photos(STARTER / split):
            source, group = source_and_group(path.name)
            photos[city, source] += 1
            groups[city, source].add(group)
            paths.append(f"{split}/{city}/{path.name}")
        for (city, source), n in sorted(photos.items()):
            rows.append({"split": split, "city": city, "source": source,
                         "photos": n, "groups": len(groups[city, source])})
    with open(OUT / "inventory_before.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["split", "city", "source", "photos", "groups"])
        w.writeheader()
        w.writerows(rows)
    with gzip.open(OUT / "starter_files.txt.gz", "wt") as f:
        f.write("\n".join(paths) + "\n")
    print(f"{'split':<6}{'city':<8}{'source':<9}{'photos':>7}{'groups':>7}")
    for r in rows:
        print(f"{r['split']:<6}{r['city']:<8}{r['source']:<9}{r['photos']:>7}{r['groups']:>7}")
    print(f"wrote results/inventory_before.csv and results/starter_files.txt.gz ({len(paths)} files)")


if __name__ == "__main__":
    main()
