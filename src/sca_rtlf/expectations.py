"""Reference verdicts for the Bleichenbacher pairs (MatrixSSL 4.6.0)."""
PAIRS = ["B1B2", "B1B3", "B1B4", "B1B5", "B2B3", "B2B4", "B2B5", "B3B4", "B3B5", "B4B5"]
# (i) from Algorithm 3 of the paper: B2 exits at line 3; B4,B5 at line 14 (B4/B5 differ only in loop count); B1,B3 at line 21.
CODE_EXPECT = {p: (p != "B1B3") for p in PAIRS}
# (ii) published RTLF verdicts, alpha = 0.009, 500k measurements (paper Sec. 7.1; artefact E2a README)
PAPER_RTLF = {p: (p in {"B1B3", "B1B4", "B2B3", "B2B4", "B3B5", "B4B5"}) for p in PAIRS}
