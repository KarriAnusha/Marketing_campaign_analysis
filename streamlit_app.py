from __future__ import annotations

from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

PROJECT_DIR = Path(__file__).resolve().parent
DATA_FILE = PROJECT_DIR / "cleaned_marketing_data.csv"

SPEND_COLUMNS = {
    "MntWines": "Wines",
    "MntFruits": "Fruits",
    "MntMeatProducts": "Meat",
    "MntFishProducts": "Fish",
    "MntSweetProducts": "Sweets",
    "MntGoldProds": "Gold",
}
CAMPAIGN_COLUMNS = {
    "AcceptedCmp1": "Campaign 1",
    "AcceptedCmp2": "Campaign 2",
    "AcceptedCmp3": "Campaign 3",
    "AcceptedCmp4": "Campaign 4",
    "AcceptedCmp5": "Campaign 5",
    "Response": "Final Campaign",
}
CHANNEL_COLUMNS = {
    "NumWebPurchases": "Web",
    "NumStorePurchases": "Store",
    "NumCatalogPurchases": "Catalog",
    "NumDealsPurchases": "Deals",
}


st.set_page_config(
    page_title="Marketing Campaign Analysis",
    page_icon=":bar_chart:",
    layout="wide",
)


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_FILE)
    df["Income_Band"] = df["Income_Band"].astype(str)
    df["Age_Band"] = df["Age_Band"].astype(str)
    return df


@st.cache_data
def get_data() -> pd.DataFrame:
    return load_data()


def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Dashboard Filters")
    countries = st.sidebar.multiselect("Country", sorted(df["Country"].dropna().unique()), default=sorted(df["Country"].dropna().unique()))
    education = st.sidebar.multiselect("Education", sorted(df["Education"].dropna().unique()), default=sorted(df["Education"].dropna().unique()))
    marital = st.sidebar.multiselect("Marital Status", sorted(df["Marital_Status"].dropna().unique()), default=sorted(df["Marital_Status"].dropna().unique()))
    age_band = st.sidebar.multiselect("Age Band", sorted(df["Age_Band"].dropna().unique()), default=sorted(df["Age_Band"].dropna().unique()))
    income_band = st.sidebar.multiselect("Income Band", sorted(df["Income_Band"].dropna().unique()), default=sorted(df["Income_Band"].dropna().unique()))

    filtered = df[
        df["Country"].isin(countries)
        & df["Education"].isin(education)
        & df["Marital_Status"].isin(marital)
        & df["Age_Band"].isin(age_band)
        & df["Income_Band"].isin(income_band)
    ].copy()
    return filtered


def format_inr(value: float) -> str:
    return f"Rs {value:,.2f}"


def metric_block(df: pd.DataFrame) -> None:
    total_customers = len(df)
    avg_spend = df["Total_Spend"].mean()
    avg_income = df["Income"].mean()
    response_rate = df["Response"].mean() * 100
    avg_web_visits = df["NumWebVisitsMonth"].mean()
    avg_total_purchases = df["Total_Purchases"].mean()

    cols = st.columns(6)
    cols[0].metric("Total Customers", f"{total_customers:,}")
    cols[1].metric("Avg Total Spend", format_inr(avg_spend))
    cols[2].metric("Avg Income", format_inr(avg_income))
    cols[3].metric("Response Rate", f"{response_rate:.2f}%")
    cols[4].metric("Avg Web Visits", f"{avg_web_visits:.2f}")
    cols[5].metric("Avg Total Purchases", f"{avg_total_purchases:.2f}")


def chart_segment_response(df: pd.DataFrame) -> None:
    segment_summary = (
        df.groupby("Primary_Segment", as_index=False)
        .agg(
            customer_count=("ID", "count"),
            AcceptedCmp1=("AcceptedCmp1", "mean"),
            AcceptedCmp2=("AcceptedCmp2", "mean"),
            AcceptedCmp3=("AcceptedCmp3", "mean"),
            AcceptedCmp4=("AcceptedCmp4", "mean"),
            AcceptedCmp5=("AcceptedCmp5", "mean"),
            Response=("Response", "mean"),
        )
    )
    for column in CAMPAIGN_COLUMNS:
        segment_summary[column] = segment_summary[column] * 100

    chart_data = segment_summary.melt(
        id_vars=["Primary_Segment", "customer_count"],
        value_vars=list(CAMPAIGN_COLUMNS.keys()),
        var_name="Campaign",
        value_name="Response Rate (%)",
    )
    chart_data["Campaign"] = chart_data["Campaign"].map(CAMPAIGN_COLUMNS)

    chart = (
        alt.Chart(chart_data)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("Primary_Segment:N", title="Primary Segment", sort="-y"),
            y=alt.Y("Response Rate (%):Q", title="Response Rate (%)"),
            color=alt.Color("Campaign:N", scale=alt.Scale(scheme="tealblues")),
            tooltip=["Primary_Segment", "Campaign", alt.Tooltip("Response Rate (%):Q", format=".2f")],
        )
        .properties(height=360)
    )

    st.subheader("Campaign Response Rate by Segment")
    st.altair_chart(chart, use_container_width=True)
    st.dataframe(
        segment_summary.rename(columns={col: label for col, label in CAMPAIGN_COLUMNS.items()}),
        use_container_width=True,
        hide_index=True,
    )


