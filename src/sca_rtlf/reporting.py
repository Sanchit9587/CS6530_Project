"""Building and summarising per-pair result tables."""
import hashlib
import numpy as np, pandas as pd
from .expectations import CODE_EXPECT, PAPER_RTLF


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def result_row(pair, x, y, res, path):
    diff, thr, sig = res.get("diff"), res.get("thr"), res.get("sig")
    return dict(pair=pair, n_per_class=len(x), leak=bool(res["leak"]),
                max_excess=None if diff is None else float(np.max(diff - thr)),
                mean_diff=float(np.mean(y) - np.mean(x)),
                deciles_flagged="" if sig is None else ",".join(f"{i + 1}0%" for i in np.where(sig)[0]),
                expected_by_code=CODE_EXPECT[pair], published_rtlf=PAPER_RTLF[pair], sha256=sha256(path)[:16])


def summarise(rows):
    df = pd.DataFrame(rows)
    df["agrees_with_code"] = df.leak == df.expected_by_code
    df["agrees_with_paper"] = df.leak == df.published_rtlf
    return df
