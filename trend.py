import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import FuncFormatter

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
df = pd.DataFrame(raw, columns=["Year", "Vacancy", "Rent"])
df["YoY_pct"]        = df["Rent"].pct_change() * 100
df["Since_base_pct"] = (df["Rent"] / df["Rent"].iloc[0] - 1) * 100

mean_rent    = df["Rent"].mean()
mean_vac     = df["Vacancy"].mean()
mean_yoy     = df["YoY_pct"].mean()
mean_cumul   = df["Since_base_pct"].mean()

# ── Palette ────────────────────────────────────────────────────────────────
BG      = "#0D1117"
PANEL   = "#161B22"
BORDER  = "#30363D"
TEXT_HI = "#E6EDF3"
TEXT_MID= "#8B949E"
FLAT_C  = "#2E86AB"
RISE_C  = "#E84855"
TEAL    = "#3FB950"
MEAN_C  = "#F4A261"   # amber — mean lines

years = df["Year"].values
rents = df["Rent"].values
vacs  = df["Vacancy"].values

fig = plt.figure(figsize=(14, 11), facecolor=BG)
gs  = GridSpec(2, 2, figure=fig,
               hspace=0.52, wspace=0.38,
               left=0.07, right=0.97, top=0.91, bottom=0.07)

ax_its  = fig.add_subplot(gs[0, :])
ax_yoy  = fig.add_subplot(gs[1, 0])
ax_vac  = fig.add_subplot(gs[1, 1])   # ← vacancy replaces cumulative

for ax in [ax_its, ax_yoy, ax_vac]:
    ax.set_facecolor(PANEL)
    ax.tick_params(colors=TEXT_MID, labelsize=9)
    for sp in ax.spines.values(): sp.set_color(BORDER)
    ax.xaxis.label.set_color(TEXT_MID)
    ax.yaxis.label.set_color(TEXT_MID)
    ax.grid(axis="y", color=BORDER, lw=0.6, alpha=0.5)

# ══════════════════════════════════════════════════════════════════════════
# Panel 1 — ITS  +  mean rent line
# ══════════════════════════════════════════════════════════════════════════
ax_its.axvspan(2018 - 0.4, 2021.5, alpha=0.07, color=FLAT_C, zorder=0)
ax_its.axvspan(2021.5,     2025.4, alpha=0.07, color=RISE_C, zorder=0)
ax_its.axvline(2021.5, color=TEXT_MID, lw=0.8, ls=":", alpha=0.5)

ax_its.text(2019.5, 1242, "STAGNATION PHASE", color=FLAT_C,
            fontsize=8.5, fontweight="bold", ha="center", alpha=0.85)
ax_its.text(2023.5, 1242, "ACCELERATION PHASE", color=RISE_C,
            fontsize=8.5, fontweight="bold", ha="center", alpha=0.85)

# Mean rent reference line
ax_its.axhline(mean_rent, color=MEAN_C, lw=1.4, ls="--", alpha=0.85, zorder=2)
ax_its.text(2025.08, mean_rent + 4, f"Mean\n${mean_rent:,.0f}",
            color=MEAN_C, fontsize=7.5, va="bottom", fontweight="bold")

# Shade above/below mean
ax_its.fill_between(years, mean_rent, rents,
                    where=(rents >= mean_rent),
                    alpha=0.12, color=RISE_C, interpolate=True)
ax_its.fill_between(years, mean_rent, rents,
                    where=(rents < mean_rent),
                    alpha=0.12, color=FLAT_C, interpolate=True)

# Coloured segments
for i in range(len(years) - 1):
    c = FLAT_C if years[i] <= 2021 else RISE_C
    ax_its.plot(years[i:i+2], rents[i:i+2], "-", color=c, lw=2.4, zorder=3)

for yr, r in zip(years, rents):
    c = FLAT_C if yr <= 2021 else RISE_C
    ax_its.plot(yr, r, "o", color=c, ms=8, zorder=4,
                markeredgecolor=BG, markeredgewidth=1.5)
    ax_its.annotate(f"${int(r):,}", (yr, r),
                    textcoords="offset points", xytext=(0, 12),
                    fontsize=8, color=TEXT_HI, ha="center", fontweight="bold")

ax_its.annotate("+$160 (+15.4%)",
                xy=(2024, 1198), xytext=(2023.05, 1158),
                fontsize=8, color=RISE_C, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=RISE_C, lw=1.3))

ax_its.set_title(
    "St. John's CMA — 2BR Average Rent (2018–2025)  |  Interrupted Time Series",
    color=TEXT_HI, fontsize=13, fontweight="bold", pad=14)
