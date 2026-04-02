import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

raw = [

    (2018,6.75,951.0),
    (2019,6.6,963.5),
    (2020,7.2,970.0),
    (2021,5.3,1000.0),
    (2022,3.0,1032.0),
    (2023,2.2,1118.0),
    (2024,1.8,1224.0),
    (2025,2.05,1305.5),
]
df = pd.DataFrame(raw, columns=["Year", "Vacancy", "Rent"])
df["Rent_chg"]    = df["Rent"].pct_change() * 100
df["Vacancy_chg"] = df["Vacancy"].diff()

def fmt_chg(val, up_is_red=True):
    """Format a change value with arrow and colour.
       up_is_red=True  → rent: going up is red (bad for tenant)
       up_is_red=False → vacancy: going up is green (market loosening)
    """
    if pd.isna(val):
        return "—", "#8B949E"
    sign  = "+" if val >= 0 else ""
    arrow = "▲" if val > 0 else ("▼" if val < 0 else "—")
    text  = f"{arrow} {sign}{val:.1f}%"
    if up_is_red:
        color = "#E84855" if val > 0 else "#3FB950"   # rent: up=red, down=green
    else:
        color = "#3FB950" if val > 0 else "#E84855"   # vacancy: up=green, down=red
    return text, color

# Build display rows
rows = []
for _, r in df.iterrows():
    rent_chg_txt,  rent_chg_col  = fmt_chg(r["Rent_chg"],    up_is_red=True)
    vac_chg_txt,   vac_chg_col   = fmt_chg(r["Vacancy_chg"], up_is_red=False)
    rows.append({
        "year":         str(int(r["Year"])),
        "rent":         f"${int(r['Rent']):,}",
        "rent_chg":     rent_chg_txt,
        "rent_chg_col": rent_chg_col,
        "vac":          f"{r['Vacancy']}%",
        "vac_chg":      vac_chg_txt,
        "vac_chg_col":  vac_chg_col,
    })

# ── Palette ────────────────────────────────────────────────────────────────
BG       = "#0D1117"
PANEL    = "#161B22"
BORDER   = "#30363D"
HDR_BG   = "#21262D"
TEXT_HI  = "#E6EDF3"
TEXT_MID = "#8B949E"
ALT_ROW  = "#1C2128"
FLAT_C   = "#2E86AB"
RISE_C   = "#E84855"

COL_X     = [0.04, 0.20, 0.38, 0.58, 0.76]   # x positions (0–1)
COL_W     = [0.10, 0.16, 0.18, 0.10, 0.18]
HEADERS   = ["Year", "Avg 2BR Rent", "Rent Change", "Vacancy", "Vacancy Change"]
ROW_H     = 0.082
HDR_H     = 0.10
TOP_Y     = 0.82

fig, ax = plt.subplots(figsize=(10, 7), facecolor=BG)
ax.set_facecolor(BG)
ax.axis("off")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# ── Title ──────────────────────────────────────────────────────────────────
fig.text(0.5, 0.93, "St. John's CMA — Rental Market Summary  (2018–2025)",
         ha="center", va="center", fontsize=14, fontweight="bold",
         color=TEXT_HI)
fig.text(0.5, 0.885, "2BR Average Rent & Vacancy Rate with Year-over-Year Change",
         ha="center", va="center", fontsize=9, color=TEXT_MID)

# ── Header row ─────────────────────────────────────────────────────────────
hdr_y = TOP_Y
ax.add_patch(mpatches.FancyBboxPatch(
    (0.02, hdr_y - HDR_H * 0.5), 0.96, HDR_H,
    boxstyle="round,pad=0.005", linewidth=0,
    facecolor=HDR_BG, zorder=1))

for x, hdr in zip(COL_X, HEADERS):
    ax.text(x + 0.01, hdr_y + 0.005, hdr,
            ha="left", va="center", fontsize=9.5,
            fontweight="bold", color=TEXT_MID, zorder=2)

# Divider under header
ax.axhline(hdr_y - HDR_H * 0.52, xmin=0.02, xmax=0.98,
           color=FLAT_C, lw=1.2, alpha=0.6)

# ── Data rows ──────────────────────────────────────────────────────────────
for i, row in enumerate(rows):
    y = TOP_Y - HDR_H * 0.6 - (i + 0.5) * ROW_H

    # Alternating row bg
    row_bg = ALT_ROW if i % 2 == 0 else PANEL
    ax.add_patch(mpatches.FancyBboxPatch(
        (0.02, y - ROW_H * 0.5), 0.96, ROW_H,
        boxstyle="square,pad=0", linewidth=0,
        facecolor=row_bg, zorder=1))

    # Phase dot indicator
    phase_col = FLAT_C if int(row["year"]) <= 2021 else RISE_C
    ax.plot(0.015, y, "o", color=phase_col, ms=5, zorder=3)

    # Year
    ax.text(COL_X[0] + 0.01, y, row["year"],
            ha="left", va="center", fontsize=10,
            fontweight="bold", color=TEXT_HI, zorder=2)

    # Rent
    ax.text(COL_X[1] + 0.01, y, row["rent"],
            ha="left", va="center", fontsize=10,
            color=TEXT_HI, zorder=2)

    # Rent change (coloured)
    ax.text(COL_X[2] + 0.01, y, row["rent_chg"],
            ha="left", va="center", fontsize=9.5,
            color=row["rent_chg_col"], fontweight="bold", zorder=2)

    # Vacancy
    ax.text(COL_X[3] + 0.01, y, row["vac"],
            ha="left", va="center", fontsize=10,
            color=TEXT_HI, zorder=2)

    # Vacancy change (coloured)
    ax.text(COL_X[4] + 0.01, y, row["vac_chg"],
            ha="left", va="center", fontsize=9.5,
            color=row["vac_chg_col"], fontweight="bold", zorder=2)

    # Row divider
    ax.axhline(y - ROW_H * 0.5, xmin=0.02, xmax=0.98,
               color=BORDER, lw=0.5, alpha=0.6)

# ── Legend ─────────────────────────────────────────────────────────────────
legend_y = TOP_Y - HDR_H * 0.6 - (len(rows) + 0.8) * ROW_H
ax.plot(0.04, legend_y, "o", color=FLAT_C, ms=6)
ax.text(0.06, legend_y, "Stagnation phase (2018–2021)",
        va="center", fontsize=8, color=TEXT_MID)
ax.plot(0.38, legend_y, "o", color=RISE_C, ms=6)
ax.text(0.40, legend_y, "Acceleration phase (2022–2025)",
        va="center", fontsize=8, color=TEXT_MID)

# ── Note ───────────────────────────────────────────────────────────────────
note_y = legend_y - ROW_H * 0.9
ax.text(0.04, note_y,
        "▲ = increase from prior year   ▼ = decrease from prior year   "
        "Vacancy change shown in percentage points (pp)",
        va="center", fontsize=7.5, color=TEXT_MID, style="italic")

plt.tight_layout()
plt.savefig("rent_table.png", dpi=150, bbox_inches="tight", facecolor=BG)
print("Saved: rent_table.png")
