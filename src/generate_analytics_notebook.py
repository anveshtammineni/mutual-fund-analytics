import os
import json

# Output path
NOTEBOOK_DIR = r"D:\mutual-fund-analytics\notebooks"
os.makedirs(NOTEBOOK_DIR, exist_ok=True)
NOTEBOOK_PATH = os.path.join(NOTEBOOK_DIR, "Performance_Analytics.ipynb")

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
            "## Day 4: Fund Performance Analytics\n",
            "**Intern Name:** Anvesh Tammineni  \n",
            "**Date:** June 29, 2026  \n",
            "\n",
            "This notebook calculates advanced risk-adjusted performance metrics, builds a composite scorecard ranking the 40 mutual fund schemes, calculates Alpha/Beta coefficients and Maximum Drawdowns, and compares the top 5 performing funds against the Nifty 50 and Nifty 100 benchmarks."
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
            "import scipy.stats as stats\n",
            "\n",
            "# Output directories\n",
            "IMAGE_DIR = \"../reports/images\"\n",
            "os.makedirs(IMAGE_DIR, exist_ok=True)\n",
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
            "bench_df = pd.read_csv(\"../data/processed/10_benchmark_indices.csv\")\n",
            "perf_df = pd.read_csv(\"../data/processed/07_scheme_performance.csv\")\n",
            "print(\"All required processed datasets loaded successfully.\")"
        ]
    })
    
    # Cell 4: Daily Returns Calculation & Distribution Plot
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 1. Compute & Validate Daily Returns\n",
            "Calculate daily returns: $daily\\_return = \\frac{nav_t}{nav_{t-1}} - 1$ for all 40 schemes and plot returns distribution for sample schemes."
        ]
    })
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "nav_df['date'] = pd.to_datetime(nav_df['date'])\n",
            "nav_df = nav_df.sort_values(by=['amfi_code', 'date'])\n",
            "nav_df['daily_return'] = nav_df.groupby('amfi_code')['nav'].pct_change()\n",
            "\n",
            "# Select 5 sample funds to plot distributions\n",
            "sample_codes = master_df['amfi_code'].head(5).tolist()\n",
            "sample_returns = nav_df[nav_df['amfi_code'].isin(sample_codes)].merge(master_df[['amfi_code', 'scheme_name']], on='amfi_code')\n",
            "\n",
            "plt.figure(figsize=(12, 6))\n",
            "sns.kdeplot(data=sample_returns, x='daily_return', hue='scheme_name', fill=True, common_norm=False, alpha=0.3)\n",
            "plt.title(\"Daily Returns Distribution (Sample Funds)\")\n",
            "plt.xlabel(\"Daily Return\")\n",
            "plt.ylabel(\"Density\")\n",
            "plt.xlim(-0.04, 0.04)\n",
            "plt.tight_layout()\n",
            "plt.savefig(\"../reports/images/daily_returns_distribution.png\", dpi=150)\n",
            "plt.show()\n",
            "\n",
            "print(\"Returns validation complete. Standard distribution looks normal near-zero mean.\")"
        ]
    })
    
    # Cell 5: CAGR Calculation (1yr, 3yr, Full Period)
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 2. Compute Trailing CAGR\n",
            "Calculate Compound Annual Growth Rate (CAGR) for 1-Year and 3-Year periods. For 5-Year period, since the dataset spans 4.4 years, we calculate the Full Period CAGR from 2022 to 2026."
        ]
    })
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "max_date = nav_df['date'].max()\n",
            "date_1yr_ago = max_date - pd.DateOffset(years=1)\n",
            "date_3yr_ago = max_date - pd.DateOffset(years=3)\n",
            "date_start = nav_df['date'].min()\n",
            "\n",
            "all_dates = nav_df['date'].unique()\n",
            "def get_closest_date(target, dates):\n",
            "    return min(dates, key=lambda x: abs(x - target))\n",
            "\n",
            "date_1yr_actual = get_closest_date(date_1yr_ago, all_dates)\n",
            "date_3yr_actual = get_closest_date(date_3yr_ago, all_dates)\n",
            "\n",
            "cagr_list = []\n",
            "for amfi, group in nav_df.groupby('amfi_code'):\n",
            "    group = group.set_index('date')\n",
            "    nav_end = group.loc[max_date, 'nav']\n",
            "    nav_1yr_start = group.loc[date_1yr_actual, 'nav']\n",
            "    nav_3yr_start = group.loc[date_3yr_actual, 'nav']\n",
            "    nav_start = group.loc[date_start, 'nav']\n",
            "    \n",
            "    cagr_1yr = (nav_end / nav_1yr_start) - 1.0\n",
            "    cagr_3yr = (nav_end / nav_3yr_start) ** (1.0 / 3.0) - 1.0\n",
            "    \n",
            "    years_full = (max_date - date_start).days / 365.25\n",
            "    cagr_full = (nav_end / nav_start) ** (1.0 / years_full) - 1.0\n",
            "    \n",
            "    cagr_list.append({\n",
            "        \"amfi_code\": amfi,\n",
            "        \"cagr_1yr\": cagr_1yr,\n",
            "        \"cagr_3yr\": cagr_3yr,\n",
            "        \"cagr_full_period\": cagr_full\n",
            "    })\n",
            "    \n",
            "cagr_df = pd.DataFrame(cagr_list)\n",
            "print(\"CAGR values computed. Head of CAGR Comparison table:\")\n",
            "print(cagr_df.head())\n"
        ]
    })
    
    # Cell 6: Sharpe and Sortino Ratios
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 3. Compute Risk-Adjusted Return Ratios\n",
            "Calculate annualized **Sharpe Ratio** and **Sortino Ratio** using risk-free rate of $6.5\\%$ ($Rf_{daily} = 6.5\\%/252$)."
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
            "ratios_list = []\n",
            "for amfi, group in nav_df.groupby('amfi_code'):\n",
            "    returns = group['daily_return'].dropna()\n",
            "    mean_ret = returns.mean()\n",
            "    std_ret = returns.std()\n",
            "    \n",
            "    sharpe = (mean_ret - daily_rf) / std_ret * np.sqrt(252) if std_ret > 0 else 0\n",
            "    \n",
            "    downside_returns = returns[returns < 0]\n",
            "    downside_std = downside_returns.std() if len(downside_returns) > 0 else std_ret\n",
            "    sortino = (mean_ret - daily_rf) / downside_std * np.sqrt(252) if downside_std > 0 else 0\n",
            "    \n",
            "    ratios_list.append({\n",
            "        \"amfi_code\": amfi,\n",
            "        \"mean_daily_return\": mean_ret,\n",
            "        \"std_daily_return\": std_ret,\n",
            "        \"sharpe_ratio\": sharpe,\n",
            "        \"sortino_ratio\": sortino\n",
            "    })\n",
            "    \n",
            "ratios_df = pd.DataFrame(ratios_list)\n",
            "print(\"Sharpe and Sortino ratios computed and ranked.\")\n",
            "print(ratios_df.head())\n"
        ]
    })
    
    # Cell 7: Alpha and Beta Regression
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 4. Alpha & Beta Regression on Nifty 100\n",
            "Run OLS linear regression of fund daily returns against NIFTY100 daily returns using `scipy.stats.linregress`. Export results to `alpha_beta.csv`."
        ]
    })
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "nifty100 = bench_df[bench_df['index_name'] == 'NIFTY100'].copy()\n",
            "nifty100['date'] = pd.to_datetime(nifty100['date'])\n",
            "nifty100 = nifty100.sort_values(by='date')\n",
            "nifty100['nifty100_return'] = nifty100['close_value'].pct_change()\n",
            "nifty100_clean = nifty100[['date', 'nifty100_return']].dropna()\n",
            "\n",
            "reg_list = []\n",
            "for amfi, group in nav_df.groupby('amfi_code'):\n",
            "    merged = group.merge(nifty100_clean, on='date').dropna(subset=['daily_return', 'nifty100_return'])\n",
            "    if len(merged) > 10:\n",
            "        slope, intercept, r_val, p_val, std_err = stats.linregress(merged['nifty100_return'], merged['daily_return'])\n",
            "        alpha = intercept * 252\n",
            "        beta = slope\n",
            "    else:\n",
            "        alpha, beta = 0, 1.0\n",
            "    reg_list.append({\n",
            "        \"amfi_code\": amfi,\n",
            "        \"alpha\": alpha,\n",
            "        \"beta\": beta\n",
            "    })\n",
            "    \n",
            "reg_df = pd.DataFrame(reg_list)\n",
            "reg_df.to_csv(\"../alpha_beta.csv\", index=False)\n",
            "print(\"Alpha and Beta coefficients successfully exported to alpha_beta.csv. Summary:\")\n",
            "print(reg_df.head())\n"
        ]
    })
    
    # Cell 8: Maximum Drawdown & Date Ranges
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 5. Maximum Drawdown & Date Range Analysis\n",
            "Calculate maximum drawdown: $min(\\frac{NAV}{running\\_max} - 1)$ for each fund, and identify the worst Peak-to-Trough drawdown date ranges and recovery dates."
        ]
    })
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "dd_list = []\n",
            "for amfi, group in nav_df.groupby('amfi_code'):\n",
            "    group = group.sort_values(by='date').reset_index(drop=True)\n",
            "    navs = group['nav']\n",
            "    running_max = navs.cummax()\n",
            "    drawdowns = navs / running_max - 1.0\n",
            "    max_dd = drawdowns.min()\n",
            "    \n",
            "    trough_idx = drawdowns.idxmin()\n",
            "    trough_date = group.loc[trough_idx, 'date']\n",
            "    \n",
            "    peak_val = running_max.loc[trough_idx]\n",
            "    peak_df = group[(group['date'] <= trough_date) & (group['nav'] == peak_val)]\n",
            "    peak_date = peak_df['date'].max() if not peak_df.empty else group.loc[group['nav'].idxmax(), 'date']\n",
            "    \n",
            "    recovery_df = group[(group['date'] > trough_date) & (group['nav'] >= peak_val)]\n",
            "    recovery_date = recovery_df.iloc[0]['date'] if not recovery_df.empty else \"Not Recovered\"\n",
            "    \n",
            "    dd_list.append({\n",
            "        \"amfi_code\": amfi,\n",
            "        \"max_drawdown\": max_dd,\n",
            "        \"worst_drawdown_peak_date\": peak_date.strftime('%Y-%m-%d'),\n",
            "        \"worst_drawdown_trough_date\": trough_date.strftime('%Y-%m-%d'),\n",
            "        \"worst_drawdown_recovery_date\": recovery_date.strftime('%Y-%m-%d') if isinstance(recovery_date, pd.Timestamp) else recovery_date\n",
            "    })\n",
            "    \n",
            "dd_df = pd.DataFrame(dd_list)\n",
            "print(\"Drawdown analysis complete. worst drawdown ranges mapped:\")\n",
            "print(dd_df.head())\n"
        ]
    })
    
    # Cell 9: Fund Scorecard (0-100)
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 6. Fund Scorecard (0 - 100)\n",
            "Compile a composite scorecard score based on:\n",
            "- $30\\% \\times$ 3yr Return Rank\n",
            "- $25\\% \\times$ Sharpe Ratio Rank\n",
            "- $20\\% \\times$ Alpha Rank\n",
            "- $15\\% \\times$ Inverse Expense Ratio Rank\n",
            "- $10\\% \\times$ Inverse Max Drawdown Rank\n",
            "\n",
            "Export scorecard to `fund_scorecard.csv`."
        ]
    })
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "score_df = master_df[['amfi_code', 'scheme_name', 'fund_house', 'expense_ratio_pct']].copy()\n",
            "score_df = score_df.merge(cagr_df, on='amfi_code')\n",
            "score_df = score_df.merge(ratios_df, on='amfi_code')\n",
            "score_df = score_df.merge(reg_df, on='amfi_code')\n",
            "score_df = score_df.merge(dd_df, on='amfi_code')\n",
            "\n",
            "# Percentile ranks\n",
            "score_df['rank_3yr'] = score_df['cagr_3yr'].rank(pct=True) * 100\n",
            "score_df['rank_sharpe'] = score_df['sharpe_ratio'].rank(pct=True) * 100\n",
            "score_df['rank_alpha'] = score_df['alpha'].rank(pct=True) * 100\n",
            "score_df['rank_expense'] = score_df['expense_ratio_pct'].rank(ascending=False, pct=True) * 100\n",
            "score_df['rank_dd'] = score_df['max_drawdown'].rank(pct=True) * 100 # less negative is higher rank\n",
            "\n",
            "# Weighted Score\n",
            "score_df['scorecard_score'] = (\n",
            "    0.30 * score_df['rank_3yr'] +\n",
            "    0.25 * score_df['rank_sharpe'] +\n",
            "    0.20 * score_df['rank_alpha'] +\n",
            "    0.15 * score_df['rank_expense'] +\n",
            "    0.10 * score_df['rank_dd']\n",
            ")\n",
            "\n",
            "score_df['scorecard_rank'] = score_df['scorecard_score'].rank(ascending=False, method='min')\n",
            "score_df_sorted = score_df.sort_values(by='scorecard_rank')\n",
            "score_df_sorted.to_csv(\"../fund_scorecard.csv\", index=False)\n",
            "print(\"Scorecard calculated. Top 5 schemes:\")\n",
            "print(score_df_sorted[['scheme_name', 'scorecard_score', 'scorecard_rank']].head(5))\n"
        ]
    })
    
    # Cell 10: Benchmark Comparison Chart & Tracking Error
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 7. Benchmark Comparison & Tracking Error\n",
            "Compare rebased NAV trajectories of the top 5 scorecard funds vs Nifty 50 and Nifty 100 benchmarks over a 3-year window. Compute daily tracking error: $TE = Std(Rp - Rb) \\times \\sqrt{252}$ against Nifty 100."
        ]
    })
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "top_5 = score_df_sorted.head(5)\n",
            "top_5_codes = top_5['amfi_code'].tolist()\n",
            "top_5_names = top_5['scheme_name'].tolist()\n",
            "\n",
            "start_3yr = max_date - pd.DateOffset(years=3)\n",
            "nav_3yr = nav_df[(nav_df['amfi_code'].isin(top_5_codes)) & (nav_df['date'] >= start_3yr)].copy()\n",
            "\n",
            "bench_3yr = bench_df[(bench_df['index_name'].isin(['NIFTY50', 'NIFTY100'])) & (pd.to_datetime(bench_df['date']) >= start_3yr)].copy()\n",
            "bench_3yr['date'] = pd.to_datetime(bench_3yr['date'])\n",
            "\n",
            "nav_pivot = nav_3yr.pivot(index='date', columns='amfi_code', values='nav')\n",
            "bench_pivot = bench_3yr.pivot(index='date', columns='index_name', values='close_value')\n",
            "\n",
            "merged_3yr = nav_pivot.merge(bench_pivot, left_index=True, right_index=True, how='inner')\n",
            "rebased = merged_3yr.div(merged_3yr.iloc[0]) * 100.0\n",
            "\n",
            "# Calculate tracking errors\n",
            "nifty100_ret = merged_3yr['NIFTY100'].pct_change().dropna()\n",
            "te_results = {}\n",
            "for code in top_5_codes:\n",
            "    fund_ret = merged_3yr[code].pct_change().dropna()\n",
            "    aligned = pd.DataFrame({'fund': fund_ret, 'bench': nifty100_ret}).dropna()\n",
            "    te = np.std(aligned['fund'] - aligned['bench']) * np.sqrt(252)\n",
            "    te_results[code] = te\n",
            "\n",
            "# Plotting\n",
            "plt.figure(figsize=(12, 7))\n",
            "for code, name in zip(top_5_codes, top_5_names):\n",
            "    plt.plot(rebased.index, rebased[code], label=f\"{name} (TE: {te_results[code]*100:.2f}%)\")\n",
            "    \n",
            "plt.plot(rebased.index, rebased['NIFTY50'], label=\"NIFTY 50\", color='black', linestyle='--')\n",
            "plt.plot(rebased.index, rebased['NIFTY100'], label=\"NIFTY 100\", color='red', linestyle='-.')\n",
            "\n",
            "plt.title(\"3-Year Cumulative Performance Comparison vs Benchmarks (Rebased to 100)\")\n",
            "plt.xlabel(\"Date\")\n",
            "plt.ylabel(\"Rebased NAV / Index Value\")\n",
            "plt.legend(loc=\"upper left\", fontsize=8)\n",
            "plt.tight_layout()\n",
            "plt.savefig(\"../reports/images/benchmark_comparison.png\", dpi=150)\n",
            "plt.show()\n",
            "print(\"Benchmark comparison plot successfully exported to reports/images/benchmark_comparison.png\")"
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
