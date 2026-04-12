# Power BI Dashboard Package

This folder contains the Power BI-ready assets for the `Marketing campaign analysis` proposal.

## What is included
- `data/`
  - CSV extracts generated from the SQL layer for the dashboard
- `DASHBOARD_SPEC.md`
  - Exact page-by-page dashboard definition aligned to the proposal

## How to build the interactive Power BI dashboard
1. Run:
   - `python data_processing.py`
   - `python build_sqlite_db.py`
   - `python export_powerbi_assets.py`
2. Open Power BI Desktop.
3. Get Data -> Text/CSV.
4. Load the files from `powerbi/data/`.
5. Build the visuals exactly as defined in `DASHBOARD_SPEC.md`.
6. Add slicers for:
   - `Country`
   - `Education`
   - `Marital_Status`
   - `Age_Band`
   - `Income_Band`

## Note
The current environment does not expose Power BI Desktop tooling, so a native `.pbix` file could not be generated programmatically here. The data model, exported datasets, and dashboard blueprint are prepared for immediate import into Power BI Desktop.
