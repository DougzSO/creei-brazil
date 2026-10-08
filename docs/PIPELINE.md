# Pipeline

`python main.py <COUNTRY>` runs the phases of `config/pipeline.yaml` in order and skips the ones that are already
complete.

## Running

```text
python main.py BRA                      # every phase except the long ones; completed phases are skipped
python main.py Brazil --dry-run         # print the plan, run nothing
python main.py BRA --only w3,w4         # only these phases (long phases included) plus the headline check
python main.py BRA --force coexposure   # re-run a phase although its hash is unchanged
python main.py BRA --adopt              # record the hashes of outputs that already exist (first use on an existing tree)
python main.py BRA --list               # phases
```

- `BRA` and `Brazil` are accepted. `PRT` and `IND` stop at once with `ERRO: país não implementado: PRT` (exit 2)
  before any phase runs; nothing is executed partially.
- A complete phase prints `[SKIP] <phase>: saídas presentes, hash igual`. The long phases (`acquire`, `indices`,
  `hydro`) never run unless named with `--only` or `--force`; the default run only reports whether they are current.
- `headlines` (`scripts/check_headlines.py`) is always the last phase and is never skipped; a failure stops the run
  with exit 1.
- State is kept in `<interim_dir>/pipeline_state_<ISO>.json` (hash of each completed phase and a cache of file hashes
  by size and modification time). It is not part of the repository.
- Scripts run alone write the article files to `<outputs_dir>/article/_preview`; only
  `scripts/article/build_all.py --promote` (the `article` phase) writes the official folders.

## Completion criterion

A phase is complete when all its declared outputs exist and the recorded hash equals the current one. The hash covers
the declared inputs, the phase's scripts (and `watch` files), `config/countries/<ISO>.yaml`, `config/params.yaml` and
`config/pipeline.yaml`. A downstream phase sees an upstream re-run through the hash of its outputs
(`phase:<name>` inputs), so it re-runs only if those outputs changed. Input tokens:

| Token | Meaning |
|---|---|
| `processed:` `tables:` `geo:` `article:` | file under that root |
| `raw:GLOB` | raw files, hashed directly |
| `rawcov:GLOB` | raw files that must be in `raw/manifest.json`; the manifest sha256 is the hash and the files are not read again. A file outside the manifest raises an error |
| `phase:NAME` | all declared outputs of an earlier phase |

The long phases `indices` and `hydro` use `rawcov:` for the ISIMIP3b `tasmax`, `tasmin` and `pr` files. The 36 W5E5
`.nc` files read by `w5e5` are not in the manifest (it registers the downloaded zip files), so that phase hashes them
directly (2.5 GB, cached by size and time).

## Phases

| # | Phase | Scripts | Long |
|---|---|---|---|
| 0 | acquire | `02_acquire`, `04_full_acquire` | yes |
| 1 | geo | `geo_base` | |
| 2 | inventory | `05_plants`, `05b_plant_units` | |
| 3 | spatial | `06_spatial` | |
| 4 | indices | `04_daily_indices` | yes |
| 5 | hydro | `07_water_balance`, `08_spei` | yes |
| 6 | hazards | `prepare_aqueduct`, `09_consolidate` | |
| 7 | w5e5 | `24_w5e5_spei_validation`, `e1_w5e5_inputs` | |
| 8 | w3 | `w3_heat_fuel` ... `w3_curves`, `th1_fleet_gw`, `w3g_heat_levels` | |
| 9 | w4 | `w4_null` ... `w4f_threshold_grid`, `w4r_emulator_check`, `w4g_drought_levels`, `w4h_coexposure` | |
| 10 | coexposure | `w3h_state_coexposure`, `w5_table3_gcm_mean`, `w5_sensitivity` | |
| 11 | e1 | `e1_hedge`, `e1_colocation` | |
| 12 | e3 | `e3_ena_validation`, `e3_hit_rate` | |
| 13 | w6 | `w6_gcm_subset`, `w6_nonmonotonicity` | |
| 14 | validation (supplementary) | `25_validation_stats` | |
| 15 | article | `article/build_all.py --promote` | |
| 16 | headlines | `check_headlines` | always |

## Country interface

`config/countries/<ISO>.yaml` holds, for each country, its ISO code and aliases, the geometry files and layer names,
the Itaipu special case, the filters, the macro-region map and the submarket approximation. `BRA` is implemented;
`PRT` and `IND` carry `implemented: false`. `creei.countries.iso()` returns the country of the run (environment
variable `CREEI_COUNTRY`, set by `main.py`; `BRA` when a script runs alone), and the country filters of the
production scripts read it. The `country="BRA"` defaults in `src/creei/` and the Portugal/Brazil lists of
`24_w5e5_spei_validation.py` are left as they are.
