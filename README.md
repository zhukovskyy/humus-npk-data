# Humus–NPK decision-support framework: validation data and coefficients

Supplementary data and code for:

> Zhukovskyy V., Skrypchuk P., Shpak H., Zhukovska N. *A GIS-enabled environmental
> decision-support framework for integrated humus and NPK balance modelling in
> crop-rotation planning.* Manuscript submitted for publication.

Web application: <https://organicportal.in.ua/organic-map>

## Contents

| File | Content | Origin |
|---|---|---|
| `data/kudria2024_table2_humus_balance.csv` | Humus balance of 16 short rotations (mean 1996–2015): residue fractions, humus formed, mineralised, balance | Values transcribed from Kudria et al. (2024), Table 2 |
| `data/kudria2024_table1_humus_stock.csv` | Humus content (0–10, 10–20, 20–30 cm) and 0–30 cm stock after 13 rotations | Values transcribed from Kudria et al. (2024), Table 1 |
| `data/npk_coefficient_audit_podobed.csv` | Term-by-term comparison of NPK balance coefficients | This work vs. Podobed (see manuscript) |
| `data/calculator_coefficients.csv` | Representative model coefficients (residue regressions, humification, mineralisation, removal norms, fertiliser contents, deposition, fixation) | Read from the deployed calculator |
| `data/npk_worked_example.csv` | N, P, K inputs, outputs and balances for a four-crop organic rotation | Output of the deployed calculator |
| `scripts/humus_validation.py` | Reproduces the cross-regional humus validation (metrics + figure) | This work |
| `output/` | Script outputs: predictions, metrics, figure | Generated |

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

Model: annual humus balance ΔH = κ·R − M (Sokolovsky/Chesnyak 1987 method), where
R is the total post-harvest residue mass and M the mineralisation, both as reported
by the experiment. Only the humification coefficient κ is supplied:
0.15 (cereal and grain-legume residues) / 0.17 (green-mass legumes) for the
Left-Bank chernozem zone; 0.20/0.22 is the calculator's native Polissia value,
shown as an out-of-zone reference.

## Notes on the data

- **Kudria et al. (2024)**: numerical values were transcribed by the present
  authors from the published tables; column layout, labels and units were
  re-organised. For every row, formed − mineralised = balance holds exactly, and
  the three residue fractions sum to the totals used. Residue classes
  (`cereal` / `green_mass`) are our classification. Productivity is in tonnes of
  feed-protein units per ha, as in the source.
- The original articles are **not** redistributed here; please obtain them from
  the publishers.
- Residue regressions in `calculator_coefficients.csv` are in centners per hectare
  (1 c = 0.1 t), as in the source agronomic tables and the calculator code.

## Sources

- Kudria S.I., Tarariko Yu.O., Kudria N.A., Lychuk H.I. (2024). The humus regime of
  typical chernozem in short crop rotations with different leguminous components.
  *Visnyk Agrarnoi Nauky* 1(850): 64–70. <https://doi.org/10.31073/agrovisnyk202401-08>
- Chesnyak G.Ya., Zinchenko M.M., Serokurov Yu.I. (1987). Calculation of the humus
  balance and organic-fertiliser rates… Methodical recommendations. Kharkiv.
- Podobed O.Yu. Balance of nitrogen, phosphorus, potassium and crop-rotation
  productivity under long-term fertiliser use. *Bulletin of the Institute of Grain
  Farming* (in Ukrainian).
- Skrypchuk P. et al. (2020). *Journal of Ecological Engineering*.
  <https://doi.org/10.12911/22998993/123255>

## Licence

The compilation, derived values, model predictions and code in this package are
released under **CC BY 4.0** (<https://creativecommons.org/licenses/by/4.0/>).
Values transcribed from third-party publications remain attributable to their
authors; cite the original sources listed above when reusing them.

## Contact

Viktor Zhukovskyy, National University of Water and Environmental Engineering,
Rivne, Ukraine — v.v.zhukovskyy@nuwm.edu.ua
