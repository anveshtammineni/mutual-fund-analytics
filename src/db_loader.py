import os
import sqlite3
import pandas as pd
import numpy as np

# Paths
PROCESSED_DIR = r"D:\mutual-fund-analytics\data\processed"
DB_PATH = r"D:\mutual-fund-analytics\bluestock_mf.db"
SCHEMA_SQL_PATH = r"D:\mutual-fund-analytics\schema.sql"

# DDL Statements for Star Schema
DDL_STATEMENTS = {
    "dim_fund": """
        CREATE TABLE IF NOT EXISTS dim_fund (
            amfi_code INTEGER PRIMARY KEY,
            fund_house TEXT NOT NULL,
            scheme_name TEXT NOT NULL,
            category TEXT NOT NULL,
            sub_category TEXT,
            plan TEXT,
            launch_date TEXT,
            benchmark TEXT,
            expense_ratio_pct REAL,
            exit_load_pct REAL,
            min_sip_amount INTEGER,
            min_lumpsum_amount INTEGER,
            fund_manager TEXT,
            risk_category TEXT,
            sebi_category_code TEXT
        );
    """,
    
    "dim_date": """
        CREATE TABLE IF NOT EXISTS dim_date (
            date TEXT PRIMARY KEY, -- YYYY-MM-DD
            year INTEGER NOT NULL,
            month INTEGER NOT NULL,
            day INTEGER NOT NULL,
            quarter INTEGER NOT NULL,
            day_of_week INTEGER NOT NULL,
            is_weekend INTEGER NOT NULL
        );
    """,
    
    "fact_nav": """
        CREATE TABLE IF NOT EXISTS fact_nav (
            amfi_code INTEGER,
            date TEXT,
            nav REAL NOT NULL,
            PRIMARY KEY (amfi_code, date),
            FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
            FOREIGN KEY (date) REFERENCES dim_date(date)
        );
    """,
    
    "fact_transactions": """
        CREATE TABLE IF NOT EXISTS fact_transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            investor_id TEXT NOT NULL,
            transaction_date TEXT NOT NULL,
            amfi_code INTEGER NOT NULL,
            transaction_type TEXT NOT NULL,
            amount_inr INTEGER NOT NULL,
            state TEXT,
            city TEXT,
            city_tier TEXT,
            age_group TEXT,
            gender TEXT,
            annual_income_lakh REAL,
            payment_mode TEXT,
            kyc_status TEXT,
            FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
            FOREIGN KEY (transaction_date) REFERENCES dim_date(date)
        );
    """,
    
    "fact_performance": """
        CREATE TABLE IF NOT EXISTS fact_performance (
            amfi_code INTEGER PRIMARY KEY,
            scheme_name TEXT,
            fund_house TEXT,
            category TEXT,
            plan TEXT,
            return_1yr_pct REAL,
            return_3yr_pct REAL,
            return_5yr_pct REAL,
            benchmark_3yr_pct REAL,
            alpha REAL,
            beta REAL,
            sharpe_ratio REAL,
            sortino_ratio REAL,
            std_dev_ann_pct REAL,
            max_drawdown_pct REAL,
            aum_crore INTEGER,
            expense_ratio_pct REAL,
            morningstar_rating INTEGER,
            risk_grade TEXT,
            FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
        );
    """,
    
    "fact_aum": """
        CREATE TABLE IF NOT EXISTS fact_aum (
            aum_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            fund_house TEXT NOT NULL,
            aum_lakh_crore REAL,
            aum_crore INTEGER,
            num_schemes INTEGER,
            FOREIGN KEY (date) REFERENCES dim_date(date)
        );
    """,
    
    "fact_sip_inflows": """
        CREATE TABLE IF NOT EXISTS fact_sip_inflows (
            month TEXT PRIMARY KEY, -- YYYY-MM
            sip_inflow_crore INTEGER,
            active_sip_accounts_crore REAL,
            new_sip_accounts_lakh REAL,
            sip_aum_lakh_crore REAL,
            yoy_growth_pct REAL
        );
    """,
    
    "fact_category_inflows": """
        CREATE TABLE IF NOT EXISTS fact_category_inflows (
            month TEXT NOT NULL, -- YYYY-MM
            category TEXT NOT NULL,
            net_inflow_crore REAL,
            PRIMARY KEY (month, category)
        );
    """,
    
    "fact_industry_folios": """
        CREATE TABLE IF NOT EXISTS fact_industry_folios (
            month TEXT PRIMARY KEY, -- YYYY-MM
            total_folios_crore REAL,
            equity_folios_crore REAL,
            debt_folios_crore REAL,
            hybrid_folios_crore REAL,
            others_folios_crore REAL
        );
    """,
    
    "fact_portfolio_holdings": """
        CREATE TABLE IF NOT EXISTS fact_portfolio_holdings (
            amfi_code INTEGER,
            stock_symbol TEXT,
            stock_name TEXT,
            sector TEXT,
            weight_pct REAL,
            market_value_cr REAL,
            current_price_inr REAL,
            portfolio_date TEXT,
            PRIMARY KEY (amfi_code, stock_symbol),
            FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
            FOREIGN KEY (portfolio_date) REFERENCES dim_date(date)
        );
    """,
    
    "fact_benchmark_indices": """
        CREATE TABLE IF NOT EXISTS fact_benchmark_indices (
            date TEXT,
            index_name TEXT,
            close_value REAL,
            PRIMARY KEY (date, index_name),
            FOREIGN KEY (date) REFERENCES dim_date(date)
        );
    """
}

