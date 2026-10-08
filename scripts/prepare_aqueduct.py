"""Prepare the Aqueduct 4.0 inputs of `09_consolidate.py` from the official WRI package.

Reads `Aqueduct40_future_annual_*.csv` and `Aqueduct40_baseline_annual_*.csv` from `aqueduct_dir` (extracted from
`aqueduct-4-0-water-risk-data.zip` when the CSV files are absent) and writes:

- `<aqueduct_dir>/<Country>/aqueduct_2050.csv` for each study country: the rows of `future_annual` whose `pfaf_id`
  appears in `baseline_annual` for that country (`gid_0`), without the `fid` column;
- `<aqueduct_dir>/baseline_annual/aqueduct_baseline_annual_3countries.csv`: the rows of `baseline_annual` of the three
  study countries, with `gid_0` renamed to `country`.

An existing output is kept when its content is equal (numbers to 1e-12 relative); a different content stops the script (nothing is overwritten).

Usage: python scripts/prepare_aqueduct.py
"""

import sys
import zipfile
from pathlib import Path

import pandas as pd

from creei.config import load_paths
from creei.inventory.plants import COUNTRY_NAMES

ZIP_NAME = "aqueduct-4-0-water-risk-data.zip"
FUTURE_PREFIX, BASELINE_PREFIX = "Aqueduct40_future_annual_", "Aqueduct40_baseline_annual_"
BASELINE_COLS = ["string_id", "pfaf_id", "gid_1", "aqid", "gid_0", "name_1", "area_km2", "bws_raw", "bws_score", "bws_cat", "bws_label"]
OUT_BASELINE_COLS = ["string_id", "pfaf_id", "gid_1", "aqid", "country", "name_1", "area_km2", "bws_raw", "bws_score", "bws_cat", "bws_label"]


def find_or_extract(aqueduct_dir: Path, prefix: str) -> Path:
    """Return `<prefix>*.csv` of `aqueduct_dir`, extracting it from the WRI zip file when absent."""
    hits = sorted(aqueduct_dir.glob(f"{prefix}*.csv"))
    if hits:
        return hits[-1]
    zip_path = aqueduct_dir / ZIP_NAME
    if not zip_path.exists():
        sys.exit(f"ABORT: no {prefix}*.csv and no {ZIP_NAME} in {aqueduct_dir}; download the Aqueduct 4.0 package from WRI")
    with zipfile.ZipFile(zip_path) as z:
        members = [m for m in z.namelist() if Path(m).name.startswith(prefix) and m.endswith(".csv")]
        if len(members) != 1:
            sys.exit(f"ABORT: expected one {prefix}*.csv in {ZIP_NAME}, found {members}")
        target = aqueduct_dir / Path(members[0]).name
        target.write_bytes(z.read(members[0]))
    return target


def write_if_new(df: pd.DataFrame, path: Path, sort_cols: list[str]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        old = pd.read_csv(path)
        try:
            pd.testing.assert_frame_equal(
                old.sort_values(sort_cols).reset_index(drop=True), df.sort_values(sort_cols).reset_index(drop=True), check_exact=False, rtol=1e-12)
        except AssertionError:
            sys.exit(f"ABORT: {path} exists with different content; nothing overwritten")
        return "kept"
    df.to_csv(path, index=False)
    return "written"


def main() -> None:
    aqueduct_dir = Path(load_paths()["aqueduct_dir"])
    future = pd.read_csv(find_or_extract(aqueduct_dir, FUTURE_PREFIX)).drop(columns=["fid"])
    baseline = pd.read_csv(find_or_extract(aqueduct_dir, BASELINE_PREFIX), usecols=BASELINE_COLS)
    for iso, name in COUNTRY_NAMES.items():
        pfaf = set(baseline.loc[baseline["gid_0"] == iso, "pfaf_id"])
        rows = future[future["pfaf_id"].isin(pfaf)].reset_index(drop=True)
        status = write_if_new(rows, aqueduct_dir / name / "aqueduct_2050.csv", ["pfaf_id"])
        print(f"{iso}: {len(rows)} basins of {len(pfaf)} in baseline_annual -> {name}/aqueduct_2050.csv ({status})")
    three = baseline[baseline["gid_0"].isin(COUNTRY_NAMES)].rename(columns={"gid_0": "country"})[OUT_BASELINE_COLS].reset_index(drop=True)
    status = write_if_new(three, aqueduct_dir / "baseline_annual" / "aqueduct_baseline_annual_3countries.csv", ["string_id"])
    print(f"baseline_annual: {len(three)} rows -> baseline_annual/aqueduct_baseline_annual_3countries.csv ({status})")


if __name__ == "__main__":
    main()
