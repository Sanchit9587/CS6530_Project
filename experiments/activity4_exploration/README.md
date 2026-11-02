# Activity 4 – small engineering exploration (TO DO)

Change ONE controlled parameter of the Activity 3 analysis, state the hypothesis first, repeat, and explain how confidence in the leak conclusion changes.
**Planned (Phase 1 report, Sec. 5.3):** sample size 30k / 100k / 200k / 500k via `--n`, alpha fixed at 0.009, same seed, random subsample.
**Hypothesis:** large-difference pairs (B2 vs B1/B3) stay detected at all sizes; the smallest expected difference (B4B5) appears only at larger n. Optional: alpha = 0.09 on full data.
**How:** `for n in 30000 100000 200000 0; do python3 scripts/run_activity3.py --data data/<folder> --n $n --tag n$n --out results/activity4; done`, then compare detection per pair vs n (plot to `report/figures/`). Implement `scripts/run_activity4.py` as a loop over the same engine. Keep repetitions with several seeds so the trend is not a single bootstrap draw.
