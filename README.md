# Mutual Fund Analytics

Day 1 ETL setup and data ingestion pipeline for the Mutual Fund Analytics project.

## Directory Structure
```text
mutual-fund-analytics/
├── data/
│   ├── raw/                 # Contains 10 raw CSV datasets and live NAVs
│   └── processed/
├── notebooks/
├── sql/
├── dashboard/
├── reports/
│   └── data_quality_summary.md  # Detailed data quality report
├── src/
│   ├── data_ingestion.py    # Dataset audit and validation script
│   └── live_nav_fetch.py    # Script to fetch live NAVs from mfapi.in
└── requirements.txt         # Dependencies and short data quality summary
```

## Data Quality Summary

### 1. Dataset Audits
| Dataset Filename | Description | Row Count | Column Count | Null Values Found |
| :--- | :--- | :--- | :--- | :--- |
| `01_fund_master.csv` | Fund Master | 40 | 15 | None |
| `02_nav_history.csv` | NAV History | 46,000 | 3 | None |
| `03_aum_by_fund_house.csv` | AUM by Fund House | 90 | 5 | None |
| `04_monthly_sip_inflows.csv` | Monthly SIP Inflows | 48 | 6 | 12 (`yoy_growth_pct`) |
| `05_category_inflows.csv` | Category Inflows | 144 | 3 | None |
| `06_industry_folio_count.csv` | Industry Folio Count | 21 | 6 | None |
| `07_scheme_performance.csv` | Scheme Performance | 40 | 19 | None |
| `08_investor_transactions.csv` | Investor Transactions | 32,778 | 13 | None |
| `09_portfolio_holdings.csv` | Portfolio Holdings | 322 | 8 | None |
| `10_benchmark_indices.csv` | Benchmark Indices | 8,050 | 3 | None |

### 2. Identified Anomalies & Notes
- **04_monthly_sip_inflows.csv**: Column `yoy_growth_pct` contains 12 null values. This is not a data corruption issue but a baseline omission: the first 12 months do not have historical data from the prior year to calculate YoY growth.

### 3. AMFI Code Validation Analysis
- **Total Unique Schemes in Fund Master**: 40
- **Total Unique Schemes in NAV History**: 40
- **Validation Status**: **100% Match** (All AMFI codes in `01_fund_master.csv` have historical entries in `02_nav_history.csv`).

---

## Getting Started
To install the dependencies and run the scripts:

```bash
pip install -r requirements.txt
python src/data_ingestion.py
python src/live_nav_fetch.py
```
