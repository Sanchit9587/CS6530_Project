#!/usr/bin/env python3
"""Activity 3 CLI: RTLF on the Bleichenbacher pairs B1..B5 (MatrixSSL 4.6.0) from the authors' dataset.
Also the engine for Activity 4 (use --n / --alpha / --seed / --tag to vary ONE parameter and keep the rest fixed)."""
import _bootstrap  # noqa: F401
import argparse, json, os, platform, sys, time
import numpy as np, pandas as pd
from sca_rtlf import rtlf, rtlf_fast
from sca_rtlf.backends import run_r
from sca_rtlf.data import find_pair_files, load_pair
from sca_rtlf.expectations import PAIRS
from sca_rtlf.reporting import result_row, summarise


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", required=True, help="folder containing the authors' B1..B5 pair CSVs")
    ap.add_argument("--out", default="results/activity3")
    ap.add_argument("--alpha", type=float, default=0.009)
    ap.add_argument("--B", type=int, default=10000)
    ap.add_argument("--n", type=int, default=0, help="random subsample per class (0 = all)")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--backend", choices=["fast", "py", "r"], default="fast")
    ap.add_argument("--rtlf-path", default="third_party/RTLF/rtlf.R")
    ap.add_argument("--tag", default="baseline")
    a = ap.parse_args()

    if "<" in a.data or ">" in a.data:
        sys.exit(f"ERROR: --data was given the placeholder text {a.data!r}. Use the real folder path.")
    if not os.path.isdir(a.data):
        sys.exit(f"ERROR: --data folder {a.data!r} does not exist. Run scripts/fetch_dataset.sh first.")
    os.makedirs(a.out, exist_ok=True)

    files, allc = find_pair_files(a.data)
    print(f"found {len(files)}/10 pair files in {a.data}; missing: {[p for p in PAIRS if p not in files] or 'none'}")
    if not files:
        print(f"ERROR: none of the {len(allc)} CSVs matched the known pair file names.")
        for q in sorted(allc)[:10]:
            print("   sample file:", os.path.relpath(q, a.data))
        sys.exit("Point --data at the folder with the pair CSVs, or adapt FILENAME_MAP in src/sca_rtlf/data.py.")

    engine = {"fast": rtlf_fast, "py": rtlf}.get(a.backend)
    rows, t0 = [], time.time()
    for pair in PAIRS:
        if pair not in files:
            continue
        x, y = load_pair(files[pair], a.n, a.seed)
        res = run_r(x, y, a.alpha, a.rtlf_path) if a.backend == "r" else engine(x, y, a.alpha, a.B, a.seed)
        rows.append(result_row(pair, x, y, res, files[pair]))
    df = summarise(rows)
    df.to_csv(os.path.join(a.out, f"results_{a.tag}.csv"), index=False)
    pd.set_option("display.width", 200)
    print(df.drop(columns=["sha256"]).to_string(index=False))
    print(f"\nleaks: {df.leak.sum()}/{len(df)}   agree-with-code: {df.agrees_with_code.sum()}/{len(df)}   "
          f"agree-with-published-RTLF: {df.agrees_with_paper.sum()}/{len(df)}   ({time.time() - t0:.1f}s)")
    json.dump(dict(args=vars(a), python=platform.python_version(), numpy=np.__version__, pandas=pd.__version__,
                   platform=platform.platform(), pairs=len(df)),
              open(os.path.join(a.out, f"run_info_{a.tag}.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
