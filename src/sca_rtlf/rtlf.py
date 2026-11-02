"""Core statistical test: student numpy implementation of RTLF's decision rule (Algorithms 1 and 2 of Dunsche et al., USENIX Sec '24).

The authors' R tool (third_party/RTLF/rtlf.R) is the reference; this module exists for speed and for sweeps.
Mirrors R quantile(type=2) and the artefact wrapper: per-decile threshold at 1 - alpha/9, max of the x-side and y-side thresholds.
"""
import numpy as np

PROBS = np.arange(1, 10) / 10.0


def _is_int(v):
    return abs(v - round(v)) < 1e-9


def deciles_type2(sorted_x):
    """Deciles of already-sorted data, R quantile(type=2): average the two neighbours when n*p is an integer."""
    n = len(sorted_x)
    out = np.empty(9)
    for k, p in enumerate(PROBS):
        np_ = n * p
        if _is_int(np_):
            j = int(round(np_))
            out[k] = 0.5 * (sorted_x[j - 1] + sorted_x[j])
        else:
            out[k] = sorted_x[int(np.ceil(np_)) - 1]
    return out


def column_quantile_type2(M, prob):
    """R quantile(type=2) of each column of M (rows = bootstrap replicates)."""
    S = np.sort(M, axis=0)
    np_ = M.shape[0] * prob
    if _is_int(np_):
        j = int(round(np_))
        return 0.5 * (S[j - 1] + S[j])
    return S[int(np.ceil(np_)) - 1]


def _finish(x_sorted, y_sorted, qx, qy, alpha, B, n):
    thr = np.maximum(column_quantile_type2(qx, 1 - alpha / 9), column_quantile_type2(qy, 1 - alpha / 9))
    diff = np.abs(deciles_type2(x_sorted) - deciles_type2(y_sorted))
    sig = diff > thr
    return dict(diff=diff, thr=thr, sig=sig, leak=bool(sig.any()), n=n, alpha=alpha, B=B)


# ---- reference-style bootstrap: literal resampling (slow, O(B*n)) ----
def _noise_resample(dat, n, B, rng):
    """B decile-difference vectors between two resamples of the SAME data (behaviour under H0)."""
    res = np.empty((B, 9))
    for b in range(B):
        a = np.sort(rng.choice(dat, n, replace=True))
        c = np.sort(rng.choice(dat, n, replace=True))
        res[b] = np.abs(deciles_type2(a) - deciles_type2(c))
    return res


def rtlf(x, y, alpha=0.09, B=10000, seed=None):
    """RTLF with literal bootstrap resampling. Use for validation; slow for large n."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    n = min(len(x), len(y))  # the artefact wrapper resamples n = min(|x|,|y|) points
    rng = np.random.default_rng(seed)
    qx = _noise_resample(x, n, B, rng); qy = _noise_resample(y, n, B, rng)
    return _finish(np.sort(x), np.sort(y), qx, qy, alpha, B, n)


# ---- fast exact bootstrap (STUDENT OPTIMISATION, not in the authors' tool) ----
# The k-th order statistic of a with-replacement resample of n points from sorted data d is d[floor(m*U)], where
# U ~ Beta(k, n-k+1) (k-th order statistic of n uniforms); the next one is U + (1-U)*Beta(1, n-k).
# Gives exact per-decile marginals in O(B). Deciles within one resample are drawn independently (thresholds use only marginals).
def _decile_draws(sorted_dat, n, B, rng):
    m = len(sorted_dat)

    def pick(u):
        return sorted_dat[np.minimum((u * m).astype(np.int64), m - 1)]

    cols = []
    for p in PROBS:
        np_ = n * p
        if _is_int(np_):
            k = int(round(np_))
            u1 = rng.beta(k, n - k + 1, B)
            u2 = u1 + (1 - u1) * rng.beta(1, n - k, B)
            cols.append(0.5 * (pick(u1) + pick(u2)))
        else:
            k = int(np.ceil(np_))
            cols.append(pick(rng.beta(k, n - k + 1, B)))
    return np.stack(cols, axis=1)


def rtlf_fast(x, y, alpha=0.09, B=10000, seed=None):
    """RTLF with the Beta-order-statistic bootstrap: same decision rule, ~1000x faster at n = 500k."""
    x = np.sort(np.asarray(x, float)); y = np.sort(np.asarray(y, float))
    n = min(len(x), len(y))
    rng = np.random.default_rng(seed)
    qx = np.abs(_decile_draws(x, n, B, rng) - _decile_draws(x, n, B, rng))
    qy = np.abs(_decile_draws(y, n, B, rng) - _decile_draws(y, n, B, rng))
    return _finish(x, y, qx, qy, alpha, B, n)
