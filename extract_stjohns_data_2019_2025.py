import pandas as pd
import numpy as np
import glob
import re

SHEET = "Table 1.0"

# ---------------------------------------------------------------------------
# Column layout (same as before)
# ---------------------------------------------------------------------------
COL_DATE1       = 1
COL_DATE2       = 3
COL_VAC1        = 1
COL_VAC2        = 3
COL_TURN1       = 6
COL_TURN2       = 8
COL_RENT1       = 11
COL_RENT2       = 13
HEADER_ROW      = 6
DATA_START_ROW  = 7

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def clean_num(val):
    if val is None:
        return np.nan
    s = str(val).replace(",", "").strip()
    try:
        return float(s)
    except ValueError:
        return np.nan

def fmt_tuple(v1, v2):
    s1 = str(v1) if not (isinstance(v1, float) and np.isnan(v1)) else "N/A"
    s2 = str(v2) if not (isinstance(v2, float) and np.isnan(v2)) else "N/A"
    return f"{s1}:{s2}"

def extract_year(filename):
    match = re.search(r'(\d{4})', filename)
    return int(match.group(1)) if match else None

# ---------------------------------------------------------------------------
# Get all files (make sure names contain year like rmr-canada-2023-en.xlsx)
# ---------------------------------------------------------------------------
files = glob.glob("rmr-canada-*.xlsx")

all_records = []

for file in files:
    YEAR = extract_year(file)
    if YEAR is None or YEAR < 2019 or YEAR > 2025:
        continue

    df = pd.read_excel(file, sheet_name=SHEET, header=None)

    header = df.iloc[HEADER_ROW]
    date1 = str(header[COL_DATE1]).strip()
    date2 = str(header[COL_DATE2]).strip()

    for i in range(DATA_START_ROW, len(df)):
        region = str(df.iloc[i, 0]).strip()
        if not region or region in ("nan", "NaN") or region.startswith("Source"):
            continue
        if "10,000+" in region:
            continue

        v1  = clean_num(df.iloc[i, COL_VAC1])
        v2  = clean_num(df.iloc[i, COL_VAC2])
        t1  = clean_num(df.iloc[i, COL_TURN1])
        t2  = clean_num(df.iloc[i, COL_TURN2])
        r1  = clean_num(df.iloc[i, COL_RENT1])
        r2  = clean_num(df.iloc[i, COL_RENT2])

        all_records.append({
            "Region":       region,
            "VacancyRate":  fmt_tuple(v1, v2),
            "TurnoverRate": fmt_tuple(t1, t2),
            "Rent2BR":      fmt_tuple(r1, r2),
            "Year":         YEAR,
            "_vac1": v1, "_vac2": v2,
            "_turn1": t1, "_turn2": t2,
            "_rent1": r1, "_rent2": r2,
        })

# ---------------------------------------------------------------------------
# Final dataset
# ---------------------------------------------------------------------------
full_df = pd.DataFrame(all_records)

display_cols = ["Region", "VacancyRate", "TurnoverRate", "Rent2BR", "Year"]
rental_df = full_df[display_cols]

#rental_df.to_csv("rental_data_all_years.csv", index=False)

# Filter St. John's across years
stj = rental_df[rental_df["Region"].str.contains("John's", case=False)]
# Save ONLY St. John's data
stj.to_csv("rental_data_stjohns_2019_2025.csv", index=False)
print(stj.to_string(index=False))
