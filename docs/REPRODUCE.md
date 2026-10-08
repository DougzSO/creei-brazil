# Reproduce the results

## Requirements

- Python 3.11 and the packages of `requirements.txt` (or `environment.yml`), pinned to the versions used for the article.
- A machine with 6 GB of RAM is enough: large tables are read with selective column and row filters. The pipeline was
  run on Windows 10 with 6.2 GB of RAM.
- Disk space (measured on the author's run):

| Folder | Content | Size |
|---|---|---|
| `raw_dir` | ISIMIP3b files cropped to Brazil, India and Portugal | 16 GB |
| | W5E5 v2.0 cutouts | 2.5 GB |
| | Aqueduct 4.0 package and derived files | 1.0 GB |
| | GADM, boundaries, HydroBASINS, GEM, ONS | about 0.6 GB |
| `isimip_global_cache_dir` | Global ISIMIP3b files kept for reuse (optional, only if you keep the cache) | 353 GB in the author's cache |
| `processed_dir` | Parquet files | 1.3 GB |
| `outputs_dir` | Result tables, figures | 0.1 GB |

The 353 GB cache is a convenience: the acquisition step crops each global file to the three study countries and
does not need the cache again afterwards.

## Time

Wall-clock times on the author's machine (Windows 10, 6.2 GB RAM, no GPU), one phase at a time with
`python main.py BRA --force <phase>`; each time includes the headline check that closes the run.

| Phase | Time |
|---|---|
| `geo` | 2 s |
| `inventory` | 3 min |
| `spatial` | 5 min |
| `hazards` | 2 min |
| `w5e5` | 9 min |
| `w3` | 1 min |
| `w4` | 5 min |
| `coexposure` | 13 s |
| `e1` | 3 min |
| `e3` | 1 min |
| `w6` | 28 s |
| `validation` | 21 s |
| `article` | 34 s |
| All the phases above | about 30 min |
| `indices` (long) | 72 min, measured once on the full 60-job run; not repeated for this document |
| `hydro` (long) | not measured |
| `acquire` (long) | not measured: days, set by the ISIMIP queue and the network |

## 1. Configure

```bash
cp config/paths.example.yaml config/paths.local.yaml   # edit every path
python -m pytest -q
```

## 2. Raw data

| Data | How it arrives | Where |
|---|---|---|
| ISIMIP3b `tasmax`, `tasmin`, `pr` (5 GCMs, historical and three SSPs) | `python main.py BRA --only acquire` (ISIMIP client, resumable, days) | `raw_dir/climate/isimip3b/<model>/<scenario>/<variable>/` |
| W5E5 v2.0 | same step | `raw_dir/climate/w5e5v2.0/<variable>/` |
| HydroBASINS level 6 (`sa`, `as`, `eu`) | same step | `raw_dir/boundaries/hydrobasins/` |
| ONS daily natural inflow energy | same step | `raw_dir/validation/ons_ena/` |
| REN and DGEG (Portugal, supplementary validation) | same step | `raw_dir/validation/` |
| Global Energy Monitor, Global Integrated Power Tracker (xlsx) | manual download from globalenergymonitor.org | `gem_file` |
| WRI Aqueduct 4.0 package | manual download from wri.org | `aqueduct_dir` (the CSV files are derived by `scripts/prepare_aqueduct.py`) |
| Natural Earth 10 m coastline and rivers | manual download from naturalearthdata.com | `natural_earth_*` |
| GADM 4.1 `gadm41_BRA.gpkg`, `gadm41_IND.gpkg`, `gadm41_PRT.gpkg` | manual download from gadm.org | `raw_dir/gadm/` |
| GADM 4.1 Brazil shapefiles (mainland, levels 0 and 1) | manual download from gadm.org | `gadm_bra_dir` |

Licences and versions: [DATA_AVAILABILITY.md](DATA_AVAILABILITY.md).

## 3. Run

```bash
python main.py BRA --dry-run         # plan
python main.py BRA --only acquire    # long: days, network
python main.py BRA --only indices    # long: daily heat and precipitation indices
python main.py BRA --only hydro      # long: water balance and SPEI/SPI
python main.py BRA                   # all other phases, then the headline check
```

Phases, inputs and outputs: [PIPELINE.md](PIPELINE.md). `python main.py BRA --adopt` records the current outputs as
complete when you already have them.

## 4. Check

`scripts/check_headlines.py` runs at the end of `main.py` and compares the headline numbers with their expected values
(13 checks). Figures and tables are written to `<outputs_dir>/article/{figures,tables}`; the reference figures are in
`results/figures`.

## Random numbers

All random draws use `numpy.random.default_rng` with a seed list, so reruns return identical numbers. There are no
unseeded draws in the production code.

| Analysis | Scripts | Stream |
|---|---|---|
| Heat: cell bootstrap, 2,000 draws | `w3_bootstrap.py`, `w3_scenario.py` (`creei.exposure.heat_bootstrap`, `heat_scenario`) | `default_rng([86, group index])` |
| Drought null, hydro (block lengths 12/24/36/60, 2,000 draws) and its SPI version | `w4_null.py`, `w4c_null_spi.py` | `default_rng([23, block])`; AR(1): `default_rng([23, 1])` |
| Drought null, water-dependent thermal | `w4c_null_thermal.py` | `default_rng([23, 100, block])`; AR(1): `default_rng([23, 100, 1])` |
| Drought null, 3-GCM subset | `w6_gcm_subset.py` | `default_rng(23)` and `default_rng([23, 100])` |
| Drought level classes (20,000 draws) | `w4g_drought_levels.py` | `default_rng([23, 99, ...])` |
| E1 hedge failure | `e1_hedge.py` | `default_rng([23, 3, k])`, `k` the running index of the bootstrap calls |
| E1 co-location control | `e1_colocation.py` | same stream with `k` starting at 20,000 |
| E3 correlation interval | `e3_ena_validation.py` | `default_rng([23, 4, k])` |
| E3 hit rate | `e3_hit_rate.py` | `default_rng([23, 5, k])` |
| Supplementary validation table | `25_validation_stats.py` | `default_rng(20260930)` |

`e1_hedge.py` and `e1_colocation.py` use different streams, so their intervals for the same quantity differ by
Monte Carlo error only.

## Known limits

- `python main.py BRA --force geo` rebuilds `gadm_brazil.gpkg`, whose bytes change at each build; the phases that
  read it (`coexposure`, `e1`, `w6`, `article`) then run again with identical results.
- The 36 W5E5 `.nc` files are hashed directly by the `w5e5` phase because the manifest registers the downloaded zip
  files, not the extracted files.
- The Aqueduct water-stress file `plant_aqueduct.parquet` is rebuilt from the official WRI package and differs from an
  earlier hand-prepared version by at most 6e-8 in relative terms; no article result reads it.
