import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

raw = [
    (2018, 7.2,  941.0),
    (2019, 6.3,  961.0),
    (2020, 6.9,  966.0),
    (2021, 7.5,  974.0),
    (2022, 3.1, 1026.0),
    (2023, 2.9, 1038.0),
    (2024, 1.5, 1198.0),
    (2025, 2.1, 1250.0),
]
df = pd.DataFrame(raw, columns=["Year", "Vacancy", "Rent"])

# Cumulative % change from base year (2018)
df["Rent_cumul"]    = (df["Rent"]    / df["Rent"].iloc[0]    - 1) * 100
df["Vacancy_cumul"] = (df["Vacancy"] / df["Vacancy"].iloc[0] - 1) * 100

# ── Palette ────────────────────────────────────────────────────────────────
BG       = "#0D1117"
PANEL    = "#161B22"
BORDER   = "#30363D"
TEXT_HI  = "#E6EDF3"
TEXT_MID = "#8B949E"
RED      = "#E84855"
RED_DARK = "#9B1C28"

years = df["Year"].values

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), facecolor=BG)

for ax in [ax1, ax2]:
    ax.set_facecolor(PANEL)
    ax.tick_params(colors=TEXT_MID, labelsize=9)
    for sp in ax.spines.values(): sp.set_color(BORDER)
    ax.xaxis.label.set_color(TEXT_MID)
    ax.yaxis.label.set_color(TEXT_MID)
    ax.grid(axis="y", color=BORDER, lw=0.6, alpha=0.5)
    ax.set_xticks(years)
    ax.set_xticklabels(years, rotation=45)
    ax.axhline(0, color=BORDER, lw=1)

# ── Panel 1: Rent cumulative ───────────────────────────────────────────────
rent_vals = df["Rent_cumul"].values

ax1.fill_between(years, 0, rent_vals, alpha=0.15, color=RED)
ax1.plot(years, rent_vals, "o-", color=RED, lw=2.4, ms=7,
         zorder=3, markeredgecolor=BG, markeredgewidth=1.5)

for yr, val in zip(years, rent_vals):
    offset = 12 if val >= 0 else -18
    ax1.annotate(f"+{val:.1f}%" if val >= 0 else f"{val:.1f}%",
                 (yr, val), textcoords="offset points",
                 xytext=(0, offset), fontsize=8,
                 color=TEXT_HI, ha="center", fontweight="bold")

ax1.set_title("Cumulative Rent Increase Since 2018",
              color=TEXT_HI, fontsize=11, fontweight="bold", pad=12)
ax1.set_ylabel("% Change Since 2018 (Base Year)", fontsize=9)
ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"+{x:.0f}%" if x >= 0 else f"{x:.0f}%"))
ax1.set_ylim(-5, 50)

# ── Panel 2: Vacancy cumulative ───────────────────────────────────────────
vac_vals = df["Vacancy_cumul"].values

ax2.fill_between(years, 0, vac_vals,
                 where=(vac_vals >= 0), alpha=0.15, color=RED)
ax2.fill_between(years, 0, vac_vals,
                 where=(vac_vals < 0),  alpha=0.15, color=RED)
ax2.plot(years, vac_vals, "o-", color=RED, lw=2.4, ms=7,
         zorder=3, markeredgecolor=BG, markeredgewidth=1.5)

for yr, val in zip(years, vac_vals):
    offset = 12 if val >= 0 else -18
    ax2.annotate(f"+{val:.1f}%" if val >= 0 else f"{val:.1f}%",
                 (yr, val), textcoords="offset points",
                 xytext=(0, offset), fontsize=8,
                 color=TEXT_HI, ha="center", fontweight="bold")

ax2.set_title("Cumulative Vacancy Rate Change Since 2018",
              color=TEXT_HI, fontsize=11, fontweight="bold", pad=12)
ax2.set_ylabel("% Change Since 2018 (Base Year)", fontsize=9)
ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"+{x:.0f}%" if x >= 0 else f"{x:.0f}%"))
ax2.set_ylim(-85, 25)

# ── Shared drop the bomb annotation ───────────────────────────────────────
fig.text(0.5, 0.01,
         "2018 Base Year  |  Rent +32.8%  vs  Vacancy −70.8%  by 2025",
         ha="center", fontsize=9, color=RED,
         fontweight="bold", fontfamily="monospace",
         bbox=dict(boxstyle="round,pad=0.4", facecolor=PANEL,
                   edgecolor=RED, alpha=0.9))

fig.suptitle("St. John's CMA — Cumulative Change Since 2018 (Base Year)",
             color=TEXT_HI, fontsize=13, fontweight="bold", y=1.01)

plt.tight_layout()
plt.savefig("cumulative_plot.png", dpi=150, bbox_inches="tight", facecolor=BG)
print("Saved: cumulative_plot.png")
