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

-- 10. Rule-based segmentation using CASE statements (SQL-native derivation)
-- This mirrors the Python segmentation logic directly in SQL.
SELECT
  ID,
  Income,
  Age,
  Response,
  NumWebVisitsMonth,
  Children,
  Total_Spend,
  CASE
    WHEN Income > 75000                                          THEN 'High Income'
    WHEN Age < 30                                               THEN 'Young Customer'
    WHEN Response = 1                                           THEN 'Campaign Responder'
    WHEN NumWebVisitsMonth > 5                                  THEN 'High Web Engagement'
    WHEN Children > 0                                           THEN 'Family Customer'
    WHEN Total_Spend > (
      SELECT Total_Spend
      FROM customers
      ORDER BY Total_Spend
      LIMIT 1
      OFFSET CAST(ROUND(0.9 * (SELECT COUNT(*) FROM customers)) AS INTEGER) - 1
    )                                                           THEN 'High Spender'
    ELSE 'Regular'
  END AS Derived_Segment
FROM customers;

-- 11. Segment-level KPIs summarised with CASE-based grouping (aggregation on derived segment)
SELECT
  CASE
    WHEN Income > 75000          THEN 'High Income'
    WHEN Age < 30                THEN 'Young Customer'
    WHEN Response = 1            THEN 'Campaign Responder'
    WHEN NumWebVisitsMonth > 5   THEN 'High Web Engagement'
    WHEN Children > 0            THEN 'Family Customer'
    ELSE 'Regular'
  END AS Derived_Segment,
  COUNT(*)                                       AS customer_count,
  ROUND(AVG(Total_Spend), 2)                     AS avg_total_spend,
  ROUND(AVG(Income), 2)                          AS avg_income,
  ROUND(AVG(Response) * 100.0, 2)               AS response_rate_pct
FROM customers
GROUP BY Derived_Segment
ORDER BY response_rate_pct DESC;

-- 12. Customer spend ranking within each segment using window functions
-- ROW_NUMBER to rank customers by spend within their segment.
SELECT
  ID,
  Primary_Segment,
  Income,
  Total_Spend,
  Response,
  ROW_NUMBER() OVER (
    PARTITION BY Primary_Segment ORDER BY Total_Spend DESC
  ) AS spend_rank_in_segment,
  ROUND(AVG(Total_Spend) OVER (PARTITION BY Primary_Segment), 2) AS avg_segment_spend,
  ROUND(Total_Spend - AVG(Total_Spend) OVER (PARTITION BY Primary_Segment), 2) AS spend_vs_segment_avg
FROM customers;

-- 13. Cumulative spend share by country (window function — running total)
-- Shows what percentage of total spend each country contributes cumulatively.
SELECT
  Country,
  ROUND(SUM(Total_Spend), 2)                                              AS country_total_spend,
  ROUND(
    SUM(SUM(Total_Spend)) OVER (ORDER BY SUM(Total_Spend) DESC)
    / SUM(SUM(Total_Spend)) OVER () * 100.0, 2
  )                                                                        AS cumulative_spend_share_pct
FROM customers
GROUP BY Country
ORDER BY country_total_spend DESC;

-- 14. Response rate percentile rank per income band (window function — NTILE)
-- Divides customers into 4 income quartiles and computes response rate per quartile.
SELECT
  income_quartile,
  COUNT(*)                               AS customer_count,
  ROUND(AVG(Response) * 100.0, 2)       AS response_rate_pct,
  ROUND(AVG(Total_Spend), 2)            AS avg_total_spend
FROM (
  SELECT
    Response,
    Total_Spend,
    NTILE(4) OVER (ORDER BY Income) AS income_quartile
  FROM customers
) ranked
GROUP BY income_quartile
ORDER BY income_quartile;
