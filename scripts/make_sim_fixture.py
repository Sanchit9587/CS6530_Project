#!/usr/bin/env python3
"""SIMULATED stand-in for the MatrixSSL dataset. NOT the authors' measurements, NOT evidence about MatrixSSL.
Purpose: exercise run_matrixssl_study.py end-to-end where Zenodo is unreachable, with KNOWN ground truth.
Model (ns): early-exit structure of Algorithm 3: B2 exits at line 3, B4/B5 at line 14 (B5 scans more loop
iterations), B1/B3 at line 21; B1 and B3 execute identical instructions. Noise: skewed log-normal + rare spikes."""
import _bootstrap  # noqa: F401
import sys, os, numpy as np, pandas as pd
from sca_rtlf.data import FILENAME_MAP as MAP
out, n, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 7
rng = np.random.default_rng(seed)
BASE = 52000.0
EXTRA = {"B1": 900.0, "B3": 900.0, "B2": 0.0, "B4": 430.0, "B5": 400.0}   # ns of extra work per vector (B1==B3 on purpose)
def sample(v, n):
    noise = rng.lognormal(mean=np.log(3000), sigma=0.45, size=n)       # skewed jitter
    spike = (rng.random(n) < 0.01) * rng.exponential(20000, n)           # rare scheduler spikes
    return BASE + EXTRA[v] + noise + spike
os.makedirs(out, exist_ok=True)
inv = {v: k for k, v in MAP.items()}
for pair in inv:
    a, b = pair[:2], pair[2:]
    # file name 'XvsY': MODIFIED vs BASELINE as in the authors' naming; direction is irrelevant for a two-sided test
    xs, ys = sample(b, n), sample(a, n)
    pd.DataFrame({"V1": ["BASELINE"]*n + ["MODIFIED"]*n, "V2": np.r_[xs, ys]}).to_csv(os.path.join(out, inv[pair] + "_SIM.csv"), index=False)
print("wrote simulated fixture to", out)
