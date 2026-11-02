PY ?= python3
DATA ?=
.PHONY: setup rtlf-clone test validate calibrate-demo activity3-sim activity3 activity3-r

setup:            ## python deps (R is installed separately, see docs/SETUP.md)
	$(PY) -m pip install -r requirements.txt
rtlf-clone:       ## authors' reference tool (author-provided, never edited)
	git clone https://github.com/tls-attacker/RTLF.git third_party/RTLF
test:
	$(PY) -m pytest -q
validate:         ## student port vs authors' R output on RTLF's example files
	$(PY) scripts/validate_port.py third_party/RTLF/examples 10000
calibrate-demo:   ## Type-1 calibration, 200 repetitions (~2 min)
	$(PY) scripts/calibrate_type1.py 200 results/activity3
activity3-sim:    ## pipeline smoke test on SIMULATED data (not evidence about MatrixSSL)
	$(PY) scripts/make_sim_fixture.py /tmp/sim_fixture 200000 7
	$(PY) scripts/run_activity3.py --data /tmp/sim_fixture --out /tmp/sim_out --tag sim
activity3:        ## real study: make activity3 DATA=data/<MatrixSSL Bleichenbacher folder>
	$(PY) scripts/run_activity3.py --data "$(DATA)" --alpha 0.009 --tag baseline
activity3-r:      ## same with the authors' R tool as backend (slow)
	$(PY) scripts/run_activity3.py --data "$(DATA)" --alpha 0.009 --tag baseline_R --backend r
