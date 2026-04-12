-- Marketing Campaign Analysis SQL Queries
-- These queries align directly with the proposal business questions.

-- 1. KPI overview
SELECT * FROM kpi_overview;

-- 2. Overall and campaign-wise response rate by customer segment
SELECT * FROM segment_campaign_response
ORDER BY final_campaign_response_rate_pct DESC, customer_count DESC;

-- 3. Segment-level KPI summary
SELECT * FROM segment_summary
ORDER BY avg_total_spend DESC;

-- 4. Product spending patterns by age, income, marital status, and country
SELECT *
FROM spending_by_demographics
ORDER BY avg_total_spend DESC;

-- 5. Channel usage for high-value customers
SELECT *
FROM channel_usage_high_value
ORDER BY avg_total_spend DESC;

-- 6. Under-served segments: low spend, high visits, low response
SELECT *
FROM underserved_segments
ORDER BY underserved_customers DESC, avg_web_visits DESC;

-- 7. Characteristics of ideal future target customers
SELECT *
FROM ideal_target_customers
ORDER BY response_rate_pct DESC, avg_total_spend DESC;

-- 8. Segment summary by demographic lenses for dashboard slicers
SELECT
  Age_Band,
  Income_Band,
  Education,
  Marital_Status,
  Country,
  COUNT(*) AS customer_count,
  ROUND(AVG(Total_Spend), 2) AS avg_total_spend,
  ROUND(AVG(Response) * 100.0, 2) AS response_rate_pct
FROM customers
GROUP BY Age_Band, Income_Band, Education, Marital_Status, Country
ORDER BY response_rate_pct DESC;

-- 9. Campaign acceptance totals
SELECT
  SUM(AcceptedCmp1) AS accepted_cmp1_total,
  SUM(AcceptedCmp2) AS accepted_cmp2_total,
  SUM(AcceptedCmp3) AS accepted_cmp3_total,
  SUM(AcceptedCmp4) AS accepted_cmp4_total,
  SUM(AcceptedCmp5) AS accepted_cmp5_total,
  SUM(Response) AS final_campaign_response_total
FROM customers;