def chart_product_spending(df: pd.DataFrame) -> None:
    st.subheader("Product Spending by Demographic")
    dimension = st.selectbox(
        "Compare spending across",
        ["Age_Band", "Income_Band", "Marital_Status", "Country"],
        index=0,
    )
    grouped = df.groupby(dimension, as_index=False)[list(SPEND_COLUMNS.keys())].mean()
    grouped = grouped.rename(columns=SPEND_COLUMNS)
    chart_data = grouped.melt(id_vars=[dimension], var_name="Product", value_name="Average Spend")

    chart = (
        alt.Chart(chart_data)
        .mark_bar()
        .encode(
            x=alt.X(f"{dimension}:N", title=dimension.replace("_", " ")),
            y=alt.Y("Average Spend:Q", title="Average Spend"),
            color=alt.Color("Product:N", scale=alt.Scale(scheme="tableau20")),
            tooltip=[dimension, "Product", alt.Tooltip("Average Spend:Q", format=".2f")],
        )
        .properties(height=360)
    )
    st.altair_chart(chart, use_container_width=True)


def chart_channel_usage(df: pd.DataFrame) -> None:
    st.subheader("Channel Usage for High-Value Customers")
    high_value = df[df["High_Value_Customer"] == 1].copy()
    if high_value.empty:
        st.info("No high-value customers match the current filters.")
        return

    grouped = high_value.groupby("Primary_Segment", as_index=False)[list(CHANNEL_COLUMNS.keys()) + ["NumWebVisitsMonth", "Total_Spend", "Response"]].mean()
    chart_data = grouped.melt(
        id_vars=["Primary_Segment"],
        value_vars=list(CHANNEL_COLUMNS.keys()),
        var_name="Channel",
        value_name="Average Purchases",
    )
    chart_data["Channel"] = chart_data["Channel"].map(CHANNEL_COLUMNS)

    chart = (
        alt.Chart(chart_data)
        .mark_bar()
        .encode(
            x=alt.X("Primary_Segment:N", title="Primary Segment"),
            y=alt.Y("Average Purchases:Q", title="Average Purchases"),
            color=alt.Color("Channel:N", scale=alt.Scale(scheme="set2")),
            tooltip=["Primary_Segment", "Channel", alt.Tooltip("Average Purchases:Q", format=".2f")],
        )
        .properties(height=360)
    )
    st.altair_chart(chart, use_container_width=True)

    cols = st.columns(3)
    cols[0].metric("Avg Spend of High-Value Customers", format_inr(high_value["Total_Spend"].mean()))
    cols[1].metric("Avg Web Visits", f"{high_value['NumWebVisitsMonth'].mean():.2f}")
    cols[2].metric("Response Rate", f"{high_value['Response'].mean() * 100:.2f}%")


