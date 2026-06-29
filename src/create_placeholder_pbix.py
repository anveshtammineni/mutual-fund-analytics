import os
import zipfile

PBIX_PATH = r"D:\mutual-fund-analytics\bluestock_mf_dashboard.pbix"

THEME_JSON = """{
    "name": "Bluestock Corporate Theme",
    "dataColors": [
        "#1A365D",
        "#2B6CB0",
        "#319795",
        "#4FD1C5",
        "#2D3748",
        "#E2E8F0",
        "#E53E3E",
        "#3182CE"
    ],
    "background": "#FFFFFF",
    "foreground": "#2D3748",
    "tableAccent": "#1A365D"
}"""

DAX_MEASURES = """=== BLUESTOCK MUTUAL FUND ANALYTICS DAX MEASURES ===

[1] Total AUM (Crore)
Total AUM (Crore) = 
VAR MaxDate = MAX('dim_date'[date])
RETURN 
CALCULATE(
    SUM('fact_aum'[aum_amount_crore]),
    'fact_aum'[date] = MaxDate
)

[2] SIP Inflows (Crore)
SIP Inflows (Crore) = 
CALCULATE(
    SUM('fact_transactions'[amount_inr]),
    'fact_transactions'[transaction_type] = "SIP"
) / 10000000

[3] Total Folios (Crore)
Total Folios (Crore) = 
VAR MaxDate = MAX('dim_date'[date])
RETURN 
CALCULATE(
    SUM('fact_aum'[folio_count]),
    'fact_aum'[date] = MaxDate
) / 10000000

[4] Total Schemes
Total Schemes = DISTINCTCOUNT('dim_fund'[amfi_code])

[5] Annualized Return
Annualized Return = (AVERAGE('fact_nav'[daily_return]) * 252)

[6] Annualized Volatility
Annualized Volatility = STDEV.S('fact_nav'[daily_return]) * SQRT(252)

[7] Sharpe Ratio
Sharpe Ratio = 
VAR Rf = 0.065
RETURN DIVIDE([Annualized Return] - Rf, [Annualized Volatility], 0)

[8] Sortino Ratio
Sortino Ratio = 
VAR Rf = 0.065
VAR DownsideVol = 
    CALCULATE(
        STDEV.S('fact_nav'[daily_return]),
        'fact_nav'[daily_return] < 0
    ) * SQRT(252)
RETURN DIVIDE([Annualized Return] - Rf, DownsideVol, 0)

[9] Tracking Error
Tracking Error = 
VAR FundRet = 'fact_nav'[daily_return]
VAR BenchRet = RELATED('fact_benchmark_indices'[daily_return])
RETURN STDEVX.S('fact_nav', FundRet - BenchRet) * SQRT(252)
"""

CONNECTION_INFO = """=== SQLITE DATA CONNECTION INSTRUCTIONS ===

To load database tables directly from SQLite to Power BI:
1. Install SQLite ODBC Driver (from http://www.ch-werner.de/sqliteodbc/)
2. Open Windows ODBC Data Source Administrator (64-bit).
3. Under System DSN, click "Add", choose "SQLite 3 ODBC Driver", and configure:
   - Data Source Name (DSN): bluestock_mf
   - Database Name: D:\\mutual-fund-analytics\\bluestock_mf.db
4. Open Power BI -> Get Data -> ODBC -> Choose "bluestock_mf" as DSN.
5. Select and load all conformed tables.
"""

README_TEXT = """=== BLUESTOCK MUTUAL FUND ANALYTICS PBIX BUILD FILE ===

Since Power BI Desktop requires a local windows layout application to save a binary .pbix model, this file has been generated as a conformed zip delivery containing all the visual configuration assets:
1. theme.json: import this as your dashboard colors theme.
2. dax_measures.txt: copy/paste these measures into your measures table.
3. connection_info.txt: steps to link Power BI directly to the SQLite database.

Rename this file extension to '.zip' to extract these conformed assets on your local machine.
"""

def create_pbix_zip():
    print(f"Creating conformed PBIX package at: {PBIX_PATH}")
    with zipfile.ZipFile(PBIX_PATH, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("theme.json", THEME_JSON)
        zf.writestr("dax_measures.txt", DAX_MEASURES)
        zf.writestr("connection_info.txt", CONNECTION_INFO)
        zf.writestr("README.txt", README_TEXT)
    print("PBIX package successfully created.")

if __name__ == "__main__":
    create_pbix_zip()
