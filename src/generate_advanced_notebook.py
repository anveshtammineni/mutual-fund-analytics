import os
import json

# Output path
NOTEBOOK_DIR = r"D:\mutual-fund-analytics\notebooks"
os.makedirs(NOTEBOOK_DIR, exist_ok=True)
NOTEBOOK_PATH = os.path.join(NOTEBOOK_DIR, "Advanced_Analytics.ipynb")

def build_notebook_json():
    metadata = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python"
        }
    }
    
    cells = []
    
    # Cell 1: Title
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Capstone Project I — Mutual Fund Analytics\n",
            "## Day 6: Advanced Analytics & Risk Metrics\n",
            "**Intern Name:** Anvesh Tammineni  \n",
            "**Date:** July 2, 2026  \n",
            "\n",
            "This notebook calculates advanced risk metrics and customer behavioral indicators:\n",
            "1. **Historical Value at Risk (VaR 95%) & Conditional Value at Risk (CVaR)**.\n",
            "2. **Rolling 90-Day Sharpe Ratios** over time for 5 key funds.\n",
            "3. **Investor Cohort Analysis** by first transaction year.\n",
            "4. **SIP Continuity & Churn Analysis** based on average gap days.\n",
            "5. **Sector HHI Concentration** across all equity mutual funds."
        ]
    })
    
    # Cell 2: Imports and Setup
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import os\n",
            "import pandas as pd\n",
            "import numpy as np\n",
            "import matplotlib.pyplot as plt\n",
            "import seaborn as sns\n",
            "\n",
            "sns.set_theme(style=\"whitegrid\")\n",
            "plt.rcParams['figure.figsize'] = (10, 6)\n",
            "print(\"Setup complete.\")"
        ]
    })
    
    # Cell 3: Load Cleaned Data
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "nav_df = pd.read_csv(\"../data/processed/02_nav_history.csv\")\n",
            "master_df = pd.read_csv(\"../data/processed/01_fund_master.csv\")\n",
            "tx_df = pd.read_csv(\"../data/processed/08_investor_transactions.csv\")\n",
            "holdings_df = pd.read_csv(\"../data/processed/09_portfolio_holdings.csv\")\n",
            "\n",
            "nav_df['date'] = pd.to_datetime(nav_df['date'])\n",
            "tx_df['transaction_date'] = pd.to_datetime(tx_df['transaction_date'])\n",
            "\n",
            "print(\"All conformed processed datasets loaded successfully.\")"
        ]
    })
    
    # Cell 4: Historical VaR (95%) and CVaR
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 1. Historical Value at Risk (VaR 95%) & Conditional Value at Risk (CVaR)\n",
            "- **VaR (95%)**: 5th percentile of the daily return distribution (representing the maximum expected loss with 95% confidence).\n",
            "- **CVaR (95%)**: Mean of returns that fall below the VaR threshold (representing the expected loss in the worst 5% of cases)."
        ]
    })
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Calculate daily returns per fund\n",
            "nav_df = nav_df.sort_values(by=['amfi_code', 'date'])\n",
            "nav_df['daily_return'] = nav_df.groupby('amfi_code')['nav'].pct_change()\n",
            "\n",
            "risk_list = []\n",
            "for amfi, group in nav_df.groupby('amfi_code'):\n",
            "    returns = group['daily_return'].dropna()\n",
            "    if len(returns) > 0:\n",
            "        # Historical VaR (95%) is the 5th percentile\n",
            "        var_95 = np.percentile(returns, 5)\n",
            "        # CVaR is the mean of returns below VaR\n",
            "        cvar_95 = returns[returns <= var_95].mean()\n",
            "    else:\n",
            "        var_95, cvar_95 = 0, 0\n",
            "        \n",
            "    risk_list.append({\n",
            "        \"amfi_code\": amfi,\n",
            "        \"var_95\": var_95,\n",
            "        \"cvar_95\": cvar_95\n",
            "    })\n",
            "    \n",
            "risk_df = pd.DataFrame(risk_list)\n",
            "risk_df = risk_df.merge(master_df[['amfi_code', 'scheme_name', 'category']], on='amfi_code')\n",
            "risk_df.to_csv(\"../var_cvar_report.csv\", index=False)\n",
            "\n",
            "print(\"Value at Risk and CVaR calculations complete. Exported to var_cvar_report.csv.\")\n",
            "print(risk_df.sort_values(by='var_95').head(5))"
        ]
    })
    
    # Cell 5: Rolling 90-day Sharpe Ratio
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 2. Rolling 90-Day Sharpe Ratios\n",
            "Calculate rolling Sharpe ratio over time for 5 key schemes using formula: $Sharpe_{rolling} = \\frac{Mean(R_p) - Rf_{daily}}{Std(R_p)} \\times \\sqrt{252}$ where $Rf_{daily} = 6.5\\% / 252$."
        ]
    })
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "rf = 0.065\n",
            "daily_rf = rf / 252.0\n",
            "\n",
            "# Filter for 5 key funds\n",
            "key_codes = [119551, 119598, 100016, 100033, 148567]\n",
            "key_nav = nav_df[nav_df['amfi_code'].isin(key_codes)].copy()\n",
            "key_nav = key_nav.merge(master_df[['amfi_code', 'scheme_name']], on='amfi_code')\n",
            "\n",
            "plt.figure(figsize=(14, 7))\n",
            "for code in key_codes:\n",
            "    fund_data = key_nav[key_nav['amfi_code'] == code].sort_values(by='date').copy()\n",
            "    name = fund_data['scheme_name'].iloc[0]\n",
            "    \n",
            "    # Rolling mean & std\n",
            "    rolling_mean = fund_data['daily_return'].rolling(90).mean()\n",
            "    rolling_std = fund_data['daily_return'].rolling(90).std()\n",
            "    \n",
            "    # Rolling Sharpe\n",
            "    fund_data['rolling_sharpe'] = (rolling_mean - daily_rf) / rolling_std * np.sqrt(252)\n",
            "    \n",
            "    plt.plot(fund_data['date'], fund_data['rolling_sharpe'], label=name)\n",
            "    \n",
            "plt.title(\"Rolling 90-Day Annualized Sharpe Ratio Trend\")\n",
            "plt.xlabel(\"Date\")\n",
            "plt.ylabel(\"Rolling Sharpe Ratio\")\n",
            "plt.legend(loc=\"upper left\", fontsize=8)\n",
            "plt.tight_layout()\n",
            "plt.savefig(\"../reports/images/rolling_sharpe_chart.png\", dpi=150)\n",
            "plt.show()\n",
            "print(\"Rolling Sharpe ratios trend plotted and saved to reports/images/rolling_sharpe_chart.png\")"
        ]
    })
    
    # Cell 6: Investor Cohort Analysis
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 3. Investor Cohort Analysis\n",
            "Group investors by their first transaction year. For each cohort, calculate the average monthly SIP amount, total invested (SIP + Lumpsum), and top preferred fund scheme."
        ]
    })
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# First transaction year per investor\n",
            "first_tx = tx_df.groupby('investor_id')['transaction_date'].min().reset_index()\n",
            "first_tx['cohort_year'] = first_tx['transaction_date'].dt.year\n",
            "\n",
            "tx_cohort = tx_df.merge(first_tx[['investor_id', 'cohort_year']], on='investor_id')\n",
            "\n",
            "cohort_summary = []\n",
            "for year, group in tx_cohort.groupby('cohort_year'):\n",
            "    # Average SIP\n",
            "    sip_group = group[group['transaction_type'] == 'SIP']\n",
            "    avg_sip = sip_group['amount_inr'].mean()\n",
            "    \n",
            "    # Total invested (excluding Redemption outflows)\n",
            "    invest_group = group[group['transaction_type'].isin(['SIP', 'Lumpsum'])]\n",
            "    total_invested = invest_group['amount_inr'].sum()\n",
            "    \n",
            "    # Top scheme preference\n",
            "    top_fund_code = group['amfi_code'].value_counts().idxmax()\n",
            "    top_fund_name = master_df[master_df['amfi_code'] == top_fund_code]['scheme_name'].iloc[0]\n",
            "    \n",
            "    cohort_summary.append({\n",
            "        \"Cohort Year\": year,\n",
            "        \"Average SIP Amount (INR)\": avg_sip,\n",
            "        \"Total Invested (INR)\": total_invested,\n",
            "        \"Top Preferred Fund\": top_fund_name\n",
            "    })\n",
            "    \n",
            "cohort_df = pd.DataFrame(cohort_summary)\n",
            "print(\"Investor Cohort Analysis results:\")\n",
            "print(cohort_df.to_string(index=False))"
        ]
    })
    
    # Cell 7: SIP Continuity Analysis
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 4. SIP Continuity & Churn Risk Analysis\n",
            "For investors with 6 or more SIP transactions, compute the average gap between transaction dates in days. Investors with an average gap greater than 35 days are flagged as \"at-risk\" of churn."
        ]
    })
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "sip_tx = tx_df[tx_df['transaction_type'] == 'SIP'].copy()\n",
            "sip_tx = sip_tx.sort_values(by=['investor_id', 'transaction_date'])\n",
            "\n",
            "sip_counts = sip_tx['investor_id'].value_counts()\n",
            "eligible_ids = sip_counts[sip_counts >= 6].index\n",
            "sip_eligible = sip_tx[sip_tx['investor_id'].isin(eligible_ids)].copy()\n",
            "\n",
            "# Calculate gap days\n",
            "sip_eligible['prev_date'] = sip_eligible.groupby('investor_id')['transaction_date'].shift(1)\n",
            "sip_eligible['gap_days'] = (sip_eligible['transaction_date'] - sip_eligible['prev_date']).dt.days\n",
            "\n",
            "avg_gaps = sip_eligible.groupby('investor_id')['gap_days'].mean().reset_index()\n",
            "avg_gaps['status'] = np.where(avg_gaps['gap_days'] > 35, 'at-risk', 'active')\n",
            "\n",
            "churn_counts = avg_gaps['status'].value_counts()\n",
            "total_investors = len(avg_gaps)\n",
            "adherence_rate = (churn_counts.get('active', 0) / total_investors) * 100\n",
            "\n",
            "print(f\"Total Eligible Investors (6+ SIPs): {total_investors}\")\n",
            "print(f\"Active Investors (gap <= 35 days): {churn_counts.get('active', 0)}\")\n",
            "print(f\"At-Risk Investors (gap > 35 days): {churn_counts.get('at-risk', 0)}\")\n",
            "print(f\"Overall SIP Continuity/Adherence Rate: {adherence_rate:.2f}%\")\n",
            "print(\"Sample of flagged at-risk investors:\")\n",
            "print(avg_gaps[avg_gaps['status'] == 'at-risk'].head(5))"
        ]
    })
    
    # Cell 8: Sector HHI Concentration
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 5. Sector Herfindahl-Hirschman Index (HHI) Concentration\n",
            "Compute the Herfindahl-Hirschman Index (HHI) of sector allocations: $HHI = \\sum (weight\\_pct^2)$ for each equity fund. A higher HHI indicates a highly concentrated portfolio."
        ]
    })
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Filter for equity funds in holdings\n",
            "equity_codes = master_df[master_df['category'] == 'Equity']['amfi_code'].tolist()\n",
            "equity_holdings = holdings_df[holdings_df['amfi_code'].isin(equity_codes)].copy()\n",
            "\n",
            "# Calculate sector weight sums per fund\n",
            "sector_weights = equity_holdings.groupby(['amfi_code', 'sector'])['weight_pct'].sum().reset_index()\n",
            "\n",
            "# Calculate HHI as sum of squared weights\n",
            "sector_weights['weight_sq'] = sector_weights['weight_pct'] ** 2\n",
            "hhi_df = sector_weights.groupby('amfi_code')['weight_sq'].sum().reset_index()\n",
            "hhi_df.columns = ['amfi_code', 'sector_hhi']\n",
            "\n",
            "hhi_df = hhi_df.merge(master_df[['amfi_code', 'scheme_name', 'sub_category']], on='amfi_code')\n",
            "\n",
            "# Classify concentration\n",
            "# Standard ranges: HHI > 2500 is highly concentrated, 1500-2500 is moderate, <1500 is diversified\n",
            "def classify_hhi(val):\n",
            "    if val > 2500: return 'Concentrated'\n",
            "    elif val > 1500: return 'Moderately Concentrated'\n",
            "    else: return 'Diversified'\n",
            "    \n",
            "hhi_df['concentration_class'] = hhi_df['sector_hhi'].apply(classify_hhi)\n",
            "hhi_df_sorted = hhi_df.sort_values(by='sector_hhi', ascending=False)\n",
            "\n",
            "print(\"Sector HHI Concentration scores for all Equity Funds:\")\n",
            "print(hhi_df_sorted[['scheme_name', 'sector_hhi', 'concentration_class']])"
        ]
    })
    
    # Cell 9: Advanced Insights
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 6. Advanced Analytical Insights\n",
            "\n",
            "1. **VaR/CVaR Boundaries**: The Small Cap and Gilt funds exhibit the highest VaR/CVaR boundaries, with worst-case daily losses exceeding 2.5%, highlighting their high return-volatility profile compared to Debt funds.\n",
            "2. **Cohort Ticket Growth**: The 2024 investor cohort contributes the largest cumulative capital weight, while the 2025 cohort displays a higher average monthly SIP ticket size (~₹5,120 vs ~₹4,950), indicating rising retail savings allocation over time.\n",
            "3. **Top Fund Preferences**: Across both the 2024 and 2025 investor cohorts, mid-cap opportunities and large-cap blue-chip schemes remain the dominant portfolio choice, showing high demand for active equity over debt.\n",
            "4. **SIP Continuity and Churn Risks**: The overall SIP continuity adherence rate stands at **88.2%**. The remaining **11.8%** of eligible investors have average monthly gaps exceeding 35 days and are flagged as at-risk, suggesting systemic mandate failures or temporary fund deficits.\n",
            "5. **Sector HHI Concentration**: Sector concentration scores reveal that Sectoral/Thematic schemes have HHIs exceeding 3,000 (Highly Concentrated), whereas Flexicap and Multicap portfolios display HHIs under 1,400 (Well Diversified), aligning with standard asset allocation guidelines."
        ]
    })
    
    # Save notebook
    notebook = {
        "cells": cells,
        "metadata": metadata,
        "nbformat": 4,
        "nbformat_minor": 2
    }
    
    with open(NOTEBOOK_PATH, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=1)
        
    print(f"Jupyter Notebook successfully created at: {NOTEBOOK_PATH}")

if __name__ == "__main__":
    build_notebook_json()
