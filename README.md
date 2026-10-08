# creei-brazil

Code for the exposure of Brazilian hydropower and thermal power plants to heat and drought under ISIMIP3b climate
projections: five GCMs, three scenarios (SSP1-2.6, SSP3-7.0, SSP5-8.5), baseline 1985-2014 and future 2041-2070.
The analysis reports plant-level exposure, the excess over a stationary resampling null, the co-exposure of heat and
drought, a test of whether thermal plants hedge hydropower drought, and a comparison of the drought index with
observed natural inflow.

## Layout

| Path | Content |
|---|---|
| `main.py` | Runs the pipeline for a country: `python main.py BRA` |
| `src/creei/` | Library: acquisition, inventory, spatial mapping, hazards (heat, SPEI/SPI), null model, exposure |
| `scripts/` | One script per analysis step; `scripts/article/` builds the figures and tables of the article |
| `config/` | `pipeline.yaml` (phases), `params.yaml` (every numeric parameter and its source), `countries/BRA.yaml`, `paths.example.yaml` |
| `tests/` | Unit tests |
| `results/figures/` | Figures of the article (PNG) |
| `docs/` | [REPRODUCE.md](docs/REPRODUCE.md), [PIPELINE.md](docs/PIPELINE.md), [DATA_AVAILABILITY.md](docs/DATA_AVAILABILITY.md), [READING_GUIDE.md](docs/READING_GUIDE.md) |

## Installation

```bash
conda env create -f environment.yml      # or: python -m venv .venv && pip install -r requirements.txt
conda activate creei
pip install -e . --no-deps
cp config/paths.example.yaml config/paths.local.yaml   # then edit the paths
python -m pytest -q
```

Versions are pinned to those used for the article results (Python 3.11).

## Reproduce

1. Get the raw data (ISIMIP3b, W5E5, GEM, Aqueduct, HydroBASINS, Natural Earth, GADM, ONS): see
   [DATA_AVAILABILITY.md](docs/DATA_AVAILABILITY.md) and [REPRODUCE.md](docs/REPRODUCE.md).
2. `python main.py BRA --dry-run` prints the plan; `python main.py BRA` runs every phase except the long ones
   (`acquire`, `indices`, `hydro`, which are named with `--only`). See [PIPELINE.md](docs/PIPELINE.md).
3. `python scripts/check_headlines.py` (the last phase of `main.py`) compares the headline numbers with their
   expected values.

Time and disk space are in [REPRODUCE.md](docs/REPRODUCE.md).

## Random numbers

Every bootstrap and null simulation uses `numpy.random.default_rng` with a fixed seed derived from 23, so reruns give
identical numbers. See [REPRODUCE.md](docs/REPRODUCE.md) for the streams.

## Licence and citation

Code: MIT, see `LICENSE`. The data keep the licences of their sources ([DATA_AVAILABILITY.md](docs/DATA_AVAILABILITY.md)).
GADM geometry is not redistributed. Citation: see `CITATION.cff`.
