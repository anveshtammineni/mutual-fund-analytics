import os
import pandas as pd
import numpy as np

# Define directories
RAW_DIR = r"D:\mutual-fund-analytics\data\raw"
REPORTS_DIR = r"D:\mutual-fund-analytics\reports"

os.makedirs(REPORTS_DIR, exist_ok=True)

# List of all 10 datasets
DATASETS = {
    "01_fund_master.csv": "Fund Master",
    "02_nav_history.csv": "NAV History",
    "03_aum_by_fund_house.csv": "AUM by Fund House",
    "04_monthly_sip_inflows.csv": "Monthly SIP Inflows",
    "05_category_inflows.csv": "Category Inflows",
    "06_industry_folio_count.csv": "Industry Folio Count",
    "07_scheme_performance.csv": "Scheme Performance",
    "08_investor_transactions.csv": "Investor Transactions",
    "09_portfolio_holdings.csv": "Portfolio Holdings",
    "10_benchmark_indices.csv": "Benchmark Indices"
}

def load_and_describe_datasets():
    loaded_data = {}
    print("=" * 80)
    print(" STEP 1: LOAD AND DESCRIBE ALL 10 DATASETS ")
    print("=" * 80)
    
    for filename, desc in DATASETS.items():
        filepath = os.path.join(RAW_DIR, filename)
        if not os.path.exists(filepath):
            print(f"ERROR: {filename} not found at {filepath}")
            continue
            
        df = pd.read_csv(filepath)
        loaded_data[filename] = df
        
        print(f"\nDataset: {filename} ({desc})")
        print("-" * 50)
        print(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")
        print("\nData Types:")
        print(df.dtypes)
        print("\nHead (First 3 rows):")
        print(df.head(3))
        print("-" * 80)
        
    return loaded_data

def explore_fund_master(df_master):
    print("\n" + "=" * 80)
    print(" STEP 2: EXPLORING FUND MASTER ")
    print("=" * 80)
    
    unique_fund_houses = df_master['fund_house'].unique()
    unique_categories = df_master['category'].unique()
    unique_sub_categories = df_master['sub_category'].unique()
    unique_risk_categories = df_master['risk_category'].unique()
    
    print(f"Total Unique Fund Houses ({len(unique_fund_houses)}):")
    for fh in sorted(unique_fund_houses):
        print(f" - {fh}")
        
    print(f"\nTotal Unique Categories ({len(unique_categories)}):")
    for cat in sorted(unique_categories):
        print(f" - {cat}")
        
    print(f"\nTotal Unique Sub-Categories ({len(unique_sub_categories)}):")
    for subcat in sorted(unique_sub_categories):
        print(f" - {subcat}")
        
    print(f"\nTotal Unique Risk Categories ({len(unique_risk_categories)}):")
    for rc in sorted(unique_risk_categories):
        print(f" - {rc}")
        
    print("\nAMFI Code Structure:")
    print("AMFI codes are unique, numeric identifiers assigned to mutual fund schemes by the Association of Mutual Funds in India.")
    print(f"Min AMFI Code: {df_master['amfi_code'].min()}")
    print(f"Max AMFI Code: {df_master['amfi_code'].max()}")
    print(f"Are all AMFI codes unique? {df_master['amfi_code'].is_unique}")
    
def validate_amfi_codes(df_master, df_nav):
    print("\n" + "=" * 80)
    print(" STEP 3: VALIDATING AMFI CODES ")
    print("=" * 80)
    
    master_codes = set(df_master['amfi_code'].unique())
    nav_codes = set(df_nav['amfi_code'].unique())
    
    missing_in_nav = master_codes - nav_codes
    extra_in_nav = nav_codes - master_codes
    
    print(f"Unique AMFI codes in Fund Master: {len(master_codes)}")
    print(f"Unique AMFI codes in NAV History: {len(nav_codes)}")
    
    if len(missing_in_nav) == 0:
        print("[OK] Validation Success: All AMFI codes in Fund Master exist in NAV History.")
    else:
        print(f"[WARNING] Validation Warning: {len(missing_in_nav)} codes in Fund Master are MISSING from NAV History.")
        print(f"Missing codes: {missing_in_nav}")
        
    if len(extra_in_nav) > 0:
        print(f"[INFO] Note: NAV History contains {len(extra_in_nav)} codes that are not in Fund Master.")
        
    return missing_in_nav, extra_in_nav

def generate_quality_report(loaded_data, missing_in_nav, extra_in_nav):
    print("\n" + "=" * 80)
    print(" STEP 4: GENERATING DATA QUALITY REPORT ")
    print("=" * 80)
    
    report_path = os.path.join(REPORTS_DIR, "data_quality_summary.md")
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Data Quality Summary Report (Day 1 - Ingestion)\n\n")
        f.write(f"Generated on: 2026-06-21\n\n")
        
        f.write("## 1. Overview of Datasets\n\n")
        f.write("| Dataset Filename | Description | Row Count | Column Count | Null Values Found |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- |\n")
        
        anomalies_log = []
        
        for name, df in loaded_data.items():
            null_cols = df.isnull().sum()
            null_sum = null_cols.sum()
            null_info = "None" if null_sum == 0 else f"{null_sum} ({', '.join([f'{c}: {v}' for c, v in null_cols.items() if v > 0])})"
            
            f.write(f"| {name} | {DATASETS[name]} | {df.shape[0]} | {df.shape[1]} | {null_info} |\n")
            
            # Detect duplicates
            dup_count = df.duplicated().sum()
            if dup_count > 0:
                anomalies_log.append(f"**{name}**: Found {dup_count} duplicate rows.")
                
            # Specific check for missing dates
            for date_col in ['date', 'month', 'transaction_date', 'portfolio_date']:
                if date_col in df.columns:
                    # check if string parses as date
                    try:
                        pd.to_datetime(df[date_col])
                    except Exception as e:
                        anomalies_log.append(f"**{name}**: Column `{date_col}` contains unparseable date formats.")
            
            # Specific check for monthly SIP YoY Growth nulls
            if name == "04_monthly_sip_inflows.csv":
                sip_nulls = df['yoy_growth_pct'].isnull().sum()
                if sip_nulls > 0:
                    anomalies_log.append(f"**{name}**: Column `yoy_growth_pct` contains {sip_nulls} null values (likely due to first year of data having no comparison baseline).")
                    
        f.write("\n## 2. Identified Anomalies & Notes\n\n")
        if anomalies_log:
            for anomaly in anomalies_log:
                f.write(f"- {anomaly}\n")
        else:
            f.write("- No major database anomalies detected in the raw CSV files.\n")
            
        f.write("\n## 3. AMFI Code Validation Analysis\n\n")
        f.write(f"- **Total Unique Schemes in Fund Master:** {len(loaded_data['01_fund_master.csv']['amfi_code'].unique())}\n")
        f.write(f"- **Total Unique Schemes in NAV History:** {len(loaded_data['02_nav_history.csv']['amfi_code'].unique())}\n")
        
        if len(missing_in_nav) == 0:
            f.write("- ✅ **All AMFI codes in Fund Master have historical NAV entries in NAV History.**\n")
        else:
            f.write(f"- ⚠️ **{len(missing_in_nav)} AMFI codes in Fund Master are MISSING from NAV History:** {sorted(list(missing_in_nav))}\n")
            
        if len(extra_in_nav) > 0:
            f.write(f"- ℹ️ **NAV History contains {len(extra_in_nav)} AMFI codes not listed in the Fund Master.** These may correspond to schemes not featured in the current Fund Master list.\n")
            
        f.write("\n## 4. Fund Master Exploration Summary\n\n")
        df_master = loaded_data['01_fund_master.csv']
        f.write(f"- **Fund Houses:** {df_master['fund_house'].nunique()} unique fund houses\n")
        f.write(f"- **Categories:** {df_master['category'].nunique()} unique categories ({', '.join(df_master['category'].unique())})\n")
        f.write(f"- **Sub-Categories:** {df_master['sub_category'].nunique()} unique sub-categories\n")
        f.write(f"- **Risk Categories:** {df_master['risk_category'].nunique()} levels ({', '.join(df_master['risk_category'].unique())})\n")
        
    print(f"Data quality summary written to: {report_path}")

def main():
    loaded_data = load_and_describe_datasets()
    
    if "01_fund_master.csv" in loaded_data:
        explore_fund_master(loaded_data["01_fund_master.csv"])
        
    if "01_fund_master.csv" in loaded_data and "02_nav_history.csv" in loaded_data:
        missing_in_nav, extra_in_nav = validate_amfi_codes(
            loaded_data["01_fund_master.csv"], 
            loaded_data["02_nav_history.csv"]
        )
        generate_quality_report(loaded_data, missing_in_nav, extra_in_nav)

if __name__ == "__main__":
    main()
