# CS6530 Theme 13 – Statistical timing side-channel detection (RTLF)

Phase 2 / final submission repository. Primary paper: Dunsche et al., *With Great Power Come Great Side Channels* (USENIX Security 2024).
Team: Aayush Lal (CE24B033), Sanchit Lodha (CE24B107), Sanika Nair (CE24B108).

## Design rule: library vs. experiments
* `src/sca_rtlf/` – **reusable library** (the statistical test, data loading, reference verdicts, reporting). No file paths, no printing, no experiment logic. Tested.
* `scripts/` – **thin command-line entry points**, one per experiment. They only parse arguments, call the library, and write to `results/`.
* `experiments/<activity>/` – the *design* of each experiment (question, hypothesis, parameters, exact commands). No code.
* `results/<activity>/` – machine-generated outputs. `evidence/<activity>/` – screenshots and logs cited in the report.
* Activity 4 reuses the Activity 3 engine and changes one parameter; Activities 5–6 are analysis documents built on the results.

## Where each activity lives
| Activity | Code | Design / docs | Results & evidence | Report section |
|---|---|---|---|---|
| 3 Bounded artefact study | `scripts/run_activity3.py`, `validate_port.py`, `calibrate_type1.py`, `make_sim_fixture.py`, `fetch_dataset.sh`; library `src/sca_rtlf/` | `experiments/activity3_baseline/` | `results/activity3/`, `evidence/activity3/` | `report/sections/03_activity3.md`, `report/Activity3_Report.pdf` |
| 4 Engineering exploration | `scripts/run_activity4.py` (**stub**, reuses the library) | `experiments/activity4_exploration/` | `results/activity4/`, `evidence/activity4/` | `report/sections/04_activity4.md` (to write) |
| 5 Security Evolution Matrix | – | `analysis/activity5/security_evolution_matrix.md` (template) | – | `report/sections/05_activity5.md` (to write) |
| 6 Engineering lessons | – | `analysis/activity6/engineering_lessons.md` (template) | – | `report/sections/06_activity6.md` (to write) |
| Activities 1–2 (context) | – | carry over the Phase 1 report text | – | `report/sections/01_02_context.md` (to write) |
| Submission artefacts | – | `slides/` (≤4 content slides), `video/` (5–8 min) | – | – |

## Quick start
```bash
python3 -m venv venv && source venv/bin/activate
make setup            # python deps
make rtlf-clone       # authors' R tool into third_party/ (needs R, see docs/SETUP.md)
make test             # 7 unit tests (one compares against the authors' R output)
make validate         # student port vs authors' R tool
make activity3-sim    # pipeline smoke test on SIMULATED data
make activity3 DATA=data/<MatrixSSL Bleichenbacher folder>   # the real study (after scripts/fetch_dataset.sh)
```
Full step-by-step flow including R installation: `docs/SETUP.md`. Provenance (author-provided vs student-written): `docs/PROVENANCE.md`.

## Status
Done: Activity 3 baseline on author example data, port validation, Type-1 calibration (simulated), team-machine reproduction.
**Not yet done:** real MatrixSSL B1–B5 run (needs Zenodo), R run on `example-2` on the team machine, Activities 4–6, video, slides.
