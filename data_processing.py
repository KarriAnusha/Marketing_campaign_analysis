from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent
DATA_FILE = PROJECT_DIR / "data" / "raw" / "marketing_data.csv"
DICTIONARY_FILE = PROJECT_DIR / "data" / "raw" / "marketing_data_dictionary.csv"
CLEANED_FILE = PROJECT_DIR / "data" / "processed" / "cleaned_marketing_data.csv"

REFERENCE_DATE = pd.Timestamp("2015-01-01")
SPEND_COLUMNS = [
    "MntWines",
    "MntFruits",
    "MntMeatProducts",
    "MntFishProducts",
    "MntSweetProducts",
    "MntGoldProds",
]
CHANNEL_COLUMNS = [
    "NumDealsPurchases",
    "NumWebPurchases",
    "NumCatalogPurchases",
    "NumStorePurchases",
]
CAMPAIGN_COLUMNS = [
    "AcceptedCmp1",
    "AcceptedCmp2",
    "AcceptedCmp3",
    "AcceptedCmp4",
    "AcceptedCmp5",
    "Response",
]
REQUIRED_COLUMNS = [
    "ID",
    "Year_Birth",
    "Education",
    "Marital_Status",
    "Income",
    "Kidhome",
    "Teenhome",
    "Dt_Customer",
    "Recency",
    *SPEND_COLUMNS,
    *CHANNEL_COLUMNS,
    "NumWebVisitsMonth",
    *CAMPAIGN_COLUMNS,
    "Complain",
    "Country",
]


def load_dictionary(file_path: Path | str = DICTIONARY_FILE) -> pd.DataFrame:
    dictionary = pd.read_csv(file_path)
    dictionary["Field"] = dictionary["Field"].astype(str).str.strip()
    return dictionary


def load_raw_data(file_path: Path | str = DATA_FILE) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    df.columns = [col.strip() for col in df.columns]
    return df


def validate_columns(df: pd.DataFrame, dictionary: pd.DataFrame) -> None:
    dictionary_fields = set(dictionary["Field"].tolist())
    missing_in_data = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_in_data:
        raise ValueError(f"Source data is missing required columns: {missing_in_data}")

    missing_in_dictionary = [col for col in REQUIRED_COLUMNS if col not in dictionary_fields]
    if missing_in_dictionary:
        raise ValueError(f"Dictionary is missing required column definitions: {missing_in_dictionary}")


def add_demographic_derivations(clean: pd.DataFrame) -> pd.DataFrame:
    clean["Year_Birth"] = pd.to_numeric(clean["Year_Birth"], errors="coerce")
    clean["Age"] = REFERENCE_DATE.year - clean["Year_Birth"]
    clean.loc[(clean["Age"] < 18) | (clean["Age"] > 100), "Age"] = np.nan
    clean["Age"] = clean["Age"].fillna(clean["Age"].median()).round().astype(int)

    clean["Children"] = (
        pd.to_numeric(clean["Kidhome"], errors="coerce").fillna(0).astype(int)
        + pd.to_numeric(clean["Teenhome"], errors="coerce").fillna(0).astype(int)
    )

    clean["Family_Composition"] = np.select(
        [clean["Children"] == 0, clean["Children"] == 1, clean["Children"] >= 2],
        ["No Children", "One Child", "Two or More Children"],
        default="Unknown",
    )
    return clean


def add_customer_tenure(clean: pd.DataFrame) -> pd.DataFrame:
    clean["Dt_Customer"] = pd.to_datetime(clean["Dt_Customer"], errors="coerce")
    clean["Customer_Tenure_Days"] = (REFERENCE_DATE - clean["Dt_Customer"]).dt.days
    clean.loc[clean["Customer_Tenure_Days"] < 0, "Customer_Tenure_Days"] = np.nan
    clean["Customer_Tenure_Days"] = clean["Customer_Tenure_Days"].fillna(
        clean["Customer_Tenure_Days"].median()
    )
    clean["Customer_Tenure_Months"] = (clean["Customer_Tenure_Days"] / 30.4).round(1)
    return clean


def clean_numeric_fields(clean: pd.DataFrame) -> pd.DataFrame:
    numeric_columns = [
        "Income",
        "Recency",
        "NumWebVisitsMonth",
        "Kidhome",
        "Teenhome",
        "Complain",
        *SPEND_COLUMNS,
        *CHANNEL_COLUMNS,
        *CAMPAIGN_COLUMNS,
    ]
    for column in numeric_columns:
        clean[column] = pd.to_numeric(clean[column], errors="coerce")

    clean.loc[clean["Income"] <= 0, "Income"] = np.nan
    clean["Income"] = clean["Income"].fillna(clean["Income"].median())

    clean.loc[clean["Recency"] < 0, "Recency"] = np.nan
    clean["Recency"] = clean["Recency"].fillna(clean["Recency"].median())

    clean.loc[clean["NumWebVisitsMonth"] < 0, "NumWebVisitsMonth"] = np.nan
    clean["NumWebVisitsMonth"] = clean["NumWebVisitsMonth"].fillna(clean["NumWebVisitsMonth"].median())

    for column in SPEND_COLUMNS + CHANNEL_COLUMNS + CAMPAIGN_COLUMNS + ["Complain"]:
        clean.loc[clean[column] < 0, column] = 0
        clean[column] = clean[column].fillna(0)

    # Winsorize only the fields already present at this stage.
    for column in ["Income", "Recency"]:
        lower = clean[column].quantile(0.01)
        upper = clean[column].quantile(0.99)
        clean[column] = clean[column].clip(lower=lower, upper=upper)

    return clean


