# Activity 3 – baseline study

**Question:** Does RTLF find the timing leak in MatrixSSL 4.6.0's Bleichenbacher handling, and do verdicts match the source code and the paper?
**Data:** authors' `d_measurements_qualitative.zip` (Zenodo 10817685), pairs B1B2…B4B5, 500 000 per vector.
**Fixed parameters:** alpha = 0.009, B = 10 000, seed = 1, backend = `fast` (cross-check with `--backend r`).
**Expected (paper, Sec. 7.1):** leak for B1B3, B1B4, B2B3, B2B4, B3B5, B4B5; none for B1B2, B1B5, B2B5, B3B4. Code (Algorithm 3) predicts every pair differs except B1B3.

**Commands:** see `docs/SETUP.md`, sections B–E.
**Outputs:** `results/activity3/results_baseline.csv`, `run_info_baseline.json`; evidence screenshots in `evidence/activity3/`.
**Earlier files:** logs in `results/activity3/` were produced before the repo restructure under older script names:
`rtlf_py.py`→`src/sca_rtlf/rtlf.py`, `run_matrixssl_study.py`→`scripts/run_activity3.py`, `validate_*.py`→`scripts/validate_port.py`, `type1_calibration.py`→`scripts/calibrate_type1.py`.
