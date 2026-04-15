# Marketing Campaign Analysis Report

## Problem understanding
The objective is to identify the most valuable and most responsive customer segments, analyze spending and channel behavior, and present the findings in an interactive Streamlit dashboard.

## Data preparation
- Loaded `marketing_data.csv`
- validated columns using `marketing_data_dictionary.csv`
- converted `Dt_Customer` to date
- handled missing and invalid values in `Income`, `Recency`, and usage fields
- derived:
  - `Age`
  - `Customer_Tenure_Days`
  - `Customer_Tenure_Months`
  - `Total_Spend`
  - `Total_Purchases`
  - `Children`
  - `Income_Band`
  - `Age_Band`
- implemented rule-based segments:
  - High Income
  - Young Customer
  - Campaign Responder
  - High Web Engagement
  - Family Customer
  - High Spender

## SQL deliverables
- main customer schema in [marketing_schema.sql](C:\Users\Anusha\Desktop\marketing-campaign-analysis-dashboard\sql\marketing_schema.sql)
- analytical queries in [SQL_QUERIES.sql](C:\Users\Anusha\Desktop\marketing-campaign-analysis-dashboard\SQL_QUERIES.sql)
- views supporting:
  - KPI summaries
  - segment response analysis
  - spending by demographic lens
  - high-value channel usage
  - under-served segments
  - ideal target customer profiles

## Dashboard deliverable
The dashboard deliverable is the Streamlit app in [streamlit_app.py](C:\Users\Anusha\Desktop\marketing-campaign-analysis-dashboard\streamlit_app.py).

It includes:
- KPI cards
- campaign response analysis by segment
- product spending analysis by age, income, marital status, and country
- channel usage analysis for high-value customers
- under-served segment analysis
- ideal target customer profiling
- interactive filters for:
  - Country
  - Education
  - Marital_Status
  - Age_Band
  - Income_Band

## KPI summary
- Total customers: `56,000`
- Average total spend: `640.33`
- Average income: `57,213.90`
- Overall response rate: `14.76%`
- Average web visits per month: `5.17`
- Average total purchases: `13.24`

## Key findings
- `High Income` customers are the strongest scalable response segment.
- `High Spender` customers contribute the highest spend intensity.
- `High Web Engagement` and under-served customers show conversion opportunity.
- Wines and meat remain the strongest spend categories.

## Actionable recommendations
1. Prioritize high-income segments for future campaigns because they combine stronger response and stronger spend.
2. Retarget campaign responders with personalized follow-up campaigns.
3. Focus web-conversion improvements on high-visit, low-response customer groups.
4. Lead premium offers with high-performing product categories such as wines and meat.
5. Use age band, income band, marital status, and country as primary targeting lenses.
6. Use the ideal target customer profile outputs to shortlist future campaign audiences.
