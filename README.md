## Rental-Housing-Prices-in-Newfoundland-and-Labrador
# St. John's CMA Rental Market Analysis (2018–2025)

Interrupted Time Series (ITS) analysis of 2BR rents and vacancy rates in St. John's, Newfoundland and Labrador.  
Examines the impact of the 2019 Residential Tenancies Act.

## Project Overview
- **Goal**: Visual analysis of rent stagnation (2018–2021) followed by acceleration (2022–2025).
- **Methods**: Interrupted Time Series regression.
- **Languages**: Python (main demo version) + original R code.

## How to Reproduce the Analysis

### 1. Python Version (Recommended for visuals)
```bash
git clone https://github.com/yourusername/rental-housing-nl-stjohns.git
cd rental-housing-nl-stjohns

# Install dependencies
pip install -r python/requirements.txt

# Run the analysis
cd python
python its_analysis.py
# or open its_analysis.ipynb in Jupyter