ax_its.set_ylabel("Average 2BR Rent ($)", fontsize=9)
ax_its.set_xticks(years)
ax_its.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"${int(x):,}"))
ax_its.set_ylim(870, 1310)

# ══════════════════════════════════════════════════════════════════════════
# Panel 2 — YoY %  +  mean YoY line
# ══════════════════════════════════════════════════════════════════════════
yoy_df = df.dropna(subset=["YoY_pct"])
bar_colors = [FLAT_C if y <= 2021 else RISE_C for y in yoy_df["Year"]]

bars = ax_yoy.bar(yoy_df["Year"], yoy_df["YoY_pct"],
                  color=bar_colors, alpha=0.88, width=0.55, zorder=2)

for bar, val in zip(bars, yoy_df["YoY_pct"]):
    ax_yoy.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.2,
                f"+{val:.1f}%", ha="center", fontsize=7.5,
                color=TEXT_HI, fontweight="bold")

ax_yoy.axhline(mean_yoy, color=MEAN_C, lw=1.4, ls="--", alpha=0.9, zorder=3)
ax_yoy.text(yoy_df["Year"].iloc[-1] + 0.32, mean_yoy + 0.2,
            f"Mean\n+{mean_yoy:.1f}%",
            color=MEAN_C, fontsize=7.5, fontweight="bold", va="bottom")

ax_yoy.axhline(0, color=BORDER, lw=1)
ax_yoy.axvline(2021.5, color=TEXT_MID, lw=0.8, ls=":", alpha=0.5)
ax_yoy.set_title("Year-over-Year Rent Increase (%)",
                 color=TEXT_HI, fontsize=10, fontweight="bold")
ax_yoy.set_xticks(yoy_df["Year"])
ax_yoy.set_xticklabels(yoy_df["Year"], rotation=45)
ax_yoy.set_ylabel("% Change from Prior Year")
ax_yoy.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.0f}%"))
ax_yoy.set_xlim(2018.4, 2025.9)

# ══════════════════════════════════════════════════════════════════════════
# Panel 3 — Vacancy Rate  +  mean vacancy line
# ══════════════════════════════════════════════════════════════════════════
vac_colors = [FLAT_C if y <= 2021 else RISE_C for y in years]
vac_bars = ax_vac.bar(years, vacs, color=vac_colors, alpha=0.88, width=0.55, zorder=2)

for bar, val in zip(vac_bars, vacs):
    ax_vac.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.1,
                f"{val}%", ha="center", fontsize=7.5,
                color=TEXT_HI, fontweight="bold")

ax_vac.axhline(mean_vac, color=MEAN_C, lw=1.4, ls="--", alpha=0.9, zorder=3)
ax_vac.text(years[-1] + 0.32, mean_vac + 0.1,
            f"Mean\n{mean_vac:.1f}%",
            color=MEAN_C, fontsize=7.5, fontweight="bold", va="bottom")

ax_vac.axvline(2021.5, color=TEXT_MID, lw=0.8, ls=":", alpha=0.5)
ax_vac.set_title("Vacancy Rate (%) Over Time",
                 color=TEXT_HI, fontsize=10, fontweight="bold")
ax_vac.set_xticks(years)
ax_vac.set_xticklabels(years, rotation=45)
ax_vac.set_ylabel("Vacancy Rate (%)")
ax_vac.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.0f}%"))
ax_vac.set_xlim(2017.6, 2026.2)

# ══════════════════════════════════════════════════════════════════════════
# Key findings box
# ══════════════════════════════════════════════════════════════════════════
insight = (
    "St. John's CMA  |  2018–2025 Averages\n"
    "────────────────────────────────────\n"
    f"Mean 2BR Rent   :  ${mean_rent:,.0f}/mo\n"
    f"Mean Vacancy    :  {mean_vac:.1f}%\n"
    f"Mean YoY Growth :  +{mean_yoy:.1f}%/yr\n"
    "────────────────────────────────────\n"
    "Stagnation  2018–21 :  +3.5% total\n"
    "Acceleration 2022–25:  +28.4% total\n"
    f"Peak YoY            :  +15.4% (2024)"
)

fig.text(0.975, 0.065, insight,
         transform=fig.transFigure,
         fontsize=8.2, color=TEXT_HI, va="bottom", ha="right",
         fontfamily="monospace",
         bbox=dict(boxstyle="round,pad=0.65", facecolor=PANEL,
                   edgecolor=TEAL, alpha=0.97))

plt.savefig("rent_trend_v21.png", dpi=150, bbox_inches="tight", facecolor=BG)
print(f"Done  |  mean_rent=${mean_rent:.0f}  mean_vac={mean_vac:.1f}%  mean_yoy={mean_yoy:.1f}%")
