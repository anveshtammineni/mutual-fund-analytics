# Bluestock Mutual Fund Analytics — Data Dictionary (Day 2)

This document provides a comprehensive schema description for the SQLite database `bluestock_mf.db` populated on Day 2 of the Capstone project.

---

## 1. Dimensional Tables

### `dim_fund`
Stores metadata and configurations for the mutual fund schemes.
- **Source:** Cleaned `01_fund_master.csv`
- **Granularity:** One row per unique AMFI Scheme Code.

| Column Name | Data Type | Key/Constraint | Business Definition / Description |
| :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER | PRIMARY KEY | Association of Mutual Funds in India (AMFI) numeric identifier. |
| `fund_house` | TEXT | NOT NULL | Asset Management Company (AMC) name managing the fund. |
| `scheme_name` | TEXT | NOT NULL | Complete official name of the mutual fund scheme. |
| `category` | TEXT | NOT NULL | Asset category (e.g. Equity, Debt, Hybrid). |
| `sub_category` | TEXT | - | Detailed investment class (e.g. Large Cap, Gilt, Liquid, ELSS). |
| `plan` | TEXT | - | Distribution channel format: `Regular` or `Direct`. |
| `launch_date` | TEXT | - | Inception date of the scheme in `YYYY-MM-DD` format. |
| `benchmark` | TEXT | - | Benchmark index against which the scheme performance is measured. |
| `expense_ratio_pct` | REAL | - | Management fee charged to the fund (clipped to valid range `0.1%` - `2.5%`). |
| `exit_load_pct` | REAL | - | Percentage fee charged if units are redeemed early. |
| `min_sip_amount` | INTEGER | - | Minimum transaction limit for Systemic Investment Plan installments. |
| `min_lumpsum_amount`| INTEGER | - | Minimum transaction limit for single one-off investments. |
| `fund_manager` | TEXT | - | Name of the primary investment professional managing the fund. |
| `risk_category` | TEXT | - | SEBI-defined risk meter label (e.g. Low, Moderate, High, Very High). |
| `sebi_category_code`| TEXT | - | SEBI classification tag (e.g. EC01 for Large Cap Equity). |

### `dim_date`
Centralized date dimension for time-series aggregation.
- **Source:** Programmatically generated from unique calendar dates.
- **Granularity:** One row per unique day.

| Column Name | Data Type | Key/Constraint | Business Definition / Description |
| :--- | :--- | :--- | :--- |
| `date` | TEXT | PRIMARY KEY | Standard date string in `YYYY-MM-DD` format. |
| `year` | INTEGER | NOT NULL | Calendar Year (e.g. 2026). |
| `month` | INTEGER | NOT NULL | Calendar Month index (1 to 12). |
| `day` | INTEGER | NOT NULL | Day of the month (1 to 31). |
| `quarter` | INTEGER | NOT NULL | Calendar Quarter index (1 to 4). |
| `day_of_week` | INTEGER | NOT NULL | Weekday index (0 = Monday, 6 = Sunday). |
| `is_weekend` | INTEGER | NOT NULL | Binary flag: `1` if weekend (Sat/Sun), `0` if weekday. |

---

## 2. Fact Tables

### `fact_nav`
Historical daily Net Asset Value (NAV) per scheme.
- **Source:** Cleaned and calendar-expanded `02_nav_history.csv`
- **Granularity:** One row per scheme per calendar day (including weekends/holidays).

| Column Name | Data Type | Key/Constraint | Business Definition / Description |
| :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER | PRIMARY KEY, FK | References `dim_fund(amfi_code)`. |
| `date` | TEXT | PRIMARY KEY, FK | References `dim_date(date)`. |
| `nav` | REAL | NOT NULL | Net Asset Value (price per unit) forward-filled for holidays. |

### `fact_transactions`
Individual investor transactions database.
- **Source:** Cleaned `08_investor_transactions.csv`
- **Granularity:** One row per transaction event.