def underserved_segments(df: pd.DataFrame) -> None:
    st.subheader("Under-Served Segments")
    underserved = df[
        (df["Total_Spend"] <= df["Total_Spend"].median())
        & (df["NumWebVisitsMonth"] > 5)
        & (df["Response"] == 0)
    ]
    if underserved.empty:
        st.info("No under-served segments match the current filters.")
        return

    summary = (
        underserved.groupby(["Primary_Segment", "Age_Band", "Income_Band", "Country"], as_index=False)
        .agg(
            underserved_customers=("ID", "count"),
            avg_total_spend=("Total_Spend", "mean"),
            avg_web_visits=("NumWebVisitsMonth", "mean"),
            response_rate_pct=("Response", lambda s: s.mean() * 100),
        )
        .sort_values(["underserved_customers", "avg_web_visits"], ascending=[False, False])
    )
    st.dataframe(
        summary.style.format(
            {
                "avg_total_spend": "{:.2f}",
                "avg_web_visits": "{:.2f}",
                "response_rate_pct": "{:.2f}",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )


def ideal_target_customers(df: pd.DataFrame) -> None:
    st.subheader("Ideal Target Customers")
    ideal = df[(df["Response"] == 1) | (df["High_Value_Customer"] == 1)]
    if ideal.empty:
        st.info("No ideal target profiles match the current filters.")
        return

    summary = (
        ideal.groupby(
            ["Age_Band", "Income_Band", "Family_Composition", "Country", "Education", "Marital_Status"],
            as_index=False,
        )
        .agg(
            customer_count=("ID", "count"),
            avg_total_spend=("Total_Spend", "mean"),
            response_rate_pct=("Response", lambda s: s.mean() * 100),
            avg_web_purchases=("NumWebPurchases", "mean"),
            avg_store_purchases=("NumStorePurchases", "mean"),
            avg_catalog_purchases=("NumCatalogPurchases", "mean"),
        )
    )
    summary = summary[summary["customer_count"] >= 10].sort_values(
        ["response_rate_pct", "avg_total_spend"],
        ascending=[False, False],
    )

    st.dataframe(
        summary.style.format(
            {
                "avg_total_spend": "{:.2f}",
                "response_rate_pct": "{:.2f}",
                "avg_web_purchases": "{:.2f}",
                "avg_store_purchases": "{:.2f}",
                "avg_catalog_purchases": "{:.2f}",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )


def recommendations(df: pd.DataFrame) -> None:
    st.subheader("Actionable Recommendations")
    segment_summary = (
        df.groupby("Primary_Segment", as_index=False)
        .agg(
            customer_count=("ID", "count"),
            avg_total_spend=("Total_Spend", "mean"),
            response_rate_pct=("Response", lambda s: s.mean() * 100),
        )
        .sort_values("response_rate_pct", ascending=False)
    )
    top_response_segment = segment_summary.iloc[0]
    top_spend_segment = segment_summary.sort_values("avg_total_spend", ascending=False).iloc[0]
    product_spend = df[list(SPEND_COLUMNS.keys())].mean().sort_values(ascending=False)
    top_product = SPEND_COLUMNS[product_spend.index[0]]
    underserved_count = len(
        df[(df["Total_Spend"] <= df["Total_Spend"].median()) & (df["NumWebVisitsMonth"] > 5) & (df["Response"] == 0)]
    )
    high_value_rate = df[df["High_Value_Customer"] == 1]["Response"].mean() * 100 if (df["High_Value_Customer"] == 1).any() else 0
    family_rate = df[df["Family_Customer"] == 1]["Response"].mean() * 100 if (df["Family_Customer"] == 1).any() else 0

    recs = [
        f"Prioritize {top_response_segment['Primary_Segment']} customers because they have the highest response rate in the current filtered view ({top_response_segment['response_rate_pct']:.2f}%).",
        f"Use premium or bundle offers for {top_spend_segment['Primary_Segment']} customers because they deliver the highest average spend ({top_spend_segment['avg_total_spend']:.2f}).",
        f"Lead future campaign creatives with {top_product} because it is the strongest spending category in the filtered population.",
        f"Focus web-conversion tactics on under-served groups because {underserved_count:,} customers show low spend, high visits, and low response.",
        f"Retain and upsell high-value customers because their response rate is {high_value_rate:.2f}% in the current slice.",
        f"Test family-oriented offers where relevant because family customers currently show a response rate of {family_rate:.2f}%.",
    ]
    for rec in recs:
        st.markdown(f"- {rec}")


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(15, 118, 110, 0.10), transparent 26%),
                radial-gradient(circle at top right, rgba(14, 165, 233, 0.08), transparent 24%),
                #f7faf9;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        div[data-testid="stMetric"] {
            background: white;
            border: 1px solid rgba(15, 23, 42, 0.08);
            padding: 1rem;
            border-radius: 1rem;
            box-shadow: 0 12px 24px rgba(15, 23, 42, 0.05);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    inject_styles()
    st.title("Marketing Campaign Analysis Dashboard")
    st.caption("Proposal-aligned Streamlit dashboard for customer analytics, campaign response, segmentation, and targeting.")

    df = get_data()
    filtered = filter_data(df)

    if filtered.empty:
        st.warning("No records match the selected filters. Please broaden your selections.")
        return

    metric_block(filtered)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "Executive KPIs",
            "Segment Response",
            "Product Spending",
            "Channel Usage",
            "Under-Served Segments",
            "Ideal Targets & Recommendations",
        ]
    )

    with tab1:
        overall_campaign = pd.DataFrame(
            {
                "Campaign": [label for label in CAMPAIGN_COLUMNS.values()],
                "Acceptance Rate (%)": [(filtered[column].mean() * 100) for column in CAMPAIGN_COLUMNS],
            }
        )
        chart = (
            alt.Chart(overall_campaign)
            .mark_bar(color="#0f766e", cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
            .encode(
                x=alt.X("Campaign:N", title="Campaign"),
                y=alt.Y("Acceptance Rate (%):Q", title="Acceptance Rate (%)"),
                tooltip=["Campaign", alt.Tooltip("Acceptance Rate (%):Q", format=".2f")],
            )
            .properties(height=340)
        )
        st.subheader("Overall Campaign Acceptance")
        st.altair_chart(chart, use_container_width=True)

    with tab2:
        chart_segment_response(filtered)

    with tab3:
        chart_product_spending(filtered)

    with tab4:
        chart_channel_usage(filtered)

    with tab5:
        underserved_segments(filtered)

    with tab6:
        ideal_target_customers(filtered)
        recommendations(filtered)


if __name__ == "__main__":
    main()
