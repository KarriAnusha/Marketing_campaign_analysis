# Marketing Campaign Analysis

This project is aligned to the `Marketing campaign analysis` proposal in Marketing Analytics / Customer Analytics.

## Deliverables
- Python cleaning and feature engineering:
  - [data_processing.py](C:\Users\Anusha\Desktop\marketing-campaign-analysis-dashboard\data_processing.py)
  - [notebooks/marketing_campaign_analysis.ipynb](C:\Users\Anusha\Desktop\marketing-campaign-analysis-dashboard\notebooks\marketing_campaign_analysis.ipynb)
- SQL modeling and analytical queries:
  - [sql/marketing_schema.sql](C:\Users\Anusha\Desktop\marketing-campaign-analysis-dashboard\sql\marketing_schema.sql)
  - [SQL_QUERIES.sql](C:\Users\Anusha\Desktop\marketing-campaign-analysis-dashboard\SQL_QUERIES.sql)
- Dashboard deliverable:
  - [streamlit_app.py](C:\Users\Anusha\Desktop\marketing-campaign-analysis-dashboard\streamlit_app.py)
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
1. `pip install -r requirements.txt`
2. `python data_processing.py`
3. `streamlit run streamlit_app.py`

## Dashboard coverage
The Streamlit dashboard includes:
- executive KPI cards
- campaign response by segment
- product spending analysis by age, income, marital status, and country
- channel usage for high-value customers
- under-served segment analysis
- ideal target customer profiling
- actionable recommendations
- interactive filters for `Country`, `Education`, `Marital_Status`, `Age_Band`, and `Income_Band`

## Python dependencies
Install from:
- [requirements.txt](C:\Users\Anusha\Desktop\marketing-campaign-analysis-dashboard\requirements.txt)

## Notes
- The SQL layer is retained because it is part of the proposal deliverables.
- The dashboard deliverable is Streamlit.
