-- ==============================================================================
-- BLUESTOCK MUTUAL FUND ANALYTICS - ANALYTICAL SQL QUERIES (DAY 2)
-- ==============================================================================

-- 1. Top 5 funds by AUM (Assets Under Management)
-- Business Definition: Lists the top 5 largest mutual fund schemes by AUM in crores.
SELECT 
    amfi_code, 
    scheme_name, 
    fund_house, 
    aum_crore
FROM fact_performance
ORDER BY aum_crore DESC
LIMIT 5;


-- 2. Average NAV per month
-- Business Definition: Computes the average NAV value across all funds grouped by calendar year and month.
SELECT 
    d.year, 
    d.month, 
    ROUND(AVG(n.nav), 4) AS avg_nav
FROM fact_nav n
JOIN dim_date d ON n.date = d.date
GROUP BY d.year, d.month
ORDER BY d.year, d.month;


-- 3. SIP YoY Inflow Growth
-- Business Definition: Calculates the year-over-year percentage growth in monthly SIP inflows by joining the current month with the same month from the previous year.
WITH monthly_inflows AS (
    SELECT 
        month,
        sip_inflow_crore,
        SUBSTR(month, 1, 4) AS year,
        SUBSTR(month, 6, 2) AS month_num,
        yoy_growth_pct AS recorded_yoy_growth_pct
    FROM fact_sip_inflows
)
SELECT 
    cur.month,
    cur.sip_inflow_crore AS current_year_inflow_cr,
    prev.sip_inflow_crore AS last_year_inflow_cr,
    ROUND(((cur.sip_inflow_crore - prev.sip_inflow_crore) * 100.0 / prev.sip_inflow_crore), 2) AS calculated_yoy_growth_pct,
    cur.recorded_yoy_growth_pct
FROM monthly_inflows cur
LEFT JOIN monthly_inflows prev 
    ON cur.month_num = prev.month_num 
    AND CAST(cur.year AS INTEGER) = CAST(prev.year AS INTEGER) + 1
ORDER BY cur.month;


-- 4. Total Transactions by State
-- Business Definition: Aggregates the number of transactions and total transaction amount in INR across Indian states.
SELECT 
    state, 
    COUNT(*) AS transaction_count, 
    SUM(amount_inr) AS total_amount_inr
FROM fact_transactions
GROUP BY state
ORDER BY total_amount_inr DESC;


-- 5. Funds with expense_ratio < 1%
-- Business Definition: Identifies mutual fund schemes with a low management expense ratio (under 1.0%).
SELECT 
    amfi_code, 
    scheme_name, 
    fund_house, 
    expense_ratio_pct
FROM fact_performance
WHERE expense_ratio_pct < 1.0
ORDER BY expense_ratio_pct ASC;


-- 6. Top 5 sector allocations across portfolio holdings
-- Business Definition: Aggregates the average percentage weight allocated to different sectors across all portfolios.
SELECT 
    sector, 
    ROUND(AVG(weight_pct), 2) AS avg_weight_pct
FROM fact_portfolio_holdings
GROUP BY sector
ORDER BY avg_weight_pct DESC
LIMIT 5;


-- 7. Top 5 stocks by aggregate market value across all portfolios
-- Business Definition: Sums the total market value of specific stocks held across all fund portfolios to find the most heavily invested companies.
SELECT 
    stock_name, 
    stock_symbol, 
    ROUND(SUM(market_value_cr), 2) AS total_market_value_cr
FROM fact_portfolio_holdings
GROUP BY stock_name, stock_symbol
ORDER BY total_market_value_cr DESC
LIMIT 5;


-- 8. Total Transaction Volume & Amount by Payment Mode
-- Business Definition: Evaluates investor payment preferences by grouping count and value of transactions by payment type.
SELECT 
    payment_mode, 
    COUNT(*) AS transaction_count, 
    SUM(amount_inr) AS total_amount_inr
FROM fact_transactions
GROUP BY payment_mode
ORDER BY total_amount_inr DESC;


-- 9. KYC Status Distribution of Transaction Volume
-- Business Definition: Displays the volume and amount of transactions based on the KYC status of the investor to monitor compliance.
SELECT 
    kyc_status, 
    COUNT(*) AS transaction_count, 
    SUM(amount_inr) AS total_amount_inr
FROM fact_transactions
GROUP BY kyc_status;


-- 10. Correlation baseline: Average NAV vs AUM per Fund House
-- Business Definition: Connects NAV performance with fund house size to see if larger fund houses have higher average NAV values.
SELECT 
    fp.fund_house, 
    COUNT(fp.amfi_code) AS num_schemes,
    ROUND(AVG(fp.aum_crore), 2) AS avg_aum_crore,
    ROUND(AVG(fn.avg_nav), 2) AS avg_nav_value
FROM fact_performance fp
JOIN (
    SELECT amfi_code, AVG(nav) AS avg_nav
    FROM fact_nav
    GROUP BY amfi_code
) fn ON fp.amfi_code = fn.amfi_code
GROUP BY fp.fund_house
ORDER BY avg_aum_crore DESC;