| Column Name | Data Type | Key/Constraint | Business Definition / Description |
| :--- | :--- | :--- | :--- |
| `transaction_id` | INTEGER | PRIMARY KEY | Auto-incrementing identifier for transaction tracking. |
| `investor_id` | TEXT | NOT NULL | Unique key representing the individual investor folios. |
| `transaction_date` | TEXT | FK | Date of transaction execution, references `dim_date(date)`. |
| `amfi_code` | INTEGER | FK | Scheme key, references `dim_fund(amfi_code)`. |
| `transaction_type` | TEXT | NOT NULL | Standardized transaction classes: `SIP`, `Lumpsum`, or `Redemption`. |
| `amount_inr` | INTEGER | NOT NULL | Transaction value in Indian Rupees (validated > 0). |
| `state` | TEXT | - | Billing/residence state of the investor. |
| `city` | TEXT | - | Billing/residence city of the investor. |
| `city_tier` | TEXT | - | Geographic demographic group (e.g. Tier 1, Tier 2, Tier 3). |
| `age_group` | TEXT | - | Age bucket of the investor (e.g. 18-30, 31-45, etc.). |
| `gender` | TEXT | - | Gender identity (Male/Female/Other). |
| `annual_income_lakh`| REAL | - | Self-declared investor income (in Lakhs per year). |
| `payment_mode` | TEXT | - | Execution interface (e.g. UPI, Net Banking, Cheque, Mandate). |
| `kyc_status` | TEXT | - | Compliance verification flag: `Verified` or `Pending`. |

### `fact_performance`
Static metrics indicating fund risk-return ratios.
- **Source:** Cleaned `07_scheme_performance.csv`
- **Granularity:** One row per unique AMFI Scheme Code.

| Column Name | Data Type | Key/Constraint | Business Definition / Description |
| :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER | PRIMARY KEY, FK | References `dim_fund(amfi_code)`. |
| `scheme_name` | TEXT | - | Name of the fund scheme. |
| `fund_house` | TEXT | - | Managing AMC. |
| `category` | TEXT | - | Core category (Equity/Debt). |
| `plan` | TEXT | - | Plan type (Regular/Direct). |
| `return_1yr_pct` | REAL | - | 1-year trailing growth return percentage. |
| `return_3yr_pct` | REAL | - | 3-year annualized trailing growth return percentage. |
| `return_5yr_pct` | REAL | - | 5-year annualized trailing growth return percentage. |
| `benchmark_3yr_pct`| REAL | - | 3-year annualized benchmark index returns. |
| `alpha` | REAL | - | Outperformance metric relative to the benchmark. |
| `beta` | REAL | - | Volatility sensitivity index relative to the benchmark. |
| `sharpe_ratio` | REAL | - | Risk-adjusted return ratio relative to risk-free rates. |
| `sortino_ratio` | REAL | - | Downside risk-adjusted return ratio. |
| `std_dev_ann_pct` | REAL | - | Annualized standard deviation indicating volatility. |
| `max_drawdown_pct` | REAL | - | Peak-to-trough maximum drop value percentage. |
| `aum_crore` | INTEGER | - | Assets Under Management in Crores. |
| `expense_ratio_pct`| REAL | - | Operating fees percentage. |
| `morningstar_rating`| INTEGER | - | Morningstar star rating (1 to 5). |
| `risk_grade` | TEXT | - | Volatility indicator score grade. |

### `fact_aum`
Historical Assets Under Management by fund house.
- **Source:** Cleaned `03_aum_by_fund_house.csv`
- **Granularity:** One row per AMC per quarter.

| Column Name | Data Type | Key/Constraint | Business Definition / Description |
| :--- | :--- | :--- | :--- |
| `aum_id` | INTEGER | PRIMARY KEY | Auto-incrementing identifier. |
| `date` | TEXT | FK | Quarter-end date, references `dim_date(date)`. |
| `fund_house` | TEXT | NOT NULL | AMC name. |
| `aum_lakh_crore` | REAL | - | Assets Under Management in Lakh Crores. |
| `aum_crore` | INTEGER | - | Assets Under Management in Crores. |
| `num_schemes` | INTEGER | - | Total count of active schemes offered by the AMC. |

