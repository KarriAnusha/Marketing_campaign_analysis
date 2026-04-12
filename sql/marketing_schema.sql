DROP TABLE IF EXISTS customers;
DROP VIEW IF EXISTS kpi_overview;
DROP VIEW IF EXISTS segment_summary;
DROP VIEW IF EXISTS segment_campaign_response;
DROP VIEW IF EXISTS spending_by_demographics;
DROP VIEW IF EXISTS channel_usage_high_value;
DROP VIEW IF EXISTS underserved_segments;
DROP VIEW IF EXISTS ideal_target_customers;

CREATE TABLE customers (
  ID INTEGER PRIMARY KEY,
  Year_Birth INTEGER,
  Education TEXT,
  Marital_Status TEXT,
  Income REAL,
  Kidhome INTEGER,
  Teenhome INTEGER,
  Dt_Customer TEXT,
  Recency REAL,
  MntWines REAL,
  MntFruits REAL,
  MntMeatProducts REAL,
  MntFishProducts REAL,
  MntSweetProducts REAL,
  MntGoldProds REAL,
  NumDealsPurchases REAL,
  NumWebPurchases REAL,
  NumCatalogPurchases REAL,
  NumStorePurchases REAL,
  NumWebVisitsMonth REAL,
  AcceptedCmp1 INTEGER,
  AcceptedCmp2 INTEGER,
  AcceptedCmp3 INTEGER,
  AcceptedCmp4 INTEGER,
  AcceptedCmp5 INTEGER,
  Response INTEGER,
  Complain INTEGER,
  Country TEXT,
  Age INTEGER,
  Children INTEGER,
  Family_Composition TEXT,
  Total_Spend REAL,
  Total_Purchases REAL,
  Accepted_Campaigns_Total REAL,
  Customer_Tenure_Days REAL,
  Customer_Tenure_Months REAL,
  Income_Band TEXT,
  Age_Band TEXT,
  Channel_Preference TEXT,
  Primary_Segment TEXT,
  High_Income INTEGER,
  Young_Customer INTEGER,
  Campaign_Responder INTEGER,
  High_Web_Engagement INTEGER,
  Family_Customer INTEGER,
  High_Spender INTEGER,
  High_Value_Customer INTEGER,
  Under_Served_Customer INTEGER,
  Web_Purchase_Share REAL
);

CREATE VIEW kpi_overview AS
SELECT
  COUNT(*) AS total_customers,
  ROUND(AVG(Total_Spend), 2) AS avg_total_spend,
  ROUND(AVG(Income), 2) AS avg_income,
  ROUND(AVG(Response) * 100.0, 2) AS response_rate_pct,
  ROUND(AVG(NumWebVisitsMonth), 2) AS avg_web_visits,
  ROUND(AVG(Total_Purchases), 2) AS avg_total_purchases
FROM customers;

CREATE VIEW segment_summary AS
SELECT
  Primary_Segment,
  COUNT(*) AS customer_count,
  ROUND(AVG(Income), 2) AS avg_income,
  ROUND(AVG(Total_Spend), 2) AS avg_total_spend,
  ROUND(AVG(Total_Purchases), 2) AS avg_total_purchases,
  ROUND(AVG(NumWebVisitsMonth), 2) AS avg_web_visits,
  ROUND(AVG(Response) * 100.0, 2) AS response_rate_pct
FROM customers
GROUP BY Primary_Segment;

CREATE VIEW segment_campaign_response AS
SELECT
  Primary_Segment,
  COUNT(*) AS customer_count,
  ROUND(AVG(AcceptedCmp1) * 100.0, 2) AS accepted_cmp1_rate_pct,
  ROUND(AVG(AcceptedCmp2) * 100.0, 2) AS accepted_cmp2_rate_pct,
  ROUND(AVG(AcceptedCmp3) * 100.0, 2) AS accepted_cmp3_rate_pct,
  ROUND(AVG(AcceptedCmp4) * 100.0, 2) AS accepted_cmp4_rate_pct,
  ROUND(AVG(AcceptedCmp5) * 100.0, 2) AS accepted_cmp5_rate_pct,
  ROUND(AVG(Response) * 100.0, 2) AS final_campaign_response_rate_pct
FROM customers
GROUP BY Primary_Segment;

CREATE VIEW spending_by_demographics AS
SELECT
  Age_Band,
  Income_Band,
  Marital_Status,
  Country,
  ROUND(AVG(MntWines), 2) AS avg_wines,
  ROUND(AVG(MntFruits), 2) AS avg_fruits,
  ROUND(AVG(MntMeatProducts), 2) AS avg_meat,
  ROUND(AVG(MntFishProducts), 2) AS avg_fish,
  ROUND(AVG(MntSweetProducts), 2) AS avg_sweets,
  ROUND(AVG(MntGoldProds), 2) AS avg_gold,
  ROUND(AVG(Total_Spend), 2) AS avg_total_spend,
  ROUND(AVG(Response) * 100.0, 2) AS response_rate_pct
FROM customers
GROUP BY Age_Band, Income_Band, Marital_Status, Country;

CREATE VIEW channel_usage_high_value AS
SELECT
  Primary_Segment,
  ROUND(AVG(NumWebPurchases), 2) AS avg_web_purchases,
  ROUND(AVG(NumStorePurchases), 2) AS avg_store_purchases,
  ROUND(AVG(NumCatalogPurchases), 2) AS avg_catalog_purchases,
  ROUND(AVG(NumDealsPurchases), 2) AS avg_deals_purchases,
  ROUND(AVG(NumWebVisitsMonth), 2) AS avg_web_visits,
  ROUND(AVG(Total_Spend), 2) AS avg_total_spend,
  ROUND(AVG(Response) * 100.0, 2) AS response_rate_pct
FROM customers
WHERE High_Value_Customer = 1
GROUP BY Primary_Segment;

CREATE VIEW underserved_segments AS
SELECT
  Primary_Segment,
  Age_Band,
  Income_Band,
  Country,
  COUNT(*) AS underserved_customers,
  ROUND(AVG(Total_Spend), 2) AS avg_total_spend,
  ROUND(AVG(NumWebVisitsMonth), 2) AS avg_web_visits,
  ROUND(AVG(Response) * 100.0, 2) AS response_rate_pct
FROM customers
WHERE Under_Served_Customer = 1
GROUP BY Primary_Segment, Age_Band, Income_Band, Country
ORDER BY underserved_customers DESC;

CREATE VIEW ideal_target_customers AS
SELECT
  Age_Band,
  Income_Band,
  Family_Composition,
  Country,
  Education,
  Marital_Status,
  COUNT(*) AS customer_count,
  ROUND(AVG(Total_Spend), 2) AS avg_total_spend,
  ROUND(AVG(Response) * 100.0, 2) AS response_rate_pct,
  ROUND(AVG(NumWebPurchases), 2) AS avg_web_purchases,
  ROUND(AVG(NumStorePurchases), 2) AS avg_store_purchases,
  ROUND(AVG(NumCatalogPurchases), 2) AS avg_catalog_purchases
FROM customers
WHERE Response = 1 OR High_Value_Customer = 1
GROUP BY Age_Band, Income_Band, Family_Composition, Country, Education, Marital_Status
HAVING COUNT(*) >= 10
ORDER BY response_rate_pct DESC, avg_total_spend DESC;
