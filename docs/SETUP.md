# Setup and execution flow

## A. Prerequisites
1. **Python ≥ 3.10:** `python3 -m venv venv && source venv/bin/activate && make setup`
2. **R ≥ 4.3** (needed for the authors' reference tool; the Python backend runs without it).
   * Ubuntu/WSL: `sudo apt-get update && sudo apt-get install -y software-properties-common && sudo add-apt-repository universe && sudo apt-get update && sudo apt-get install -y r-base r-base-dev r-cran-tidyverse r-cran-optparse r-cran-jsonlite r-cran-crayon`
   * If apt reports `r-cran-ragg` not installable: install `build-essential libcurl4-openssl-dev libssl-dev libxml2-dev libfontconfig1-dev libharfbuzz-dev libfribidi-dev libfreetype6-dev libpng-dev libtiff-dev libjpeg-dev libwebp-dev`, then `sudo Rscript -e 'install.packages(c("tidyverse","optparse","jsonlite","crayon"), repos="https://cloud.r-project.org")'` (10–25 min), or use conda: `conda create -n rtlf -c conda-forge r-base r-tidyverse r-optparse r-jsonlite r-crayon`.
   * macOS: `brew install r`. Windows: installer from cran.r-project.org and add `R\bin` to PATH.
   * Check: `Rscript -e 'library(tidyverse); library(optparse); library(jsonlite); library(crayon); cat("OK\n")'`
3. **Authors' tool:** `make rtlf-clone` → `third_party/RTLF/` (never edit it). Record its commit: `git -C third_party/RTLF log -1`, and `Rscript --version`.

## B. Baseline with the authors' tool (~2.5 min per run)
```bash
cd third_party/RTLF
Rscript rtlf.R -i examples/example-1.csv -a 0.09 -o out1.json    # expect: significant difference (exit 11)
Rscript rtlf.R -i examples/example-2.csv -a 0.09 -o out2.json    # expect: no significant difference (exit 10)
cd ../..
```
Screenshot both into `evidence/activity3/`. (Note: `-i` must be `example-2.csv` for the second run.)

## C. Validate the student port (~1 min)
`make validate` – decile differences must equal R's; verdicts must agree; thresholds agree to a few cycles.

## D. Real study (needs internet to Zenodo)
```bash
bash scripts/fetch_dataset.sh                                  # downloads ~809 MB, prints folders
python3 scripts/run_activity3.py --data data/<folder> --alpha 0.009 --tag baseline
```
Check `found 10/10 pair files` first. If not, the script prints sample file names; adapt `FILENAME_MAP` in `src/sca_rtlf/data.py`.
Optional reference check: add `--backend r` (slow at 500k per class; `--n 100000` to subsample).

## E. Negative test and pipeline test
`make calibrate-demo` (200 reps) or `python3 scripts/calibrate_type1.py 1000 results/activity3` (~8 min); `make activity3-sim`.

## F. Troubleshooting
| Symptom | Fix |
|---|---|
| `Rscript: command not found` | install R / add to PATH |
| `no package called tidyverse` | redo step A2 |
| `ERROR: --data was given the placeholder text` | pass a real folder path |
| `found 0/10 pair files` | wrong folder or archive layout differs; see sample names printed |