def create_database_and_tables():
    print(f"Creating/connecting to SQLite database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # Write CREATE statements to schema.sql for documentation
    with open(SCHEMA_SQL_PATH, "w", encoding="utf-8") as f:
        f.write("-- Bluestock Mutual Fund Analytics Database Schema --\n")
        f.write("-- Generated on: 2026-06-24\n\n")
        
        for table_name, ddl in DDL_STATEMENTS.items():
            print(f"  - Creating table {table_name}...")
            cursor.execute(ddl)
            f.write(ddl.strip() + "\n\n")
            
    conn.commit()
    print("Schema created successfully and exported to schema.sql")
    return conn

def populate_date_dimension(conn, dfs):
    print("Populating dim_date table...")
    # Gather all unique dates from datasets that use dates
    unique_dates = set()
    
    # Check for date columns in dataframes
    for table_name, df in dfs.items():
        for date_col in ['date', 'transaction_date', 'portfolio_date']:
            if date_col in df.columns:
                unique_dates.update(df[date_col].dropna().unique())
                
    # Create dim_date rows
    date_records = []
    for d_str in sorted(list(unique_dates)):
        try:
            dt = pd.to_datetime(d_str)
            date_records.append({
                "date": d_str,
                "year": dt.year,
                "month": dt.month,
                "day": dt.day,
                "quarter": (dt.month - 1) // 3 + 1,
                "day_of_week": dt.dayofweek,  # 0=Monday, 6=Sunday
                "is_weekend": 1 if dt.dayofweek in [5, 6] else 0
            })
        except Exception:
            continue
            
    df_date = pd.DataFrame(date_records)
    if not df_date.empty:
        df_date.to_sql("dim_date", conn, if_exists="append", index=False)
        print(f"  - Loaded {len(df_date)} unique dates into dim_date")
    else:
        print("  - WARNING: No dates found to load into dim_date")

def load_data(conn):
    print("Loading data into tables...")
    
    # Load all cleaned CSVs
    files_to_tables = {
        "01_fund_master.csv": "dim_fund",
        "02_nav_history.csv": "fact_nav",
        "08_investor_transactions.csv": "fact_transactions",
        "07_scheme_performance.csv": "fact_performance",
        "03_aum_by_fund_house.csv": "fact_aum",
        "04_monthly_sip_inflows.csv": "fact_sip_inflows",
        "05_category_inflows.csv": "fact_category_inflows",
        "06_industry_folio_count.csv": "fact_industry_folios",
        "09_portfolio_holdings.csv": "fact_portfolio_holdings",
        "10_benchmark_indices.csv": "fact_benchmark_indices"
    }
    
    dfs = {}
    for filename, table_name in files_to_tables.items():
        filepath = os.path.join(PROCESSED_DIR, filename)
        if os.path.exists(filepath):
            dfs[table_name] = pd.read_csv(filepath)
            
    # First populate dim_date
    populate_date_dimension(conn, dfs)
    
    # Load each table
    for table_name, df in dfs.items():
        # Clean columns if they don't match SQL definition
        if table_name == "fact_transactions":
            # transaction_id is AUTOINCREMENT, drop it if it is in df (it shouldn't be, but let's be safe)
            if "transaction_id" in df.columns:
                df = df.drop(columns=["transaction_id"])
        elif table_name == "fact_aum":
            if "aum_id" in df.columns:
                df = df.drop(columns=["aum_id"])
                
        df.to_sql(table_name, conn, if_exists="append", index=False)
        
        # Verify row counts
        db_count = pd.read_sql_query(f"SELECT COUNT(*) FROM {table_name}", conn).iloc[0, 0]
        csv_count = len(df)
        status = "Match [OK]" if db_count == csv_count else f"Mismatch [ERROR] (CSV: {csv_count}, DB: {db_count})"
        print(f"  - Table {table_name:<25}: loaded {db_count:<6} rows. Verification: {status}")

def main():
    print("=" * 60)
    print(" STARTING SQL STAR SCHEMA DATABASE LOADER ")
    print("=" * 60)
    
    # Remove existing db if it exists to allow clean recreate
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("Removed existing database to start fresh.")
        
    conn = create_database_and_tables()
    try:
        load_data(conn)
        print("\nDatabase loaded and verified successfully.")
    except Exception as e:
        print(f"\nERROR loading database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
