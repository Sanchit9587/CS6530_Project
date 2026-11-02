import os, sys
import numpy as np
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from sca_rtlf import rtlf, rtlf_fast, deciles_type2, wilson
from sca_rtlf.data import FILENAME_MAP, pair_label
from sca_rtlf.expectations import PAIRS, CODE_EXPECT, PAPER_RTLF


def test_deciles_match_r_type2_convention():
    assert deciles_type2(np.arange(1, 11.0)).tolist() == [1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5]  # n*p integer -> average
    d = deciles_type2(np.arange(1, 16.0))                                                             # n=15: n*p=1.5 -> ceil -> x[2]
    assert d[0] == 2.0 and d[4] == 8.0


def test_wilson_is_sane_at_zero_and_contains_estimate():
    lo, hi = wilson(0, 200)
    assert lo == 0.0 and 0 < hi < 0.03
    lo, hi = wilson(2, 200)
    assert lo < 0.01 < hi


def test_detects_clear_shift_and_not_identical():
    rng = np.random.default_rng(0)
    x = rng.lognormal(10, .1, 5000)
    assert rtlf_fast(x, x * 1.02 + rng.normal(0, 1, 5000), 0.09, 2000, seed=1)["leak"]       # 2% shift
    y = rng.lognormal(10, .1, 5000)
    fp = sum(rtlf_fast(rng.lognormal(10, .1, 3000), rng.lognormal(10, .1, 3000), 0.09, 1000, seed=i)["leak"] for i in range(60))
    assert fp / 60 <= 0.2          # alpha = 0.09; generous slack for 60 repetitions


def test_fast_and_literal_bootstrap_agree():
    rng = np.random.default_rng(1)
    x = rng.lognormal(10, .15, 2000); y = rng.lognormal(10, .15, 2000)
    a = rtlf(x, y, 0.09, 1500, seed=3); b = rtlf_fast(x, y, 0.09, 1500, seed=3)
    assert np.allclose(a["diff"], b["diff"])                      # observed statistic is deterministic
    assert np.allclose(a["thr"], b["thr"], rtol=0.25, atol=0.02 * a["thr"].max())   # thresholds agree up to bootstrap noise


@pytest.mark.skipif(not os.path.exists("third_party/RTLF/examples/example-1.csv"), reason="RTLF repo not cloned")
def test_matches_authors_r_output_on_example_1():
    import pandas as pd
    df = pd.read_csv("third_party/RTLF/examples/example-1.csv")
    r = rtlf_fast(df.loc[df.V1 == "X", "V2"].values, df.loc[df.V1 == "Y", "V2"].values, 0.09, 10000, seed=1)
    assert r["diff"].astype(int).tolist() == [14, 12, 14, 22, 22, 26, 24, 12, 14] and r["leak"]


def test_filename_map_is_complete_and_unique():
    assert sorted(FILENAME_MAP.values()) == sorted(PAIRS) and len(set(FILENAME_MAP)) == 10
    assert pair_label("No_0x00_in_messagevsInvalid_TLS_version_in_PMS_foo.csv") == "B3B5"
    assert pair_label("unrelated.csv") is None


def test_expectations_cover_all_pairs():
    assert set(CODE_EXPECT) == set(PAPER_RTLF) == set(PAIRS)
    assert not CODE_EXPECT["B1B3"] and PAPER_RTLF["B1B3"]       # the paper's one 'unexpected' finding
