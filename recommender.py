import os
import sys
import argparse
import pandas as pd

# Paths
SCORECARD_PATH = r"D:\mutual-fund-analytics\fund_scorecard.csv"
MASTER_PATH = r"D:\mutual-fund-analytics\data\processed\01_fund_master.csv"

def get_recommendations(risk_appetite):
    if not os.path.exists(SCORECARD_PATH):
        print(f"[ERROR] Fund scorecard file not found at: {SCORECARD_PATH}")
        print("Please run the Day 4 performance analytics notebook first to generate it.")
        return None
        
    scorecard = pd.read_csv(SCORECARD_PATH)
    
    # Check if 'risk_category' is in scorecard; if not, merge it from master_df
    if 'risk_category' not in scorecard.columns:
        if os.path.exists(MASTER_PATH):
            master = pd.read_csv(MASTER_PATH)
            scorecard = scorecard.merge(master[['amfi_code', 'risk_category']], on='amfi_code')
        else:
            print(f"[ERROR] Fund master file not found at: {MASTER_PATH}")
            return None
            
    risk_appetite = risk_appetite.strip().capitalize()
    
    # Map appetite to categories
    if risk_appetite == 'Low':
        target_categories = ['Low']
    elif risk_appetite == 'Moderate':
        target_categories = ['Moderate', 'Moderately High']
    elif risk_appetite == 'High':
        target_categories = ['High', 'Very High']
    else:
        print(f"[ERROR] Invalid risk appetite input: '{risk_appetite}'. Choose from Low, Moderate, High.")
        return None
        
    # Filter and sort by Sharpe Ratio
    filtered = scorecard[scorecard['risk_category'].isin(target_categories)].copy()
    
    if filtered.empty:
        print(f"[WARNING] No funds found matching risk categories: {target_categories}")
        return filtered
        
    recommendations = filtered.sort_values(by='sharpe_ratio', ascending=False).head(3)
    return recommendations[['amfi_code', 'scheme_name', 'risk_category', 'sharpe_ratio', 'cagr_3yr']]

def print_table(df, appetite):
    if df is None or df.empty:
        return
        
    print("\n" + "="*80)
    print(f" BLUESTOCK FUND RECOMMENDER - RECOMMENDATIONS FOR RISK PROFILE: {appetite.upper()} ")
    print("="*80)
    print(f"{'Rank':<5} | {'AMFI Code':<10} | {'Scheme Name':<45} | {'Sharpe':<8} | {'3yr CAGR':<8}")
    print("-"*80)
    
    for i, (_, row) in enumerate(df.iterrows(), 1):
        cagr_val = f"{row['cagr_3yr']*100:.2f}%" if pd.notnull(row['cagr_3yr']) else "N/A"
        sharpe_val = f"{row['sharpe_ratio']:.2f}" if pd.notnull(row['sharpe_ratio']) else "N/A"
        print(f"{i:<5} | {row['amfi_code']:<10} | {row['scheme_name'][:45]:<45} | {sharpe_val:<8} | {cagr_val:<8}")
        
    print("="*80 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Bluestock Mutual Fund Recommender Tool")
    parser.add_argument(
        '-r', '--risk',
        type=str,
        choices=['Low', 'Moderate', 'High', 'low', 'moderate', 'high'],
        help="Investor's risk appetite: Low, Moderate, or High"
    )
    
    args = parser.parse_args()
    
    risk_appetite = args.risk
    if not risk_appetite:
        print("\nWelcome to the Bluestock Mutual Fund Recommender Tool!")
        print("Please choose your risk appetite:")
        print("  1. Low (Focus on capital preservation and debt instruments)")
        print("  2. Moderate (Balanced growth with moderate stock exposure)")
        print("  3. High (Aggressive growth with equity and small-cap exposure)")
        
        choice = input("\nEnter choice (1, 2, 3 or type Low/Moderate/High): ").strip()
        if choice in ['1', 'low', 'Low']:
            risk_appetite = 'Low'
        elif choice in ['2', 'moderate', 'Moderate']:
            risk_appetite = 'Moderate'
        elif choice in ['3', 'high', 'High']:
            risk_appetite = 'High'
        else:
            # Fallback direct type match
            risk_appetite = choice
            
    recs = get_recommendations(risk_appetite)
    print_table(recs, risk_appetite)

if __name__ == "__main__":
    main()
