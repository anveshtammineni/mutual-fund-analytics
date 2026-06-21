import os
import requests
import pandas as pd
from datetime import datetime

# Define directories
RAW_DIR = r"D:\mutual-fund-analytics\data\raw"
os.makedirs(RAW_DIR, exist_ok=True)

# API Base URL
API_BASE_URL = "https://api.mfapi.in/mf"

# Key Schemes
HDFC_SCHEME_CODE = "125497"
KEY_SCHEMES = {
    "119551": "SBI Bluechip",
    "120503": "ICICI Bluechip",
    "118632": "Nippon Large Cap",
    "119092": "Axis Bluechip",
    "120841": "Kotak Bluechip"
}

def fetch_scheme_data(scheme_code):
    """
    Fetches JSON data from mfapi.in for a given scheme code.
    """
    url = f"{API_BASE_URL}/{scheme_code}"
    print(f"Fetching data from: {url}")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Failed to fetch scheme {scheme_code}: {e}")
        return None

def process_nav_data(json_data, scheme_code=None):
    """
    Parses the JSON data into a pandas DataFrame with standard YYYY-MM-DD dates.
    """
    if not json_data or "data" not in json_data:
        return pd.DataFrame()
        
    records = []
    for item in json_data["data"]:
        # Parse date from DD-MM-YYYY to YYYY-MM-DD
        try:
            date_str = item["date"]
            parsed_date = datetime.strptime(date_str, "%d-%m-%Y").strftime("%y-%m-%d") # wait, %Y for 4-digit year
            # Let's use %Y for YYYY-MM-DD
            parsed_date = datetime.strptime(date_str, "%d-%m-%Y").strftime("%Y-%m-%d")
            nav_val = float(item["nav"])
            
            record = {"date": parsed_date, "nav": nav_val}
            if scheme_code:
                record["amfi_code"] = int(scheme_code)
            records.append(record)
        except Exception as e:
            # Skip any malformed records
            continue
            
    df = pd.DataFrame(records)
    # Sort by date ascending
    if not df.empty:
        df = df.sort_values("date").reset_index(drop=True)
    return df

def fetch_and_save_hdfc():
    """
    Day 1 Task: Fetch live NAV for HDFC Top 100 Direct (125497) and save as raw CSV.
    """
    print("\n--- Fetching HDFC Top 100 Direct NAV ---")
    data = fetch_scheme_data(HDFC_SCHEME_CODE)
    if data:
        df = process_nav_data(data)
        if not df.empty:
            output_path = os.path.join(RAW_DIR, "live_hdfc_nav.csv")
            df.to_csv(output_path, index=False)
            print(f"Successfully saved {len(df)} HDFC NAV rows to {output_path}")
            print(df.tail(3))
        else:
            print("ERROR: Processed HDFC data is empty")
    else:
        print("ERROR: Failed to fetch HDFC data")

def fetch_and_save_key_schemes():
    """
    Day 1 Task: Fetch NAV for 5 key schemes and save to key_schemes_nav.csv.
    """
    print("\n--- Fetching 5 Key Schemes NAV ---")
    all_dfs = []
    
    for code, name in KEY_SCHEMES.items():
        print(f"Scheme: {name} (AMFI Code: {code})")
        data = fetch_scheme_data(code)
        if data:
            df = process_nav_data(data, scheme_code=code)
            if not df.empty:
                print(f"Fetched {len(df)} rows for {name}")
                all_dfs.append(df)
            else:
                print(f"WARNING: No data parsed for {name}")
        else:
            print(f"WARNING: Failed to fetch {name}")
            
    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True)
        # Reorder columns to put amfi_code first
        combined_df = combined_df[["amfi_code", "date", "nav"]]
        output_path = os.path.join(RAW_DIR, "key_schemes_nav.csv")
        combined_df.to_csv(output_path, index=False)
        print(f"\nSuccessfully saved combined {len(combined_df)} rows to {output_path}")
        print(combined_df.head(3))
        print("...")
        print(combined_df.tail(3))
    else:
        print("ERROR: No key schemes data fetched")

def main():
    fetch_and_save_hdfc()
    fetch_and_save_key_schemes()

if __name__ == "__main__":
    main()
