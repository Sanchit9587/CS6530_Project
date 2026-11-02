# Provenance: author-provided → student modifications → student-created

| Item | Category |
|---|---|
| `third_party/RTLF/` (`rtlf.R`, `examples/*.csv`) – clone of github.com/tls-attacker/RTLF | Author-provided, not modified (git-ignored; re-clone with `make rtlf-clone`) |
| Artefact repo RUB-NDS/Artifacts-With-Great-Power-Come-Great-Side-Channels and Zenodo 10817685 dataset | Author-provided; only read. The filename→pair map was re-typed as `FILENAME_MAP` in `src/sca_rtlf/data.py` |
| `src/sca_rtlf/rtlf.py` – `rtlf()` literal bootstrap | Student re-implementation of the authors' Algorithms 1–2 |
| `src/sca_rtlf/rtlf.py` – `rtlf_fast()` Beta-order-statistic bootstrap | Student modification (optimisation), validated against the authors' R tool |
| `src/sca_rtlf/{data,backends,reporting,expectations,stats}.py`, all `scripts/*`, `tests/*`, `Makefile` | Student-created |
| Simulated fixture (`make_sim_fixture.py`) and calibration data | Student-generated; **not** measurements of any real library |
| Screenshots in `evidence/` | Produced by the team on its own machine |
