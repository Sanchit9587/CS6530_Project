# Results produced on the team machine (transcribed from screenshots in `evidence/activity3/`)

Machine: Linux laptop (shell prompt `sanchit@sanchit-Inspiron-15-3511`), Python 3.12 in a venv, authors' `rtlf.R` from the cloned RTLF repository.
R version and exact RTLF commit were not captured in the screenshots; record them (`Rscript --version`, `git -C RTLF log -1`) before submission.

| # | Command | Result | Screenshot |
|---|---|---|---|
| 1 | `Rscript rtlf.R -i examples/example-1.csv -a 0.09 -o out1.json` | Leak detected; deciles 30,40,50,60% flagged; thresholds 22,13,12,12,14,16,26,26,56; 141.88 s | 01 |
| 2 | `Rscript rtlf.R -i examples/example-1.csv -a 0.09 -o out2.json` (**same input file as #1 - this is a repeat, not example-2**) | Leak detected; same four deciles; thresholds 22,14,12,12,14,16,26,26,57; 140.55 s | 02 |
| 3 | `python3 scripts/validate_py_vs_r.py RTLF/examples 10000` | Decile differences identical to R in both files; verdicts agree (True/True, False/False); 17 s and 20 s | 03 |
| 4 | `python3 scripts/validate_fast.py RTLF/examples` | Fast bootstrap 0.05 s per file; thresholds within 2 cycles of R; verdicts agree | 04 |
| 5 | `python3 scripts/run_matrixssl_study.py --data "<that folder>" ...` | **Error, user mistake plus code bug**: the literal placeholder was passed as the folder, 0 files matched, and the script crashed with `AttributeError: 'DataFrame' object has no attribute 'leak'`. Fixed (see README, "Fixes after team testing"). Real MatrixSSL data NOT yet analysed. | 05 |
| 6 | `python3 scripts/type1_calibration.py 200` | 8 cells; 7 of 8 had observed FPR <= alpha; alpha=0.009, n=30000, continuous had 2/200 = 1.0% (flagged `NO` by the old naive check) | 06 |

## Observations
* Runs 1 and 2 used identical data and parameters: the decile differences are identical (14,12,14,22,22,26,24,12,14) and the verdict is the same, while the thresholds differ by 1 cycle in two deciles (20%: 13 vs 14; 90%: 56 vs 57). This is the bootstrap's expected run-to-run randomness, and it matches the sandbox run (thresholds ...,26,26,58).
* **Still missing from the team machine:** an R run on `examples/example-2.csv` (the no-leak case). The report's example-2 row currently comes from the development-sandbox run; replace it with a team-machine run (`Rscript rtlf.R -i examples/example-2.csv -a 0.09 -o out2.json`).
* The `NO` in run 6 is not evidence that RTLF breaks its bound: 2 false positives in 200 repetitions has a 95% Wilson interval of [0.27%, 3.57%], which contains alpha = 0.9%, and the 1000-repetition run in the sandbox gave 0.4% for the same cell. The pass/fail check in `type1_calibration.py` was changed to compare alpha with the interval, not the point estimate.
