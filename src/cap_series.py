"""Run 2: at most N frames of one YouTube video (and optionally of one photographer) per city.

Works on the current track_a/selection.csv. The group of a photo comes from
results/groups.csv.gz (src/export_groups.py): a YouTube channel's video by its
video id, every other photo by its photographer. The photos kept of a group are
spread evenly over its sorted names. What is left out is added to dropped.csv.

    python src/cap_series.py --max 20                     prints what it would leave out
    python src/cap_series.py --max 20 --write             and writes it
    python src/cap_series.py --max 5 --series-max 100     also at most 100 per photographer
"""
import argparse
import collections
import csv
import gzip
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import curate  # noqa: E402
from manual_list import spread  # noqa: E402

GROUPS = ROOT / "results" / "groups.csv.gz"


def group_of(path, groups):
    """('video', id) for a YouTube frame, ('series', photographer) otherwise."""
    stem = Path(path).stem
    if stem.startswith("youtube_"):
        return "video", stem.rsplit("_", 1)[0]
    return "series", groups.get(path, stem)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--max", type=int, default=5)
    ap.add_argument("--series-max", type=int, help="also at most this many per photographer")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    with gzip.open(GROUPS, "rt", newline="") as f:
        groups = {r["path"]: r["group"] for r in csv.DictReader(f)}
    selection = curate.read_selection()
    members = collections.defaultdict(list)
    for p in selection:
        members[(p.split("/")[0], *group_of(p, groups))].append(p)

    reason = {}
    for (city, kind, _), paths in members.items():
        cap = args.max if kind == "video" else args.series_max
        if cap is None:
            continue
        paths = sorted(set(paths))
        kept = set(spread(paths, cap))
        for p in paths:
            if p not in kept:
                reason[p] = f"max {cap} per {'video' if kind == 'video' else 'fotoserie (fotograaf)'}"

    kept = [p for p in selection if p not in reason]
    print(f"{'city':<8}{'before':>8}{'after':>8}{'video':>8}{'series':>8}")
    for city in curate.CITIES:
        mine = [p for p in selection if p.startswith(city + "/")]
        gone = [p for p in mine if p in reason]
        video = sum(1 for p in gone if "video" in reason[p])
        print(f"{city:<8}{len(mine):>8}{len(mine) - len(gone):>8}{video:>8}{len(gone) - video:>8}")
    print(f"{len(reason)} photos left out, {len(kept)} kept")
    if args.write:
        curate.write_selection(kept)
        now = datetime.now().isoformat(timespec="seconds")
        with open(curate.DROPPED, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerows([p, why, now] for p, why in reason.items())
        print("wrote track_a/selection.csv and added to track_a/dropped.csv")


if __name__ == "__main__":
    main()
