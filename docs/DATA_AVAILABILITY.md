# Data availability

The repository holds code and configuration only. Raw and processed data are not stored in Git
(`config/paths.local.yaml` points to them). This file lists every source the Brazil pipeline reads, its version,
its licence and whether it may be redistributed.

Status: "Checked" means the licence text was read at the source or in the downloaded file; "Author-confirmed" means the
authors reviewed the terms and recorded them here.

## Sources

| Source | Used for | Version / release | Licence and terms | Redistribution | Official page | Status |
|---|---|---|---|---|---|---|
| ISIMIP3b bias-adjusted atmospheric climate input data (tasmax, tasmin, pr; GFDL-ESM4, IPSL-CM6A-LR, MPI-ESM1-2-HR, MRI-ESM2-0, UKESM1-0-LL; historical, SSP1-2.6, SSP3-7.0, SSP5-8.5) | Heat and drought indices | ISIMIP3BASD v2.5.0 and W5E5 v2.0 (global attributes of the files), DOI 10.48364/ISIMIP.842396 | ISIMIP Repository terms of use; the licence is assigned to each dataset (see its metadata). Cite the dataset DOIs and acknowledge ISIMIP (below) | Not redistributed here | https://www.isimip.org/outputdata/licenses/ | Author-confirmed; the individual licence of each dataset is to be listed from its metadata |
| W5E5 v2.0 (observational reference) | Observed SPEI, E1 and E3 inputs | Version 2.0, DOI 10.48364/ISIMIP.342217 | Same terms as above | Not redistributed here | https://data.isimip.org/10.48364/ISIMIP.342217 | Author-confirmed; individual licence to be listed |
| Global Energy Monitor, Global Integrated Power Tracker | Plant inventory | August 2026 release (About sheet of the file) | CC BY 4.0 | Allowed with attribution | https://globalenergymonitor.org/projects/global-integrated-power-tracker/download-data/ | Checked |
| WRI Aqueduct 4.0 (`aqueduct-4-0-water-risk-data.zip`, 5 July 2023 package) | Water stress of thermal plants; `scripts/prepare_aqueduct.py` derives the per-country inputs | 4.0 | WRI open data commitment: open licence, free use, sharing and adaptation with attribution to WRI (CC BY 4.0 on the Aqueduct FAQ) | Allowed with attribution | https://www.wri.org/aqueduct | Author-confirmed |
| HydroBASINS (HydroSHEDS), South America level 6, v1c | Upstream catchments of hydro plants | `hybas_sa_lev06_v1c` | HydroSHEDS licence agreement: free for scientific, educational and commercial use; redistribution restrictions and a required citation (below) | The raw files are not redistributed | https://www.hydrosheds.org/page/hydrobasins | Author-confirmed; full text in the HydroSHEDS technical documentation |
| Natural Earth 10 m (coastline, rivers, admin boundaries) | Distance to coast, base maps | As downloaded by `scripts/geo_base.py` | Public domain | Allowed | https://www.naturalearthdata.com/about/terms-of-use/ | Checked |
| GADM 4.1, Brazil | State polygons of the article maps | 4.1 | Free for academic and other non-commercial use; redistribution and commercial use need permission. Maps made from GADM may be published in academic articles | The data are not redistributed; the article figures with state boundaries are an academic use | https://gadm.org/license.html | Checked and author-confirmed |
| ONS Open Data, daily natural inflow energy (ENA) by subsystem | E3 validation | Files `ENA_Diario_por_Subsistema-<year>.csv`, 2000 onward | Open data of the Brazilian system operator; cite the source | Not redistributed here | https://dados.ons.org.br | Author-confirmed |
| REN DataHub, hydropower productivity index; DGEG monthly hydropower generation (Portugal) | Supplementary validation table `validation.csv` only | Downloaded 2026 | Open data of the Portuguese electricity system; cite the source | Not redistributed here | https://datahub.ren.pt, https://www.dgeg.gov.pt | Author-confirmed; no article result uses them |
| EM-DAT | Not used by any article result | Local copy | CRED terms: non-commercial use, no redistribution | Not allowed | https://doc.emdat.be/docs/legal/terms-of-use/ | Checked; excluded |

## Citations and acknowledgements required by the sources

- **ISIMIP3b and W5E5.** Cite the DOI of each dataset used (10.48364/ISIMIP.842396 and 10.48364/ISIMIP.342217) or
  acknowledge: "For their roles in producing, coordinating, and making available the ISIMIP input data and impact model
  output, we acknowledge the modelling groups, the ISIMIP sector coordinators and the ISIMIP cross-sectoral science team
  for the YY sectors." Co-authorship with the modelling groups is not required but encouraged. Notify
  info@isimip.org of the use and send the publication reference; check the changelog of the data for the latest
  version before submission.
- **HydroBASINS.** Lehner, B., Grill, G. (2013). Global river hydrography and network routing: baseline data and new
  approaches to study the world's large river systems. Hydrological Processes, 27(15): 2171-2186.
  https://doi.org/10.1002/hyp.9740
- **Aqueduct.** Attribute to the World Resources Institute (Kuzma et al., 2023, https://doi.org/10.46830/writn.23.00061).
- **Global Energy Monitor.** "Global Energy Monitor, Global Integrated Power Tracker, August 2026 release."
- **REN, DGEG, ONS.** Cite each source.

## What the repository and the Zenodo release contain

The repository (and the Zenodo record created from its release) holds the code, the configuration, the tests,
the documentation and the figures of the article (`results/figures`). It holds no data and no result tables:
the acquisition scripts download the raw data from the official sources listed above, and `python main.py BRA`
rebuilds every processed file and table. For this reason no third-party data are redistributed, and the licence
column above governs only what each user downloads.

Approximate sizes of what a user downloads and builds (measured on the author's run):

| Part | Size |
|---|---|
| Raw ISIMIP3b files cropped to the three study countries | 16 GB |
| Raw W5E5 v2.0 | 2.5 GB |
| Raw Aqueduct 4.0 | 1.0 GB |
| GADM and boundaries | about 0.5 GB |
| Processed files (`processed_dir`) | 1.3 GB |
| Result tables (`outputs_dir/tables`) | 49 MB |

The GADM geometry used for the state maps is not redistributed; each user downloads GADM 4.1 for Brazil
(see `config/paths.example.yaml`). The figures of `results/figures` show GADM state boundaries, which the GADM licence
allows for academic publications.
