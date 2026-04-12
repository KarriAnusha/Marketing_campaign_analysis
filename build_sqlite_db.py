from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent
CLEANED_FILE = PROJECT_DIR / "cleaned_marketing_data.csv"
SCHEMA_FILE = PROJECT_DIR / "sql" / "marketing_schema.sql"
DB_FILE = PROJECT_DIR / "marketing_campaign_analysis.db"


def build_database() -> Path:
    if DB_FILE.exists():
        DB_FILE.unlink()

    df = pd.read_csv(CLEANED_FILE)
    conn = sqlite3.connect(DB_FILE)
    try:
        schema_sql = SCHEMA_FILE.read_text(encoding="utf-8")
        conn.executescript(schema_sql)
        df.to_sql("customers", conn, if_exists="append", index=False)
        conn.commit()
    finally:
        conn.close()
    return DB_FILE


if __name__ == "__main__":
    db_path = build_database()
    print(f"SQLite database created at {db_path}")
