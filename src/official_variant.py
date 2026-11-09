"""Run src/official.py with a recipe from another folder, so that one Colab
session can train more than one Track A recipe.

    python src/official_variant.py track_a_variants/balanced --tag balanced

The folder holds a recipe.py and a selection.csv, like track_a/. Nothing in
official.py changes: it reads the folder from MAS1004_RECIPE_DIR. To release a
variant, copy its two files into track_a/.
"""
import os
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

if len(sys.argv) < 2:
    raise SystemExit(__doc__)
folder = (ROOT / sys.argv[1]).resolve()
for name in ("recipe.py", "selection.csv"):
    if not (folder / name).is_file():
        raise SystemExit(f"{folder / name} is missing")
os.environ["MAS1004_RECIPE_DIR"] = str(folder)
sys.argv = [str(ROOT / "src" / "official.py"), *sys.argv[2:]]
runpy.run_path(sys.argv[0], run_name="__main__")
