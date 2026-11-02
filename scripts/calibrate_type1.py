#!/usr/bin/env python3
"""Type-1 calibration: X and Y from the SAME distribution; false-positive rate vs alpha (simulated analogue of artefact E1b 'same-xy').
Usage: calibrate_type1.py [repetitions=1000] [outdir=results/activity3]"""
import _bootstrap  # noqa: F401
import json, os, sys
import numpy as np
from sca_rtlf import rtlf_fast, wilson

reps = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
out = sys.argv[2] if len(sys.argv) > 2 else "results/activity3"
os.makedirs(out, exist_ok=True)
rng = np.random.default_rng(2026)


def gen(n, discrete):
    v = 3.4e4 * np.exp(rng.normal(0, 0.12, n)) + (rng.random(n) < 0.02) * rng.exponential(2e4, n)
    return np.rint(v) if discrete else v


res = {}
print(f"{'alpha':>6} {'n/class':>8} {'data':>10} {'reps':>5} {'FP':>4} {'FPR':>7}  95% Wilson CI     consistent with <= alpha?")
for discrete in (False, True):
    for alpha in (0.09, 0.009):
        for n in (15000, 30000):
            fp = sum(rtlf_fast(gen(n, discrete), gen(n, discrete), alpha, 10000, seed=int(rng.integers(1 << 31)))["leak"] for _ in range(reps))
            lo, hi = wilson(fp, reps)
            res[f"alpha={alpha},n={n},{'int' if discrete else 'cont'}"] = dict(fp=fp, reps=reps, fpr=fp / reps, ci=[lo, hi])
            print(f"{alpha:>6} {n:>8} {'int-cycles' if discrete else 'continuous':>10} {reps:>5} {fp:>4} {fp / reps:7.3%}  "
                  f"[{lo:.3%},{hi:.3%}]  {'yes' if lo <= alpha else 'NO (investigate)'}", flush=True)
json.dump(res, open(os.path.join(out, f"type1_calibration_{reps}reps.json"), "w"), indent=1)
