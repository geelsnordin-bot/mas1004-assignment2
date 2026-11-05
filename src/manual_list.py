"""Nordin's own list of training photos to drop (track_a/manual_list.csv).

Each row names photos of one city: commons:<id>, commons:<first id>-<last id>,
or youtube:<video id>. keep is how many of them stay (0 drops them all; the
ones kept are spread evenly over the sorted names). reason goes into dropped.csv.

    python src/manual_list.py sheets                  contact sheets of what would be dropped
    python src/manual_list.py apply --files <list.gz> write selection.csv and dropped.csv

sheets needs the photos (on Colab). apply needs only the file names: either the
photos in data/starter/train or the list that src/inventory.py writes.
"""
import argparse
import csv
import gzip
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import curate  # noqa: E402
import rules  # noqa: E402

RULES = ROOT / "track_a" / "manual_list.csv"


def train_files(files):
    """'<city>/<name>' for every training photo, sorted."""
    if files:
        with gzip.open(files, "rt") as f:
            return sorted(line.strip()[len("train/"):] for line in f if line.startswith("train/"))
    return [f"{c}/{p.name}" for p, c in rules.list_photos(curate.TRAIN)]


def matches(rule, city, name):
    if city != rule["city"]:
        return False
    kind, _, what = rule["match"].partition(":")
    stem = Path(name).stem
    if kind == "youtube":
        return stem.startswith(f"youtube_{what}_")
    if kind == "commons" and stem.startswith("commons_") and stem[8:].isdigit():
        number = int(stem[8:])
        first, _, last = what.partition("-")
        return int(first) <= number <= int(last or first)
    return False


def spread(items, keep):
    """keep items spread evenly over the list."""
    if keep <= 0:
        return []
    if keep >= len(items):
        return list(items)
    return [items[round(i * (len(items) - 1) / max(keep - 1, 1))] for i in range(keep)] if keep > 1 \
        else [items[len(items) // 2]]


def decide(paths):
    """[(rule, matched paths, dropped paths)] in the order of the list."""
    with open(RULES, newline="", encoding="utf-8") as f:
        rule_rows = list(csv.DictReader(f))
    out = []
    for rule in rule_rows:
        mine = [p for p in paths if matches(rule, *p.split("/", 1))]
        kept = set(spread(mine, int(rule["keep"])))
        out.append((rule, mine, [p for p in mine if p not in kept]))
    return out


def report(decisions):
    total = 0
    for rule, mine, dropped in decisions:
        flag = "   <-- matches nothing, check the ids" if not mine else ""
        print(f"{rule['city']:<7}{rule['match']:<34} found {len(mine):>4}  drop {len(dropped):>4}  "
              f"({rule['reason']}){flag}")
        total += len(dropped)
    print(f"{total} photos to drop")


def cmd_sheets(args):
    decisions = decide(train_files(None))
    report(decisions)
    for city in rules.CITIES:
        items = [(curate.TRAIN / p, f"{rule['reason']}") for rule, _, dropped in decisions
                 if rule["city"] == city for p in dropped]
        if items:
            names = curate.draw_sheets(f"manual_{city}", items)
            print(f"{city}: {len(items)} photos on {len(names)} sheets, results/curate/manual_{city}_NN.png")


def cmd_apply(args):
    paths = train_files(args.files)
    decisions = decide(paths)
    report(decisions)
    reason = {p: rule["reason"] for rule, _, dropped in decisions for p in dropped}
    if curate.DROPPED.exists():
        raise SystemExit("track_a/dropped.csv exists already; this writes the first selection")
    curate.write_selection([p for p in paths if p not in reason])
    now = datetime.now().isoformat(timespec="seconds")
    with open(curate.DROPPED, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["path", "reason", "when"])
        w.writerows([p, why, now] for p, why in reason.items())
    print(f"selection.csv: {len(paths) - len(reason)} of {len(paths)} training photos")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("sheets").set_defaults(func=cmd_sheets)
    apply = sub.add_parser("apply")
    apply.add_argument("--files", help="the list of starter files from src/inventory.py")
    apply.set_defaults(func=cmd_apply)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
