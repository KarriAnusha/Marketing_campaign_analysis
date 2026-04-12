# Power BI Dashboard Specification

This dashboard specification is limited to the proposal scope.

## Page 1: Executive KPIs
- Cards:
  - Total Customers
  - Average Total Spend
  - Average Income
  - Response Rate %
  - Average Web Visits
  - Average Total Purchases
- Visual:
  - Clustered bar chart for campaign acceptance totals
- Slicers:
  - Country
  - Education
  - Marital_Status
  - Age_Band
  - Income_Band

## Page 2: Segment Response Analysis
- Visual:
  - Matrix from `segment_campaign_response.csv`
- Visual:
  - Bar chart of `final_campaign_response_rate_pct` by `Primary_Segment`
- Visual:
  - Bar chart of `customer_count` by `Primary_Segment`

## Page 3: Product Spending Analysis
- Visual:
  - Stacked bar chart for `avg_wines`, `avg_fruits`, `avg_meat`, `avg_fish`, `avg_sweets`, `avg_gold`
- Axes:
  - Age_Band
  - Income_Band
  - Marital_Status
  - Country
- Use drill-down or slicers instead of extra visuals.

## Page 4: Channel Usage and High-Value Customers
- Visual:
  - Clustered bar chart for `avg_web_purchases`, `avg_store_purchases`, `avg_catalog_purchases`, `avg_deals_purchases`
- Filter:
  - Only high-value customer outputs from `channel_usage_high_value.csv`
- Supporting cards:
  - Avg Total Spend
  - Avg Web Visits
  - Response Rate %

## Page 5: Under-Served Segments
- Visual:
  - Table from `underserved_segments.csv`
- Columns:
  - Primary_Segment
  - Age_Band
  - Income_Band
  - Country
  - underserved_customers
  - avg_total_spend
  - avg_web_visits
  - response_rate_pct

## Page 6: Ideal Target Customers
- Visual:
  - Table from `ideal_target_customers.csv`
- Columns:
  - Age_Band
  - Income_Band
  - Family_Composition
  - Country
  - Education
  - Marital_Status
  - customer_count
  - avg_total_spend
  - response_rate_pct
- Supporting visual:
  - Bar chart of top ideal target combinations by `response_rate_pct`

## Tooltips / Takeaways
- Each page should include a short text box summarizing the main insight.
- Keep titles explicit and business-focused.
