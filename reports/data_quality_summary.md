# Data Quality Summary Report (Day 1 - Ingestion)

Generated on: 2026-06-21

## 1. Overview of Datasets

| Dataset Filename | Description | Row Count | Column Count | Null Values Found |
| :--- | :--- | :--- | :--- | :--- |
| 01_fund_master.csv | Fund Master | 40 | 15 | None |
| 02_nav_history.csv | NAV History | 46000 | 3 | None |
| 03_aum_by_fund_house.csv | AUM by Fund House | 90 | 5 | None |
| 04_monthly_sip_inflows.csv | Monthly SIP Inflows | 48 | 6 | 12 (yoy_growth_pct: 12) |
| 05_category_inflows.csv | Category Inflows | 144 | 3 | None |
| 06_industry_folio_count.csv | Industry Folio Count | 21 | 6 | None |
| 07_scheme_performance.csv | Scheme Performance | 40 | 19 | None |
| 08_investor_transactions.csv | Investor Transactions | 32778 | 13 | None |
| 09_portfolio_holdings.csv | Portfolio Holdings | 322 | 8 | None |
| 10_benchmark_indices.csv | Benchmark Indices | 8050 | 3 | None |

## 2. Identified Anomalies & Notes

- **04_monthly_sip_inflows.csv**: Column `yoy_growth_pct` contains 12 null values (likely due to first year of data having no comparison baseline).

## 3. AMFI Code Validation Analysis

- **Total Unique Schemes in Fund Master:** 40
- **Total Unique Schemes in NAV History:** 40
- ✅ **All AMFI codes in Fund Master have historical NAV entries in NAV History.**

## 4. Fund Master Exploration Summary

- **Fund Houses:** 10 unique fund houses
- **Categories:** 2 unique categories (Equity, Debt)
- **Sub-Categories:** 12 unique sub-categories
- **Risk Categories:** 5 levels (Moderate, Very High, Low, High, Moderately High)
