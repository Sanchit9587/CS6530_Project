"""Loading the authors' per-pair measurement CSVs (columns V1 = BASELINE|MODIFIED or X|Y, V2 = timing)."""
import glob, os
import numpy as np, pandas as pd

# filename prefix (from the authors' tools/reporter/collectResults.py) -> pair label
FILENAME_MAP = {
    "Wrong_second_byte_(0x02_set_to_0x17)vsCorrectly_formatted_PKCS#1_PMS_message": "B1B2",
    "Invalid_TLS_version_in_PMSvsCorrectly_formatted_PKCS#1_PMS_message": "B1B3",
    "0x00_on_the_next_to_last_position_(|PMS|_=_1)vsCorrectly_formatted_PKCS#1_PMS_message": "B1B4",
    "No_0x00_in_messagevsCorrectly_formatted_PKCS#1_PMS_message": "B1B5",
    "Wrong_second_byte_(0x02_set_to_0x17)vsInvalid_TLS_version_in_PMS": "B2B3",
    "0x00_on_the_next_to_last_position_(|PMS|_=_1)vsWrong_second_byte_(0x02_set_to_0x17)": "B2B4",
    "No_0x00_in_messagevsWrong_second_byte_(0x02_set_to_0x17)": "B2B5",
    "0x00_on_the_next_to_last_position_(|PMS|_=_1)vsInvalid_TLS_version_in_PMS": "B3B4",
    "No_0x00_in_messagevsInvalid_TLS_version_in_PMS": "B3B5",
    "No_0x00_in_messagevs0x00_on_the_next_to_last_position_(|PMS|_=_1)": "B4B5",
}


def pair_label(fname):
    for prefix, lab in FILENAME_MAP.items():
        if fname.startswith(prefix):
            return lab
    return None


def list_csvs(data_dir):
    return glob.glob(os.path.join(data_dir, "**", "*.csv"), recursive=True)


def find_pair_files(data_dir):
    """Return ({pair label: path}, all csv paths found)."""
    allc = list_csvs(data_dir)
    files = {}
    for p in allc:
        lab = pair_label(os.path.basename(p))
        if lab and lab not in files:
            files[lab] = p
    return files, allc


def split_classes(df):
    v1 = df["V1"].astype(str)
    return (df.loc[v1.isin(["BASELINE", "X"]), "V2"].to_numpy(float),
            df.loc[v1.isin(["MODIFIED", "Y"]), "V2"].to_numpy(float))


def load_pair(path, n_max=0, seed=1):
    """Load one pair file. n_max > 0 takes a RANDOM subsample per class (a head-slice could carry drift/ordering bias)."""
    x, y = split_classes(pd.read_csv(path))
    if n_max and n_max < min(len(x), len(y)):
        r = np.random.default_rng(seed)
        x = r.choice(x, n_max, replace=False); y = r.choice(y, n_max, replace=False)
    return x, y
