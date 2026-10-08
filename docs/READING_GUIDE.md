# Reading guide

From each article item to the script that draws it, the table it reads, and the script that produces that table.
Tables are written to `<outputs_dir>/tables`; article files to `<outputs_dir>/article/{figures,tables}`.
Phase names are those of `config/pipeline.yaml` (see [PIPELINE.md](PIPELINE.md)).

## Article items

| Item | Content | Drawn by (`scripts/article/`) | Reads | Produced by (phase) |
|---|---|---|---|---|
| Table 0 | Framework parameters | `table0_parameters.py` | `config/params.yaml`, `plant_units.parquet` | `inventory` |
| Table 1 | Fleet and capacity by technology and fuel | `table1_fleet_capacity.py` | `plant_units.parquet`, `plants.parquet` | `inventory` |
| Table 2 | Leave-one-out, five largest hydro plants | `table2_leave_one_out.py` | `w4d_leave_one_out.csv` | `w4d_leave_one_out.py` (`w4`) |
| Table 3 | Heat x drought co-exposure cross-tab | `table3_coexposure_crosstab.py`, `table3_crosstab.py` | `table3_coexposure.csv`, `table3_coexposure_gcm_mean.csv` | `w5_table3_gcm_mean.py` (`coexposure`) |
| Fig 1 | Heat class map, thermal plants | `fig1_heat_class_map.py` | `w3g_heat_cell_class.csv`, `plant_cell.parquet`, `plants.parquet` | `w3g_heat_levels.py` (`w3`) |
| Fig 2 | Heat exposure curves by threshold | `fig2_threshold_curves.py` | `w3_curves_plot.csv` | `w3_curves.py` (`w3`) |
| Fig 3 | Drought exposure map, all plants | `fig3_drought_exposure_map.py` | `w4g_fd_unit_values.csv`, `plants.parquet` | `w4g_drought_levels.py` (`w4`) |
| Fig 4 | Excess exposure over the null | `fig4_excess_over_null.py` | `w4c_spi_vs_spei.csv`, `w6_agreement_k.csv` | `w4c_spi_vs_spei.py` (`w4`), `w6_gcm_subset.py` (`w6`) |
| Fig 5a, 5b | Co-exposure by state (hydro, thermal) | `fig5_state_maps.py` | `w3h_state_coexposure.csv` | `w3h_state_coexposure.py` (`coexposure`) |
| Fig 6 | Heat exposure by fuel | `fig6_thermal_heat_by_fuel.py` | `w3_table1.csv` | `w3_table1.py` (`w3`) |
| Fig 7 | E1 hedge failure | `fig7_e1_hedge.py` | `e1_hedge_{summary,metrics,delta,observed}.csv`, `e1_colocation.csv` | `e1_hedge.py`, `e1_colocation.py` (`e1`) |
| Fig 8 | E3 inflow association | `fig8_e3_ena.py` | `e3_spearman.csv`, `e3_hit_rate.csv` | `e3_ena_validation.py`, `e3_hit_rate.py` (`e3`) |

`python scripts/article/build_all.py` draws every item into `<outputs_dir>/article/_preview`;
`--promote` writes the official folders.

## Headline numbers

`scripts/check_headlines.py` recomputes the headline numbers from the tables (excess over the null, plant and
capacity counts, state sums) and compares them with fixed expected values. It is the last phase of `main.py`
and stops the run on a mismatch.

## From data to tables

| Step | Phase | Scripts |
|---|---|---|
| Plant inventory, units, populations | `inventory` | `05_plants.py`, `05b_plant_units.py` |
| Plant to grid cell and catchment | `spatial` | `06_spatial.py` |
| Daily heat and precipitation indices | `indices` | `04_daily_indices.py` |
| Water balance, SPEI-12, SPI-12 | `hydro` | `07_water_balance.py`, `08_spei.py` |
| Plant-level hazard table | `hazards` | `09_consolidate.py` |
| W5E5 observed series | `w5e5` | `24_w5e5_spei_validation.py`, `e1_w5e5_inputs.py` |
| Heat exposure (axis 1) | `w3` | `w3_*.py`, `th1_fleet_gw.py`, `w3g_heat_levels.py` |
| Drought exposure and null (axis 2) | `w4` | `w4_null.py` ... `w4h_coexposure.py` |
| E1 hedge failure | `e1` | `e1_hedge.py`, `e1_colocation.py` |
| E3 inflow validation | `e3` | `e3_ena_validation.py`, `e3_hit_rate.py` |
| Sensitivities (3-GCM subset, k/5 agreement) | `w6` | `w6_gcm_subset.py`, `w6_nonmonotonicity.py` |
