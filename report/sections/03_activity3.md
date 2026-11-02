# Activity 3 – Bounded Statistical Side-Channel Artefact Study

## 3.1 Objective and study path
Following the prescribed path (measurement set → statistical analysis → leak/no-leak verdict → interpretation → link to implementation and paper), we applied the authors' RTLF test [1] to author-provided timing data. The planned main study (MatrixSSL 4.6.0 Bleichenbacher pairs B1–B5, α = 0.009, 500 000 measurements per vector; artefact experiment E2) is implemented as a ready pipeline; the baseline evidence below comes from the author-provided datasets that could be obtained in our environment (see 3.6).

## 3.2 Environment and sources
| Item | Value |
|---|---|
| Tool (reference) | RTLF `rtlf.R`, commit 2497d660 (21 Mar 2025), unmodified; R 4.3.3, tidyverse/optparse/jsonlite from Ubuntu 24.04 packages |
| Tool (student) | `src/sca_rtlf/rtlf.py` (numpy 2.4.4, pandas 3.0.2, Python 3.12.3) |
| Hardware | 1 vCPU cloud sandbox (Linux); not comparable to the authors' i7-6700 |
| Data | `examples/example-1.csv`, `example-2.csv` from the RTLF repository (30 000 measurements per class each, units as recorded, apparently clock cycles) |
| Parameters | α = 0.09, B = 10 000 bootstraps, deciles 10–90 %, Bonferroni α/9 per decile |

## 3.3 Procedure
1. Run `rtlf.R` on each file; record per-decile difference, threshold, decision, exit code (11 leak / 10 none).
2. Cross-validate a student numpy re-implementation against the R output (same decile differences required; thresholds may differ by bootstrap noise).
3. Run a calibration where X and Y are identical, to check that the false-positive rate stays below α.
4. Run the MatrixSSL pair pipeline on a simulated fixture with known ground truth to verify the pipeline logic.

## 3.4 Results
**Baseline (author tool, author data, α = 0.09).**

| File | Deciles exceeding threshold (diff vs threshold, cycles) | Decision |
|---|---|---|
| example-1 | 30 % (14 vs 12), 40 % (22 vs 12), 50 % (22 vs 14), 60 % (26 vs 16) | **Leak detected** (exit 11) |
| example-2 | none; closest 40 %/50 % (14 vs 14), 90 % (52 vs 63) | **No leak detected** (exit 10) |

Means for example-1 are 38 535 vs 38 604 (gap ≈ 69 cycles, <0.2 %) with standard deviations ≈ 10 000, yet RTLF flags four adjacent deciles, i.e. a distribution-shape shift in the middle of the distribution is found where the mean gap is small relative to noise.

**Port validation.** Decile differences are identical to R in both files; verdicts agree; thresholds differ by ≤ 2 cycles (e.g. example-1 90 % decile: 56 vs 58). With a deliberately tiny B = 300 the port wrongly flagged example-2: the threshold is a 99 %-quantile of only 300 values (cf. the paper's remark that α must stay well above 1/B).

**Type-1 calibration (simulated identical distributions, 1 000 repetitions per cell).**

| α | n/class | continuous FPR | integer-cycle FPR |
|---|---|---|---|
| 0.09 | 15 000 | 4.9 % | 5.7 % |
| 0.09 | 30 000 | 4.4 % | 4.4 % |
| 0.009 | 15 000 | 0.8 % | 0.2 % |
| 0.009 | 30 000 | 0.4 % | 0.4 % |

All rates are ≤ α, consistent with a *bound* (the rule is conservative). The paper reports 9.2 % for same-xy at n = 15 000 and α = 0.09 (Table 3 of [1]), marginally above α; our simulated data differ from theirs (no `rand()` system-call mixture), so we do not claim to reproduce that cell.

**Pipeline test (simulated MatrixSSL-like fixture, 200 000/class).** Early-exit cost model from Algorithm 3: the pipeline reports leaks for 9/10 pairs, none for B1B3 (identical instructions), and B4B5 is the weakest (7 of 9 deciles) – 10/10 agreement with the code-derived expectation. This validates the pipeline only; it is not a measurement of MatrixSSL.

**Reproduction on the team machine (screenshots in `evidence/activity3/`).** The authors' `rtlf.R` on example-1 was run twice with identical input: both runs flag deciles 30–60 %, decile differences are identical, and thresholds differ by one cycle in two deciles (20 %: 13 vs 14; 90 %: 56 vs 57), i.e. the expected bootstrap run-to-run randomness; runtimes 141.9 s and 140.6 s. Port validation (B = 10 000) reproduced R's decile differences and verdicts on both files. A 200-repetition calibration gave 7 of 8 cells at or below alpha; the exception (alpha = 0.009, n = 30 000, continuous: 2/200 = 1.0 %) has Wilson interval [0.3 %, 3.6 %] containing alpha, and the 1000-rep sandbox run gave 0.4 % for that cell. **An R run on example-2 on the team machine is still pending** (the second team R run used example-1 again).

## 3.5 Interpretation
* A verdict is meaningful only with α, n, B and the exact pair tested: example-1's leak is flagged at α = 0.09, so a false alarm of up to 9 % is by design; example-2's "no leak" means "no difference detectable at this n and noise", not constant time (paper §5.2).
* The threshold column is the noise estimate: thresholds of 12–63 cycles show what difference this data set can resolve; the exceedance (diff − threshold) is the graded evidence.
* Relation to the implementation: for the MatrixSSL study the code predicts leaks for all pairs except B1B3 (Algorithm 3: exits at lines 3, 14, 21). The paper's RTLF verdict differs (it flags B1B3 and misses B1B2, B1B5, B2B5, B3B4), which is the interpretation exercise for the real run: discuss Type-1 error (B1B3), Type-2/noise masking (the misses), and that α = 0.009 trades power for fewer false alarms.

## 3.6 Limitations and deviations
* **The planned MatrixSSL dataset was not analysed**: the development environment could not reach Zenodo. The pipeline (`scripts/run_activity3.py`) is complete but its file matching is untested on the real archive. *Replace this section with real results once step 3 of the README is run; do not report the simulated table as MatrixSSL.*
* Example-1/2 are generic RTLF demo files; the repository does not say how they were generated, so we make no claim about a specific implementation.
* **Bug found by team testing, fixed:** passing a placeholder path to `scripts/run_activity3.py` crashed with an `AttributeError`; the script now validates the path and prints a diagnostic. The calibration pass/fail check now uses a Wilson interval instead of the observed rate.
* The fast bootstrap draws each decile's resample statistic independently (exact marginals); thresholds depend only on marginals, which we confirmed empirically against R, but it is not byte-identical to the authors' algorithm.
* Runtimes (R ≈ 150 s per 30 000/class pair on 1 vCPU) are not comparable to the authors' multi-core setup.
