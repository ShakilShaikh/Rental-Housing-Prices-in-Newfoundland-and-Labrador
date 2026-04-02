# process_rent_data.py

import pandas as pd
import numpy as np

INPUT_FILE = "rental_data.csv"
OUTPUT_FILE = "output.csv"

def parse_range(value):
    """Convert 'x:y' → [x, y] as floats"""
    try:
        parts = str(value).split(":")
        return [float(p) for p in parts]
    except:
        return [np.nan]

def compute_stats(range_str):
    values = parse_range(range_str)
    mean = np.mean(values)
    std = np.std(values, ddof=1) if len(values) > 1 else 0

    return round(mean, 2), round(std, 2)

def process_data(file_path):
    df = pd.read_csv(file_path)

    results = []

    for _, row in df.iterrows():
        rent_mean, rent_std = compute_stats(row["Rent2BR"])
        vac_mean, vac_std = compute_stats(row["VacancyRate"])
        turn_mean, turn_std = compute_stats(row["TurnoverRate"])

        results.append({
            "Region": row["Region"],
            "Rent2BR_mean": rent_mean,
            "Rent2BR_std": rent_std,
            "VacancyRate_mean": vac_mean,
            "VacancyRate_std": vac_std,
            "TurnoverRate_mean": turn_mean,
            "TurnoverRate_std": turn_std,
            "Year": row["Year"]
        })

    return pd.DataFrame(results)

if __name__ == "__main__":
    output_df = process_data(INPUT_FILE)

    print("\nProcessed Data:")
    print(output_df)

    output_df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved to {OUTPUT_FILE}")


[print("(%s,%s,%s),\n"%(output_df["Year"][i],output_df["VacancyRate_mean"][i],output_df["Rent2BR_mean"][i])) for i in range(8)]