### `fact_sip_inflows`
Industry-wide monthly SIP inflows and active accounts.
- **Source:** Cleaned `04_monthly_sip_inflows.csv`
- **Granularity:** One row per calendar month.

| Column Name | Data Type | Key/Constraint | Business Definition / Description |
| :--- | :--- | :--- | :--- |
| `month` | TEXT | PRIMARY KEY | Month of record in `YYYY-MM` format. |
| `sip_inflow_crore` | INTEGER | - | Total monthly industry SIP contribution in Crores. |
| `active_sip_accounts_crore` | REAL | - | Count of active SIP accounts nationwide (in Crores). |
| `new_sip_accounts_lakh` | REAL | - | Count of new SIP accounts registered that month (in Lakhs). |
| `sip_aum_lakh_crore` | REAL | - | Aggregate Assets Under Management linked to SIPs (in Lakh Crores). |
| `yoy_growth_pct` | REAL | - | Year-over-Year inflow percentage growth rate. |

### `fact_category_inflows`
Monthly net capital inflows divided by fund category.
- **Source:** Cleaned `05_category_inflows.csv`
- **Granularity:** One row per category per month.

| Column Name | Data Type | Key/Constraint | Business Definition / Description |
| :--- | :--- | :--- | :--- |
| `month` | TEXT | PRIMARY KEY | Month of record in `YYYY-MM` format. |
| `category` | TEXT | PRIMARY KEY | Fund category (e.g. Large Cap, Mid Cap, Small Cap). |
| `net_inflow_crore` | REAL | - | Net capital inflow (invested - redeemed) in Crores. |

### `fact_industry_folios`
Monthly aggregate industry folio metrics.
- **Source:** Cleaned `06_industry_folio_count.csv`
- **Granularity:** One row per month.

| Column Name | Data Type | Key/Constraint | Business Definition / Description |
| :--- | :--- | :--- | :--- |
| `month` | TEXT | PRIMARY KEY | Month of record in `YYYY-MM` format. |
| `total_folios_crore` | REAL | - | Combined number of active customer folios (in Crores). |
| `equity_folios_crore` | REAL | - | Equity portfolio folios count (in Crores). |
| `debt_folios_crore` | REAL | - | Debt portfolio folios count (in Crores). |
| `hybrid_folios_crore` | REAL | - | Hybrid portfolio folios count (in Crores). |
| `others_folios_crore` | REAL | - | Other category folios count (in Crores). |

### `fact_portfolio_holdings`
Stock holdings breakdown per mutual fund scheme.
- **Source:** Cleaned `09_portfolio_holdings.csv`
- **Granularity:** One row per stock held per scheme.

| Column Name | Data Type | Key/Constraint | Business Definition / Description |
| :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER | PRIMARY KEY, FK | References `dim_fund(amfi_code)`. |
| `stock_symbol` | TEXT | PRIMARY KEY | Stock market ticket symbol (e.g. HDFCBANK). |
| `stock_name` | TEXT | - | Name of company. |
| `sector` | TEXT | - | Industry sector (e.g. Banking, Utilities, IT). |
| `weight_pct` | REAL | - | Portfolio allocation percentage of the stock in the fund. |
| `market_value_cr` | REAL | - | Market value of holding in Crores. |
| `current_price_inr` | REAL | - | Current trade price of stock in Rupees. |
| `portfolio_date` | TEXT | FK | Date of holding snapshot, references `dim_date(date)`. |

### `fact_benchmark_indices`
Historical tracking indices prices.
- **Source:** Cleaned `10_benchmark_indices.csv`
- **Granularity:** One row per index per day.

| Column Name | Data Type | Key/Constraint | Business Definition / Description |
| :--- | :--- | :--- | :--- |
| `date` | TEXT | PRIMARY KEY, FK | References `dim_date(date)`. |
| `index_name` | TEXT | PRIMARY KEY | Tracking index code (e.g. NIFTY50, BSE_SENSEX). |
| `close_value` | REAL | - | EOD closing point index value. |