def add_behavioral_derivations(clean: pd.DataFrame) -> pd.DataFrame:
    clean["Total_Spend"] = clean[SPEND_COLUMNS].sum(axis=1)
    clean["Total_Purchases"] = clean[CHANNEL_COLUMNS].sum(axis=1)
    clean["Accepted_Campaigns_Total"] = clean[CAMPAIGN_COLUMNS[:-1]].sum(axis=1)
    clean["Web_Purchase_Share"] = np.where(
        clean["Total_Purchases"] > 0,
        clean["NumWebPurchases"] / clean["Total_Purchases"],
        0,
    ).round(3)
    clean["Channel_Preference"] = np.select(
        [
            clean["NumWebPurchases"] >= clean[["NumCatalogPurchases", "NumStorePurchases", "NumDealsPurchases"]].max(axis=1),
            clean["NumStorePurchases"] >= clean[["NumCatalogPurchases", "NumDealsPurchases"]].max(axis=1),
            clean["NumCatalogPurchases"] >= clean["NumDealsPurchases"],
        ],
        ["Web", "Store", "Catalog"],
        default="Deals",
    )
    return clean


def add_bands(clean: pd.DataFrame) -> pd.DataFrame:
    age_lower = clean["Age"].quantile(0.01)
    age_upper = clean["Age"].quantile(0.99)
    clean["Age"] = clean["Age"].clip(lower=age_lower, upper=age_upper).round().astype(int)

    clean["Income_Band"] = pd.cut(
        clean["Income"],
        bins=[0, 30000, 60000, 75000, 100000, np.inf],
        labels=["Low", "Medium", "Upper-Mid", "High", "Very High"],
        include_lowest=True,
    )
    clean["Age_Band"] = pd.cut(
        clean["Age"],
        bins=[17, 29, 39, 49, 59, np.inf],
        labels=["18-29", "30-39", "40-49", "50-59", "60+"],
        include_lowest=True,
    )
    return clean


def add_rule_based_segments(clean: pd.DataFrame) -> pd.DataFrame:
    high_spender_cutoff = clean["Total_Spend"].quantile(0.9)

    clean["High_Income"] = (clean["Income"] > 75000).astype(int)
    clean["Young_Customer"] = (clean["Age"] < 30).astype(int)
    clean["Campaign_Responder"] = (clean["Response"] == 1).astype(int)
    clean["High_Web_Engagement"] = (clean["NumWebVisitsMonth"] > 5).astype(int)
    clean["Family_Customer"] = (clean["Children"] > 0).astype(int)
    clean["High_Spender"] = (clean["Total_Spend"] > high_spender_cutoff).astype(int)
    clean["High_Value_Customer"] = (
        (clean["High_Income"] == 1) & (clean["High_Spender"] == 1)
    ).astype(int)
    clean["Under_Served_Customer"] = (
        (clean["Total_Spend"] <= clean["Total_Spend"].quantile(0.5))
        & (clean["NumWebVisitsMonth"] > 5)
        & (clean["Response"] == 0)
    ).astype(int)

    segment_columns = [
        "High_Income",
        "Young_Customer",
        "Campaign_Responder",
        "High_Web_Engagement",
        "Family_Customer",
        "High_Spender",
    ]
    segment_names = [
        "High Income",
        "Young Customer",
        "Campaign Responder",
        "High Web Engagement",
        "Family Customer",
        "High Spender",
    ]
    conditions = [clean[column] == 1 for column in segment_columns]
    clean["Primary_Segment"] = np.select(conditions, segment_names, default="Regular")
    return clean


def normalize_categories(clean: pd.DataFrame) -> pd.DataFrame:
    clean["Education"] = clean["Education"].astype(str).str.strip()
    clean["Marital_Status"] = clean["Marital_Status"].astype(str).str.strip()
    clean["Country"] = clean["Country"].astype(str).str.strip()
    return clean


def clean_marketing_data(df: pd.DataFrame, dictionary: pd.DataFrame | None = None) -> pd.DataFrame:
    dictionary = dictionary if dictionary is not None else load_dictionary()
    validate_columns(df, dictionary)

    clean = df.copy()
    clean.columns = [col.strip() for col in clean.columns]

    clean = normalize_categories(clean)
    clean = clean_numeric_fields(clean)
    clean = add_demographic_derivations(clean)
    clean = add_customer_tenure(clean)
    clean = add_behavioral_derivations(clean)
    clean = add_bands(clean)
    clean = add_rule_based_segments(clean)

    ordered_columns = REQUIRED_COLUMNS + [
        "Age",
        "Children",
        "Family_Composition",
        "Total_Spend",
        "Total_Purchases",
        "Accepted_Campaigns_Total",
        "Customer_Tenure_Days",
        "Customer_Tenure_Months",
        "Income_Band",
        "Age_Band",
        "Channel_Preference",
        "Primary_Segment",
        "High_Income",
        "Young_Customer",
        "Campaign_Responder",
        "High_Web_Engagement",
        "Family_Customer",
        "High_Spender",
        "High_Value_Customer",
        "Under_Served_Customer",
        "Web_Purchase_Share",
    ]
    return clean[ordered_columns]


def export_cleaned_data(df: pd.DataFrame, output_path: Path | str = CLEANED_FILE) -> None:
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    dictionary_df = load_dictionary()
    raw_df = load_raw_data()
    cleaned_df = clean_marketing_data(raw_df, dictionary_df)
    export_cleaned_data(cleaned_df)
    print(f"Cleaned data exported to {CLEANED_FILE}")
