"""Adapter to the authors' reference implementation (R). Exit codes of rtlf.R: 11 = leak detected, 10 = none."""
import os, subprocess, tempfile
import numpy as np, pandas as pd


def run_r(x, y, alpha, rtlf_path="third_party/RTLF/rtlf.R"):
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, "t.csv")
        pd.DataFrame({"V1": ["X"] * len(x) + ["Y"] * len(y), "V2": np.r_[x, y]}).to_csv(f, index=False)
        p = subprocess.run(["Rscript", rtlf_path, "-i", f, "-a", str(alpha), "-q", "-o", os.path.join(d, "o.json")],
                           capture_output=True, text=True)
    return dict(leak=(p.returncode == 11), rc=p.returncode, diff=None, thr=None, sig=None)
