"""
Interrupted Time Series (ITS) - St. John's CMA Rent
Δ ln(Rentₜ) = β₀ + β₁ Post2019ₜ + β₂ Xₜ + εₜ
OLS via numpy lstsq (no statsmodels needed)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
from scipy import stats

# ---------------------------------------------------------------------------
# 1. Data (date1 obs per year)
# ---------------------------------------------------------------------------
raw = [
    (2018,6.75,951.0),
    (2019,6.6,963.5),
    (2020,7.2,970.0),
    (2021,5.3,1000.0),
    (2022,3.0,1032.0),
    (2023,2.2,1118.0),
    (2024,1.8,1224.0),
    (2025,2.05,1305.5)
    ]
df = pd.DataFrame(raw, columns=["Year", "VacancyRate", "Rent2BR"])
df["lnRent"]   = np.log(df["Rent2BR"])
df["DlnRent"]  = df["lnRent"].diff()
df["Post2019"] = (df["Year"] > 2019).astype(float)
df["X"]        = (df["Year"] - df["Year"].min()).astype(float)

mdf = df.dropna(subset=["DlnRent"]).reset_index(drop=True)

# ---------------------------------------------------------------------------
# 2. OLS via numpy
# ---------------------------------------------------------------------------
Y = mdf["DlnRent"].values
A = np.column_stack([np.ones(len(mdf)), mdf["Post2019"].values, mdf["X"].values])

coeffs, residuals, rank, sv = np.linalg.lstsq(A, Y, rcond=None)
b0, b1, b2 = coeffs

Y_hat = A @ coeffs
resid = Y - Y_hat
n, k  = len(Y), 3
s2    = resid @ resid / (n - k)
cov   = s2 * np.linalg.inv(A.T @ A)
se    = np.sqrt(np.diag(cov))
t_stat = coeffs / se
p_vals = 2 * (1 - stats.t.cdf(np.abs(t_stat), df=n - k))
r2     = 1 - np.sum(resid**2) / np.sum((Y - Y.mean())**2)

print("OLS Results: Δln(Rent) = β₀ + β₁·Post2019 + β₂·X")
print(f"  β₀ = {b0:+.4f}  se={se[0]:.4f}  t={t_stat[0]:.2f}  p={p_vals[0]:.3f}")
print(f"  β₁ = {b1:+.4f}  se={se[1]:.4f}  t={t_stat[1]:.2f}  p={p_vals[1]:.3f}")
print(f"  β₂ = {b2:+.4f}  se={se[2]:.4f}  t={t_stat[2]:.2f}  p={p_vals[2]:.3f}")
print(f"  R² = {r2:.3f}   n={n}")

# Reconstruct fitted rent levels
fitted_lnRent = [df["lnRent"].iloc[0]]
for d in Y_hat:
    fitted_lnRent.append(fitted_lnRent[-1] + d)
fitted_rent = np.exp(fitted_lnRent)

# ---------------------------------------------------------------------------
# 3. Plot
# ---------------------------------------------------------------------------
INTERRUPT = 2019
C_BLUE    = "#2E86AB"
C_RED     = "#E84855"
C_AMBER   = "#F4A261"
C_GRAY    = "#8B949E"

fig = plt.figure(figsize=(13, 9), facecolor="#0D1117")
gs  = GridSpec(2, 2, figure=fig, hspace=0.5, wspace=0.35,
               left=0.08, right=0.96, top=0.88, bottom=0.09)
ax1 = fig.add_subplot(gs[0, :])
ax2 = fig.add_subplot(gs[1, 0])
ax3 = fig.add_subplot(gs[1, 1])

for ax in [ax1, ax2, ax3]:
    ax.set_facecolor("#161B22")
    ax.tick_params(colors=C_GRAY, labelsize=9)
    for sp in ax.spines.values():
        sp.set_color("#30363D")
    ax.xaxis.label.set_color(C_GRAY)
    ax.yaxis.label.set_color(C_GRAY)

years = df["Year"].values

# ── Panel 1: Rent levels ──────────────────────────────────────────────────
ax1.axvspan(years[0] - 0.4, INTERRUPT,        alpha=0.06, color=C_BLUE, zorder=0)
ax1.axvspan(INTERRUPT,       years[-1] + 0.4, alpha=0.06, color=C_RED,  zorder=0)
ax1.axvline(INTERRUPT, color="#58A6FF", lw=1.3, ls="--", alpha=0.75, zorder=1)

ax1.plot(years, df["Rent2BR"], "o-", color="#58A6FF", lw=2.2, ms=7,
         zorder=3, label="Observed Rent")
ax1.plot(years, fitted_rent,  "s--", color=C_AMBER,  lw=1.8, ms=6,
         zorder=3, label="ITS Fitted Rent")

# Counterfactual: pre-trend extrapolated
pre = df[df["Year"] <= INTERRUPT]
slope_cf, int_cf, *_ = stats.linregress(pre["Year"], pre["Rent2BR"])
cf_years = years[years >= INTERRUPT]
cf_rent  = int_cf + slope_cf * cf_years
ax1.plot(cf_years, cf_rent, ":", color=C_GRAY, lw=1.6, alpha=0.75,
         label="Pre-trend counterfactual")
obs_post = [df.loc[df["Year"]==y, "Rent2BR"].values[0] for y in cf_years]
ax1.fill_between(cf_years, cf_rent, obs_post,
                 alpha=0.13, color=C_RED, label="Excess rent (post)")

for yr, rent in zip(years, df["Rent2BR"]):
    ax1.annotate(f"${int(rent):,}", (yr, rent),
                 textcoords="offset points", xytext=(0, 11),
                 fontsize=7.5, color="#C9D1D9", ha="center")

ax1.text(0.305, 0.04, "← Pre-2019  |  Post-2019 →",
         transform=ax1.transAxes, color="#58A6FF", fontsize=8, alpha=0.85)

ax1.set_title("St. John's CMA — 2BR Rent: Interrupted Time Series (2018–2025)",
              color="#E6EDF3", fontsize=13, fontweight="bold", pad=12)
ax1.set_ylabel("Average 2BR Rent ($)")
ax1.set_xticks(years)
ax1.legend(fontsize=8, facecolor="#161B22", edgecolor="#30363D",
           labelcolor="#C9D1D9", loc="upper left")
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${int(x):,}"))

# ── Panel 2: Δ ln(Rent) ───────────────────────────────────────────────────
w = 0.32
ax2.bar(mdf["Year"] - w/2, mdf["DlnRent"], w, color=C_BLUE,  alpha=0.85, label="Actual")
ax2.bar(mdf["Year"] + w/2, Y_hat,          w, color=C_AMBER, alpha=0.85, label="Fitted")
ax2.axhline(0, color="#30363D", lw=1)
ax2.axvline(INTERRUPT + 0.5, color="#58A6FF", lw=1, ls="--", alpha=0.6)
ax2.set_title("Δ ln(Rent) — Actual vs Fitted", color="#E6EDF3",
              fontsize=10, fontweight="bold")
ax2.set_xticks(mdf["Year"])
ax2.set_xticklabels(mdf["Year"], rotation=45)
ax2.legend(fontsize=7.5, facecolor="#161B22", edgecolor="#30363D", labelcolor="#C9D1D9")
ax2.set_ylabel("Δ ln(Rent)")

# ── Panel 3: Vacancy Rate ─────────────────────────────────────────────────
bar_colors = [C_BLUE if y <= INTERRUPT else C_RED for y in years]
ax3.bar(years, df["VacancyRate"], color=bar_colors, alpha=0.85, width=0.6)
ax3.axvline(INTERRUPT + 0.3, color="#58A6FF", lw=1, ls="--", alpha=0.6)
for yr, vr in zip(years, df["VacancyRate"]):
    ax3.text(yr, vr + 0.1, f"{vr}%", ha="center", fontsize=7.5, color="#C9D1D9")
ax3.set_title("Vacancy Rate (%) Over Time", color="#E6EDF3",
              fontsize=10, fontweight="bold")
ax3.set_xticks(years)
ax3.set_xticklabels(years, rotation=45)
ax3.set_ylabel("Vacancy Rate (%)")
ax3.legend(handles=[mpatches.Patch(color=C_BLUE, label="Pre-2019"),
                    mpatches.Patch(color=C_RED,  label="Post-2019")],
           fontsize=7.5, facecolor="#161B22", edgecolor="#30363D", labelcolor="#C9D1D9")

# ── Regression box ────────────────────────────────────────────────────────
def stars(p):
    return "***" if p < 0.01 else ("**" if p < 0.05 else ("*" if p < 0.1 else "ns"))

annot = (
    "OLS: Δln(Rent) = β₀ + β₁·Post2019 + β₂·X\n"
    f"β₀ = {b0:+.4f}  (p={p_vals[0]:.3f}) {stars(p_vals[0])}\n"
    f"β₁ = {b1:+.4f}  (p={p_vals[1]:.3f}) {stars(p_vals[1])}\n"
    f"β₂ = {b2:+.4f}  (p={p_vals[2]:.3f}) {stars(p_vals[2])}\n"
    f"R² = {r2:.3f}   n = {n}"
)
fig.text(0.97, 0.975, annot, transform=fig.transFigure,
         fontsize=8.5, color="#C9D1D9", va="top", ha="right",
         fontfamily="monospace",
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#161B22",
                   edgecolor="#58A6FF", alpha=0.95))

plt.savefig("its_stjohns.png", dpi=150, bbox_inches="tight", facecolor="#0D1117")
print("\nSaved: its_stjohns.png")
