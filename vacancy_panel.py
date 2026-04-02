import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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
mean_vac = df["Vacancy"].mean()

BG      = "#0D1117"
PANEL   = "#161B22"
BORDER  = "#30363D"
TEXT_HI = "#E6EDF3"
TEXT_MID= "#8B949E"
FLAT_C  = "#2E86AB"
RISE_C  = "#E84855"
MEAN_C  = "#F4A261"

years = df["Year"].values
vacs  = df["Vacancy"].values

fig, ax = plt.subplots(figsize=(9, 5), facecolor=BG)
ax.set_facecolor(PANEL)
ax.tick_params(colors=TEXT_MID, labelsize=9)
for sp in ax.spines.values(): sp.set_color(BORDER)
ax.grid(axis="y", color=BORDER, lw=0.6, alpha=0.5)

vac_colors = [FLAT_C if y <= 2021 else RISE_C for y in years]
bars = ax.bar(years, vacs, color=vac_colors, alpha=0.88, width=0.55, zorder=2)

for bar, val in zip(bars, vacs):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.1,
            f"{val}%", ha="center", fontsize=8.5,
            color=TEXT_HI, fontweight="bold")

ax.axhline(mean_vac, color=MEAN_C, lw=1.6, ls="--", alpha=0.9, zorder=3)
ax.text(years[-1] + 0.38, mean_vac + 0.12,
        f"Mean\n{mean_vac:.1f}%",
        color=MEAN_C, fontsize=8, fontweight="bold", va="bottom")

ax.axvline(2021.5, color=TEXT_MID, lw=0.8, ls=":", alpha=0.5)
ax.text(2019.5, 8.05, "STAGNATION", color=FLAT_C,
        fontsize=8, fontweight="bold", ha="center", alpha=0.85)
ax.text(2023.5, 8.05, "ACCELERATION", color=RISE_C,
        fontsize=8, fontweight="bold", ha="center", alpha=0.85)

ax.set_title("St. John's CMA — Vacancy Rate (2018–2025)",
             color=TEXT_HI, fontsize=12, fontweight="bold", pad=12)
ax.set_ylabel("Vacancy Rate (%)", color=TEXT_MID)
ax.set_xticks(years)
ax.set_xlim(2017.6, 2026.2)
ax.set_ylim(0, 8.8)
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.0f}%"))

import matplotlib.patches as mpatches
ax.legend(handles=[
    mpatches.Patch(color=FLAT_C, label="Pre-2022 (stagnation)"),
    mpatches.Patch(color=RISE_C, label="Post-2022 (acceleration)"),
], fontsize=8, facecolor=PANEL, edgecolor=BORDER, labelcolor=TEXT_HI,
   loc="upper right")

plt.tight_layout()
plt.savefig("vacancy_panel.png", dpi=150, bbox_inches="tight", facecolor=BG)
print(f"Saved  |  mean vacancy = {mean_vac:.1f}%")
