import os
import pandas as pd
import numpy as np

# Define directories
RAW_DIR = r"D:\mutual-fund-analytics\data\raw"
PROCESSED_DIR = r"D:\mutual-fund-analytics\data\processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)

def clean_nav_history():
    print("Cleaning 02_nav_history.csv...")
    filepath = os.path.join(RAW_DIR, "02_nav_history.csv")
    df = pd.read_csv(filepath)
    
    # 1. Parse dates to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # 2. Validate NAV > 0
    initial_rows = len(df)
    df = df[df['nav'] > 0]
    dropped_invalid_nav = initial_rows - len(df)
    if dropped_invalid_nav > 0:
        print(f"  - Dropped {dropped_invalid_nav} rows with NAV <= 0")
        
    # 3. Sort by amfi_code + date
    df = df.sort_values(by=['amfi_code', 'date'])
    
    # 4. Remove duplicate rows
    df = df.drop_duplicates(subset=['amfi_code', 'date'])
    
    # 5. Forward-fill missing NAV for holidays/weekends
    # Group by amfi_code and reindex to complete daily calendar
    cleaned_groups = []
    for amfi, group in df.groupby('amfi_code'):
        group = group.set_index('date')
        # Create a full daily index from min date to max date for this fund
        full_range = pd.date_range(start=group.index.min(), end=group.index.max(), freq='D')
        group_filled = group.reindex(full_range)
        
        # Fill in the ID column and forward-fill the NAV values
        group_filled['amfi_code'] = amfi
        group_filled['nav'] = group_filled['nav'].ffill()
        
        # Reset index to restore 'date' column
        group_filled = group_filled.reset_index().rename(columns={'index': 'date'})
        cleaned_groups.append(group_filled)
        
    df_cleaned = pd.concat(cleaned_groups, ignore_index=True)
    
    # Format date back to string YYYY-MM-DD
    df_cleaned['date'] = df_cleaned['date'].dt.strftime('%Y-%m-%d')
    
    output_path = os.path.join(PROCESSED_DIR, "02_nav_history.csv")
    df_cleaned.to_csv(output_path, index=False)
    print(f"  - Processed NAV rows: {initial_rows} -> {len(df_cleaned)} (expanded for weekends/holidays)")
    return df_cleaned

def clean_investor_transactions():
    print("Cleaning 08_investor_transactions.csv...")
    filepath = os.path.join(RAW_DIR, "08_investor_transactions.csv")
    df = pd.read_csv(filepath)
    
    # 1. Standardise transaction_type
    df['transaction_type'] = df['transaction_type'].str.strip()
    # Map synonyms if any (in this dataset they are clean: SIP, Lumpsum, Redemption)
    type_mapping = {
        'sip': 'SIP', 'SIP': 'SIP',
        'lumpsum': 'Lumpsum', 'Lumpsum': 'Lumpsum', 'lump_sum': 'Lumpsum',
        'redemption': 'Redemption', 'Redemption': 'Redemption', 'redeem': 'Redemption'
    }
    df['transaction_type'] = df['transaction_type'].map(type_mapping).fillna(df['transaction_type'])
    
    # 2. Validate amount > 0
    initial_rows = len(df)
    df = df[df['amount_inr'] > 0]
    dropped_invalid_amount = initial_rows - len(df)
    if dropped_invalid_amount > 0:
        print(f"  - Dropped {dropped_invalid_amount} transactions with amount <= 0")
        
    # 3. Fix date formats to standard YYYY-MM-DD
    df['transaction_date'] = pd.to_datetime(df['transaction_date']).dt.strftime('%Y-%m-%d')
    
    # 4. Check KYC status enum values (must be 'Verified' or 'Pending', map default if unknown)
    df['kyc_status'] = df['kyc_status'].str.strip()
    valid_kyc = {'Verified', 'Pending'}
    df['kyc_status'] = df['kyc_status'].apply(lambda x: x if x in valid_kyc else 'Pending')
    
    # 5. Remove duplicate rows
    df = df.drop_duplicates()
    
    output_path = os.path.join(PROCESSED_DIR, "08_investor_transactions.csv")
    df.to_csv(output_path, index=False)
    print(f"  - Processed transactions rows: {initial_rows} -> {len(df)}")
    return df

def clean_scheme_performance():
    print("Cleaning 07_scheme_performance.csv...")
    filepath = os.path.join(RAW_DIR, "07_scheme_performance.csv")
    df = pd.read_csv(filepath)
    
    # 1. Validate return values are numeric
    return_cols = ['return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct', 'benchmark_3yr_pct', 'alpha', 'beta', 'sharpe_ratio', 'sortino_ratio']
    for col in return_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            # Fill missing returns with median of their respective categories
            df[col] = df.groupby('category')[col].transform(lambda x: x.fillna(x.median()))
            
    # 2. Validate expense_ratio range (0.1% to 2.5%)
    # Let's inspect any anomalies outside this range
    anomalies = df[(df['expense_ratio_pct'] < 0.1) | (df['expense_ratio_pct'] > 2.5)]
    if len(anomalies) > 0:
        print(f"  - WARNING: Found {len(anomalies)} expense ratio anomalies outside range [0.1%, 2.5%]")
        # Cap/clip values to valid bounds
        df['expense_ratio_pct'] = df['expense_ratio_pct'].clip(0.1, 2.5)
        
    # 3. Clean string columns and drop duplicates
    df = df.drop_duplicates()
    
    output_path = os.path.join(PROCESSED_DIR, "07_scheme_performance.csv")
    df.to_csv(output_path, index=False)
    print(f"  - Processed performance rows: {len(df)}")
    return df

def clean_other_datasets():
    other_files = [
        "01_fund_master.csv",
        "03_aum_by_fund_house.csv",
        "04_monthly_sip_inflows.csv",
        "05_category_inflows.csv",
        "06_industry_folio_count.csv",
        "09_portfolio_holdings.csv",
        "10_benchmark_indices.csv"
    ]
    
    for filename in other_files:
        print(f"Cleaning {filename}...")
        filepath = os.path.join(RAW_DIR, filename)
        if not os.path.exists(filepath):
            print(f"  - ERROR: {filename} not found!")
            continue
            
        df = pd.read_csv(filepath)
        initial_rows = len(df)
        
        # Standard cleaning: drop exact duplicates
        df = df.drop_duplicates()
        
        # Standardize date columns if any
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        if 'month' in df.columns:
            # Monthly files can be kept as YYYY-MM
            df['month'] = pd.to_datetime(df['month']).dt.strftime('%Y-%m')
        if 'launch_date' in df.columns:
            df['launch_date'] = pd.to_datetime(df['launch_date']).dt.strftime('%Y-%m-%d')
        if 'portfolio_date' in df.columns:
            df['portfolio_date'] = pd.to_datetime(df['portfolio_date']).dt.strftime('%Y-%m-%d')
            
        # Strip string values
        for col in df.select_dtypes(include='object').columns:
            df[col] = df[col].str.strip()
            
        output_path = os.path.join(PROCESSED_DIR, filename)
        df.to_csv(output_path, index=False)
        print(f"  - Processed rows: {initial_rows} -> {len(df)}")

def main():
    print("=" * 60)
    print(" STARTING DATA CLEANING PIPELINE ")
    print("=" * 60)
    
    clean_nav_history()
    clean_investor_transactions()
    clean_scheme_performance()
    clean_other_datasets()
    
    print("\nData cleaning completed successfully. Cleaned CSVs saved in data/processed/")

if __name__ == "__main__":
    main()
