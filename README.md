# Humus–NPK balances of crop rotations: coefficients, validation data and optimisation results

Supplementary data for:

> Zhukovskyy V., Skrypchuk P., Shpak H., Zhukovska N. *Balancing soil humus, nitrogen
> and income in organic crop rotations: a multi-objective decision-support model with
> farmer profiles.* Manuscript submitted for publication.

Web application: <https://organicportal.in.ua/organic-map>

## Contents

### Input data and coefficients (`data/`)

| File | Content | Origin |
|---|---|---|
| `crop_coefficients.csv` | Per crop: district base yield and planned-yield range, residue-from-yield regressions, humification and mineralisation coefficients, removal norms, by-product nutrient contents, seed rates and contents, 2021 sale price (UAH and EUR) | Regional reference tables of the calculation workbook; prices: State Statistics Service of Ukraine |
| `model_parameters.csv` | Site parameters, green-manure, fixation, deposition, leaching and loss coefficients, fertiliser contents and maximum rates, input costs, exchange rate | Reference tables; NBU |
| `kudria2024_table2_humus_balance.csv` | Humus balance of 16 short rotations (mean 1996–2015): residue fractions, humus formed, mineralised, balance | Transcribed from Kudria et al. (2024), Table 2 |
| `kudria2024_table1_humus_stock.csv` | Humus content and 0–30 cm stock after 13 rotations | Transcribed from Kudria et al. (2024), Table 1 |
| `npk_coefficient_audit_podobed.csv` | Term-by-term comparison of NPK balance coefficients | This work vs. Podobed (2010) |

### Results (`output/`)

| File | Content |
|---|---|
| `worked_example.csv` | Year-by-year humus and N, P, K balances of the five-field organic rotation of the workbook (no sizing, organic and conventional mode) |
| `molp_front_organic.csv`, `molp_front_conventional.csv` | Weakly efficient (Slater) plans from the multi-objective linear programmes; column `pareto` marks Pareto-efficient plans; column `plan` gives planned yields (c/ha) and input rates per field |
| `scenarios.json`, `scenarios_table.csv` | Plans selected for the farmer profiles S0–S4, the calculator rule B1 and the humus-only ranking B2, and the sensitivity runs |
| `fertility_price.csv` | Maximum gross margin and shadow price of humus as a function of the humus target |
| `molp_front.*`, `fertility_price.*` | Figures |
| `humus_validation_*`, `humus_validation.*` | Cross-regional validation of the humus module |
| `scripts/humus_validation.py` | Reproduces the humus validation |

Units: humus in t/ha (or %), nutrients in kg/ha of N, P2O5 and K2O, money in EUR at the
mean official NBU exchange rate of 2021 (32.3009 UAH/EUR). Residue regressions use
yields in centners per hectare (1 c = 0.1 t), as in the source tables. Objectives in
the result files are rotation means per hectare and year: humus balance `dH`
(t/ha/yr), nitrogen deficit (kg/ha/yr) and gross margin over input cost (EUR/ha/yr).

The optimisation code is available from the corresponding author on reasonable request.

## Reproducing the humus validation

```
python scripts/humus_validation.py
```

Requires Python 3.8+; `matplotlib` only for the figure. Expected output:

```
Balance identity formed - mineralised = balance: exact in all 16 rotations
Implied plough-layer mass: 3570 t/ha (calculator 3500; diff 2.0%)
Reported mineralisation: 1.20-1.54 t/ha/yr
chernozem_zone: RMSE=41  MAE=37  MB=-9 kg/ha/yr  sign correct 16/16
polissia_native: RMSE=329  MAE=324  MB=+324 kg/ha/yr  sign correct 4/16
```

## Notes on the data

- **Kudria et al. (2024)**: numerical values were transcribed by the present authors
  from the published tables; column layout, labels and units were re-organised.
  Residue classes (`cereal` / `green_mass`) are our classification.
- The original articles are **not** redistributed here; please obtain them from the
  publishers.
- Prices: average 2021 sale prices of enterprises in Rivne oblast (State Statistics
  Service of Ukraine). Forage and green manure carry no revenue. Phosphorite flour,
  Ecosoil and sapropel have no official prices and are costed by nutrient content.

## Sources

- Kudria S.I., Tarariko Yu.O., Kudria N.A., Lychuk H.I. (2024). The humus regime of
  typical chernozem in short crop rotations with different leguminous components.
  *Visnyk Agrarnoi Nauky* 1(850): 64–70. <https://doi.org/10.31073/agrovisnyk202401-08>
- Chesnyak G.Ya., Zinchenko M.M., Serokurov Yu.I. (1987). Calculation of the humus
  balance and organic-fertiliser rates… Methodical recommendations. Kharkiv.
- Podobed O.Yu. (2010). Balance of nitrogen, phosphorus, potassium and crop-rotation
  productivity under long-term fertiliser use. *Bulletin of the Institute of Grain
  Farming* (in Ukrainian).
- Skrypchuk P. et al. (2020). *Journal of Ecological Engineering*.
  <https://doi.org/10.12911/22998993/123255>
- State Statistics Service of Ukraine. Sale of agricultural products by enterprises
  and households, 2021. <https://stat.gov.ua/en/datasets/implementation-agricultural-products-enterprises-and-households>

## Licence

The compilation, derived values, model results and code in this package are released
under **CC BY 4.0** (<https://creativecommons.org/licenses/by/4.0/>). Values transcribed
from third-party publications remain attributable to their authors; cite the original
sources listed above when reusing them.

## Contact

Viktor Zhukovskyy, National University of Water and Environmental Engineering,
Rivne, Ukraine — v.v.zhukovskyy@nuwm.edu.ua
