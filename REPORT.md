# Marketing Campaign Analysis Report

## Problem understanding
The objective is to identify the most valuable and most responsive customer segments, understand spending and channel behavior, and support future targeting decisions with a dashboard and SQL-backed analytics layer.

## Data preparation
- Loaded `marketing_data.csv`
- Validated fields against `marketing_data_dictionary.csv`
- Converted `Dt_Customer` to date
- Handled invalid or missing values in `Income`, `Recency`, and usage metrics
- Derived:
  - `Age`
  - `Customer_Tenure_Days`
  - `Customer_Tenure_Months`
  - `Total_Spend`
  - `Total_Purchases`
  - `Children`
  - `Income_Band`
  - `Age_Band`
- Applied rule-based segments:
  - High Income
  - Young Customer
  - Campaign Responder
  - High Web Engagement
  - Family Customer
  - High Spender

## KPI summary
- Total customers: `56,000`
- Average total spend: `640.33`
- Average income: `57,213.90`
- Overall response rate: `14.76%`
- Average web visits per month: `5.17`
- Average total purchases: `13.24`

## Most valuable and responsive segments
- `Campaign Responder`
  - Response rate: `100.00%`
  - Avg total spend: `688.25`
- `High Income`
  - Response rate: `23.54%`
  - Avg total spend: `1,038.03`
- `High Spender`
  - Avg total spend: `1,922.04`
  - Very small segment and low current response in the primary-segment assignment output

## Required business questions covered
- Highest response rate by segment and by campaign:
  - `segment_campaign_response` view
- Spending patterns across products by age, income, marital status, and country:
  - `spending_by_demographics` view
- Channel usage by high-value customers:
  - `channel_usage_high_value` view
- Under-served segments:
  - `underserved_segments` view
- Characteristics of ideal target customers:
  - `ideal_target_customers` view

## Actionable recommendations
1. Prioritize `High Income` customers for future campaigns because they combine strong spend with the highest scalable response rate.
2. Retarget `Campaign Responders` with follow-up offers and loyalty journeys because they already demonstrate clear acceptance behavior.
3. Focus conversion programs on `High Web Engagement` and `Under_Served_Customer` groups because they visit often but underperform on spend or response.
4. Use product-led targeting around wines and meat for higher-value audiences, since spend concentration is strongest in those categories.
5. Add country, age band, and income band targeting in campaign planning because those dimensions are now available directly in the analytics layer.
6. Use the `ideal_target_customers` output as the shortlist for future campaign audience design.

## Deliverables status
- Python cleaning and feature engineering: complete
- SQL schema and analytical queries: complete
- Power BI-ready dashboard data package: complete
- Project report: complete

## Limitation
A native `.pbix` file was not generated in this environment because Power BI Desktop was not available to automate report creation. The Power BI-ready exported datasets and dashboard specification are included for direct use in Power BI Desktop.
