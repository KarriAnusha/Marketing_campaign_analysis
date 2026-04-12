from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent
DB_FILE = PROJECT_DIR / "marketing_campaign_analysis.db"
OUTPUT_DIR = PROJECT_DIR / "powerbi" / "data"

QUERIES = {
    "kpi_overview.csv": """
        SELECT * FROM kpi_overview
    """,
    "segment_campaign_response.csv": """
        SELECT * FROM segment_campaign_response
    """,
    "spending_by_demographics.csv": """
        SELECT * FROM spending_by_demographics
    """,
    "channel_usage_high_value.csv": """
        SELECT * FROM channel_usage_high_value
    """,
    "underserved_segments.csv": """
        SELECT * FROM underserved_segments
    """,
    "ideal_target_customers.csv": """
        SELECT * FROM ideal_target_customers
    """,
    "segment_summary.csv": """
        SELECT * FROM segment_summary
    """,
}


def export_assets() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_FILE) as conn:
        for filename, query in QUERIES.items():
            df = pd.read_sql_query(query, conn)
            df.to_csv(OUTPUT_DIR / filename, index=False)


if __name__ == "__main__":
    export_assets()
    print(f"Power BI assets exported to {OUTPUT_DIR}")
