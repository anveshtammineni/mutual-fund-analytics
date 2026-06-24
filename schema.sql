-- Bluestock Mutual Fund Analytics Database Schema --
-- Generated on: 2026-06-24

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

CREATE TABLE IF NOT EXISTS dim_date (
            date TEXT PRIMARY KEY, -- YYYY-MM-DD
            year INTEGER NOT NULL,
            month INTEGER NOT NULL,
            day INTEGER NOT NULL,
            quarter INTEGER NOT NULL,
            day_of_week INTEGER NOT NULL,
            is_weekend INTEGER NOT NULL
        );

CREATE TABLE IF NOT EXISTS fact_nav (
            amfi_code INTEGER,
            date TEXT,
            nav REAL NOT NULL,
            PRIMARY KEY (amfi_code, date),
            FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
            FOREIGN KEY (date) REFERENCES dim_date(date)
        );

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

CREATE TABLE IF NOT EXISTS fact_aum (
            aum_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            fund_house TEXT NOT NULL,
            aum_lakh_crore REAL,
            aum_crore INTEGER,
            num_schemes INTEGER,
            FOREIGN KEY (date) REFERENCES dim_date(date)
        );

CREATE TABLE IF NOT EXISTS fact_sip_inflows (
            month TEXT PRIMARY KEY, -- YYYY-MM
            sip_inflow_crore INTEGER,
            active_sip_accounts_crore REAL,
            new_sip_accounts_lakh REAL,
            sip_aum_lakh_crore REAL,
            yoy_growth_pct REAL
        );

CREATE TABLE IF NOT EXISTS fact_category_inflows (
            month TEXT NOT NULL, -- YYYY-MM
            category TEXT NOT NULL,
            net_inflow_crore REAL,
            PRIMARY KEY (month, category)
        );

CREATE TABLE IF NOT EXISTS fact_industry_folios (
            month TEXT PRIMARY KEY, -- YYYY-MM
            total_folios_crore REAL,
            equity_folios_crore REAL,
            debt_folios_crore REAL,
            hybrid_folios_crore REAL,
            others_folios_crore REAL
        );

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

CREATE TABLE IF NOT EXISTS fact_benchmark_indices (
            date TEXT,
            index_name TEXT,
            close_value REAL,
            PRIMARY KEY (date, index_name),
            FOREIGN KEY (date) REFERENCES dim_date(date)
        );

