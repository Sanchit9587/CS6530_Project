#!/bin/bash
# Run this on a machine with internet access to Zenodo (the sandbox used for development had none).
# Author-provided data: Zenodo record 10817685 (DOI 10.5281/zenodo.10817685), file d_measurements_qualitative.zip (~809 MB).
set -e
mkdir -p data && cd data
wget -nc https://zenodo.org/records/10817685/files/d_measurements_qualitative.zip
sha256sum d_measurements_qualitative.zip | tee ../results/activity3/dataset_sha256.txt
unzip -n d_measurements_qualitative.zip
echo "Locate the MatrixSSL-4.6.0 Bleichenbacher folder and pass it to run_activity3.py --data"
find . -ipath '*matrixssl*' -ipath '*bleichenbacher*' -name '*.csv' | head -20
