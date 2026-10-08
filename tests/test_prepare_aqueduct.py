import importlib.util
from pathlib import Path

import pandas as pd
import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "prepare_aqueduct.py"


def _load():
    spec = importlib.util.spec_from_file_location("prepare_aqueduct", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _write_package(d: Path):
    future = pd.DataFrame({"fid": [1, 2, 3, 4], "pfaf_id": [610001, 610002, 410001, 150001], "bau50_ws_x_r": [0.1, 0.2, 0.3, 0.5]})
    future.to_csv(d / "Aqueduct40_future_annual_y2023m07d05.csv", index=False)
    base = pd.DataFrame({
        "string_id": ["610001-BRA.1_1-1", "610002-BRA.1_1-2", "410001-IND.1_1-3", "150001-PRT.1_1-4", "999999-USA.1_1-5"],
        "pfaf_id": [610001, 610002, 410001, 150001, 999999],
        "gid_1": ["BRA.1_1", "BRA.1_1", "IND.1_1", "PRT.1_1", "USA.1_1"],
        "aqid": [1, 2, 3, 4, 5],
        "gid_0": ["BRA", "BRA", "IND", "PRT", "USA"],
        "name_0": ["Brazil", "Brazil", "India", "Portugal", "United States"],
        "name_1": ["a", "a", "b", "c", "d"],
        "area_km2": [10.0, 20.0, 30.0, 40.0, 50.0],
        "bws_raw": [0.1, 0.2, 0.3, 0.4, 0.5], "bws_score": [1.0, 2.0, 3.0, 4.0, 5.0], "bws_cat": [1, 2, 3, 4, 5], "bws_label": ["l", "m", "h", "x", "y"],
    })
    base.to_csv(d / "Aqueduct40_baseline_annual_y2023m07d05.csv", index=False)


def test_country_files_and_baseline(tmp_path, monkeypatch):
    mod = _load()
    _write_package(tmp_path)
    monkeypatch.setattr(mod, "load_paths", lambda: {"aqueduct_dir": str(tmp_path)})
    mod.main()
    bra = pd.read_csv(tmp_path / "Brazil" / "aqueduct_2050.csv")
    assert sorted(bra["pfaf_id"]) == [610001, 610002]
    assert "fid" not in bra.columns
    assert sorted(pd.read_csv(tmp_path / "India" / "aqueduct_2050.csv")["pfaf_id"]) == [410001]
    assert list(pd.read_csv(tmp_path / "Portugal" / "aqueduct_2050.csv")["pfaf_id"]) == [150001]
    three = pd.read_csv(tmp_path / "baseline_annual" / "aqueduct_baseline_annual_3countries.csv")
    assert set(three["country"]) == {"BRA", "IND", "PRT"} and len(three) == 4


def test_existing_equal_output_is_kept_and_different_aborts(tmp_path, monkeypatch):
    mod = _load()
    _write_package(tmp_path)
    monkeypatch.setattr(mod, "load_paths", lambda: {"aqueduct_dir": str(tmp_path)})
    mod.main()
    mod.main()  # second run: equal content, nothing written, no error
    pd.DataFrame({"pfaf_id": [1], "bau50_ws_x_r": [9.0]}).to_csv(tmp_path / "Brazil" / "aqueduct_2050.csv", index=False)
    with pytest.raises(SystemExit):
        mod.main()
