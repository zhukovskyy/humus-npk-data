"""Cross-regional validation of the humus module against Kudria et al. (2024).

Reproduces the metrics and figure reported in the manuscript.
Usage (from the data_release folder):  python scripts/humus_validation.py

Model (annual humus balance, Sokolovsky/Chesnyak-1987 method):
    dH = kappa * R - M
where R is the total post-harvest residue mass reported by the experiment
(by-product + surface + root residues, t/ha), M the reported mineralisation
(kg/ha) and kappa the humification coefficient of the residue class.
Only kappa is supplied by us; everything else is taken as reported.
"""
import csv
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "output")

# Humification coefficient by residue class (t humus per t residue).
KAPPA = {
    "chernozem_zone": {"cereal": 0.15, "green_mass": 0.17},   # target zone
    "polissia_native": {"cereal": 0.20, "green_mass": 0.22},  # out-of-zone reference
}
PLOUGH_LAYER_T_HA = 3500  # reference mass used by the calculator


def load(name):
    with open(os.path.join(DATA, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def metrics(obs, pred):
    e = [p - o for o, p in zip(obs, pred)]
    n = len(e)
    return {
        "n": n,
        "RMSE": math.sqrt(sum(x * x for x in e) / n),
        "MAE": sum(abs(x) for x in e) / n,
        "MB": sum(e) / n,
        "sign_correct": sum((p < 0) == (o < 0) for o, p in zip(obs, pred)),
    }


def main():
    os.makedirs(OUT, exist_ok=True)
    rows = load("kudria2024_table2_humus_balance.csv")

    # kappa-independent checks
    for r in rows:
        assert int(r["formed_kg_ha"]) - int(r["mineralised_kg_ha"]) == int(r["balance_kg_ha"])
    stock = load("kudria2024_table1_humus_stock.csv")
    implied = [float(s["stock_0_30_t_ha"]) / float(s["humus_0_30_pct"]) * 100 for s in stock]
    implied_mass = sum(implied) / len(implied)
    mineral = [int(r["mineralised_kg_ha"]) for r in rows]

    obs = [int(r["balance_kg_ha"]) for r in rows]
    preds, summary = {}, {}
    for case, kap in KAPPA.items():
        p = [kap[r["residue_class"]] * float(r["residues_total_t_ha"]) * 1000
             - int(r["mineralised_kg_ha"]) for r in rows]
        preds[case] = p
        summary[case] = metrics(obs, p)

    with open(os.path.join(OUT, "humus_validation_predictions.csv"), "w",
              newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["predecessor", "rotation", "residue_class", "observed_balance_kg_ha"]
                   + [f"predicted_{c}_kg_ha" for c in KAPPA])
        for i, r in enumerate(rows):
            w.writerow([r["predecessor"], r["rotation"], r["residue_class"], obs[i]]
                       + [round(preds[c][i]) for c in KAPPA])

    lines = ["Balance identity formed - mineralised = balance: exact in all "
             f"{len(rows)} rotations",
             f"Implied plough-layer mass: {implied_mass:.0f} t/ha "
             f"(calculator {PLOUGH_LAYER_T_HA}; diff "
             f"{100 * (implied_mass - PLOUGH_LAYER_T_HA) / PLOUGH_LAYER_T_HA:.1f}%)",
             f"Reported mineralisation: {min(mineral) / 1000:.2f}-{max(mineral) / 1000:.2f} t/ha/yr"]
    for case, m in summary.items():
        lines.append(f"{case}: kappa={KAPPA[case]}  RMSE={m['RMSE']:.0f}  MAE={m['MAE']:.0f}  "
                     f"MB={m['MB']:+.0f} kg/ha/yr  sign correct {m['sign_correct']}/{m['n']}")
    text = "\n".join(lines)
    print(text)
    with open(os.path.join(OUT, "humus_validation_metrics.txt"), "w", encoding="utf-8") as f:
        f.write(text + "\n")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed; figure skipped")
        return
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    lim = (-750, 450)
    ax.plot(lim, lim, "--", color="grey", lw=1, zorder=1)
    ax.axhline(0, color="#ddd", lw=0.8, zorder=0)
    ax.axvline(0, color="#ddd", lw=0.8, zorder=0)
    m_n, m_c = summary["polissia_native"], summary["chernozem_zone"]
    ax.scatter(obs, preds["polissia_native"], marker="s", facecolors="none",
               edgecolors="grey", s=55, lw=1.3, zorder=2,
               label=r"Native Polissia coefficient $\kappa$=0.20/0.22 (out-of-zone)")
    ax.scatter(obs, preds["chernozem_zone"], color="#2a7bd5", s=40, zorder=3,
               label=r"Chernozem-zone coefficient $\kappa$=0.15/0.17"
                     f" (RMSE {m_c['RMSE']:.0f} kg ha$^{{-1}}$)")
    ax.set_xlim(lim)
    ax.set_ylim(lim)
    ax.set_aspect("equal")
    ax.set_xlabel(r"Observed humus balance, Kudria et al. 2024 (kg ha$^{-1}$ yr$^{-1}$)")
    ax.set_ylabel(r"Model-predicted humus balance (kg ha$^{-1}$ yr$^{-1}$)")
    ax.legend(loc="upper left", fontsize=7.5, frameon=False)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(OUT, f"humus_validation.{ext}"), dpi=200)


if __name__ == "__main__":
    main()
