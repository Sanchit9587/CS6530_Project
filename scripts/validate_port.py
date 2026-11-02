#!/usr/bin/env python3
"""Cross-check the student port against the authors' R output on RTLF's shipped examples (alpha = 0.09).
R reference values were taken from `Rscript rtlf.R` runs (see results/activity3/rtlf_R_example-*.log and the team screenshots)."""
import _bootstrap  # noqa: F401
import sys, time
import pandas as pd
from sca_rtlf import rtlf, rtlf_fast

R_REF = {"example-1": dict(diff=[14, 12, 14, 22, 22, 26, 24, 12, 14], thr=[22, 14, 12, 12, 14, 16, 26, 26, 58], leak=True),
         "example-2": dict(diff=[8, 12, 12, 14, 14, 12, 0, 8, 52], thr=[28, 15, 14, 14, 14, 20, 26, 25, 63], leak=False)}
d = sys.argv[1] if len(sys.argv) > 1 else "third_party/RTLF/examples"
B = int(sys.argv[2]) if len(sys.argv) > 2 else 10000
slow = "--slow" in sys.argv
for name, ref in R_REF.items():
    df = pd.read_csv(f"{d}/{name}.csv")
    x = df.loc[df.V1 == "X", "V2"].values; y = df.loc[df.V1 == "Y", "V2"].values
    for label, fn in ([("literal", rtlf)] if slow else []) + [("fast", rtlf_fast)]:
        t = time.time(); r = fn(x, y, 0.09, B, seed=1)
        ok = r["diff"].astype(int).tolist() == ref["diff"] and r["leak"] == ref["leak"]
        print(f"{name} [{label}] n={r['n']} leak={r['leak']} (R: {ref['leak']}) diffs identical to R: {ok}  t={time.time() - t:.2f}s")
        print("   thr  :", r["thr"].astype(int).tolist(), "\n   thr R:", ref["thr"])
