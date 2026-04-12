# Marketing Campaign Analysis

This project is aligned to the `Marketing campaign analysis` proposal for Marketing Analytics / Customer Analytics.

## Deliverables
- Python data cleaning and feature engineering:
  - [data_processing.py](C:\Users\Anusha\Desktop\marketing-campaign-analysis-dashboard\data_processing.py)
  - [notebooks/marketing_campaign_analysis.ipynb](C:\Users\Anusha\Desktop\marketing-campaign-analysis-dashboard\notebooks\marketing_campaign_analysis.ipynb)
- SQL data model and analytical queries:
  - [sql/marketing_schema.sql](C:\Users\Anusha\Desktop\marketing-campaign-analysis-dashboard\sql\marketing_schema.sql)
  - [SQL_QUERIES.sql](C:\Users\Anusha\Desktop\marketing-campaign-analysis-dashboard\SQL_QUERIES.sql)
- Power BI-ready dashboard package:
  - [powerbi/README.md](C:\Users\Anusha\Desktop\marketing-campaign-analysis-dashboard\powerbi\README.md)
  - [powerbi/DASHBOARD_SPEC.md](C:\Users\Anusha\Desktop\marketing-campaign-analysis-dashboard\powerbi\DASHBOARD_SPEC.md)
  - [powerbi/data](C:\Users\Anusha\Desktop\marketing-campaign-analysis-dashboard\powerbi\data)
- Project report:
  - [REPORT.md](C:\Users\Anusha\Desktop\marketing-campaign-analysis-dashboard\REPORT.md)

## Data inputs
- `marketing_data.csv`
- `marketing_data_dictionary.csv`

## Derived fields created
- `Age`
- `Customer_Tenure_Days`
- `Customer_Tenure_Months`
- `Total_Spend`
- `Total_Purchases`
- `Children`
- `Income_Band`
- `Age_Band`
- `Primary_Segment`
- `High_Income`
- `Young_Customer`
- `Campaign_Responder`
- `High_Web_Engagement`
- `Family_Customer`
- `High_Spender`
- `High_Value_Customer`
- `Under_Served_Customer`

## Run order
1. `python data_processing.py`
2. `python build_sqlite_db.py`
3. `python export_powerbi_assets.py`

## Power BI build
Use the CSVs in `powerbi/data` and follow `powerbi/DASHBOARD_SPEC.md` to create the interactive dashboard in Power BI Desktop with slicers for:
- `Country`
- `Education`
- `Marital_Status`
- `Age_Band`
- `Income_Band`

## Notes
- The SQL model answers the proposal business questions through views and query scripts.
- The environment here did not expose Power BI Desktop, so a native `.pbix` file was not generated automatically.
