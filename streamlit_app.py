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
    "Response": "Response Flag",
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


INCOME_BAND_ORDER = ["Low", "Medium", "Upper-Mid", "High", "Very High"]
AGE_BAND_ORDER = ["18-29", "30-39", "40-49", "50-59", "60+"]


def _ordered_options(series: pd.Series, order: list[str]) -> list[str]:
    present = set(series.dropna().unique())
    return [v for v in order if v in present]


def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Dashboard Filters")
    countries = st.sidebar.multiselect("Country", sorted(df["Country"].dropna().unique()), default=sorted(df["Country"].dropna().unique()))
    education = st.sidebar.multiselect("Education", sorted(df["Education"].dropna().unique()), default=sorted(df["Education"].dropna().unique()))
    marital = st.sidebar.multiselect("Marital Status", sorted(df["Marital_Status"].dropna().unique()), default=sorted(df["Marital_Status"].dropna().unique()))
    age_band_options = _ordered_options(df["Age_Band"], AGE_BAND_ORDER)
    age_band = st.sidebar.multiselect("Age Band", age_band_options, default=age_band_options)
    income_band_options = _ordered_options(df["Income_Band"], INCOME_BAND_ORDER)
    income_band = st.sidebar.multiselect("Income Band", income_band_options, default=income_band_options)

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

    metrics = [
        ("Total Customers", f"{total_customers:,}", "#FDF2F8", "#DB2777"),
        ("Avg Total Spend", format_inr(avg_spend), "#ECFDF5", "#059669"),
        ("Avg Income", format_inr(avg_income), "#EFF6FF", "#2563EB"),
        ("Response Rate", f"{response_rate:.2f}%", "#FFFBEB", "#D97706"),
        ("Avg Web Visits", f"{avg_web_visits:.2f}", "#F5F3FF", "#7C3AED"),
        ("Avg Total Purchases", f"{avg_total_purchases:.2f}", "#FEF3C7", "#F59E0B"),
    ]

    cols = st.columns([1.4, 1.4, 1.4])
    for i, (label, value, bg, accent) in enumerate(metrics):
        col = cols[i % len(cols)]
        col.markdown(
            f"""
            <div class='metric-card' style='background: linear-gradient(135deg, {bg}, #ffffff); border-left: 5px solid {accent};'>
                <div class='metric-card-label'>{label}</div>
                <div class='metric-card-value'>{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def chart_segment_response(df: pd.DataFrame) -> None:
    segment_summary = (
        df.assign(
            Any_Campaign_Accepted=lambda x: x[
                ["AcceptedCmp1", "AcceptedCmp2", "AcceptedCmp3", "AcceptedCmp4", "AcceptedCmp5"]
            ].any(axis=1).astype(int)
        )
        .groupby("Primary_Segment", as_index=False)
        .agg(
            customer_count=("ID", "count"),
            AcceptedCmp1=("AcceptedCmp1", "mean"),
            AcceptedCmp2=("AcceptedCmp2", "mean"),
            AcceptedCmp3=("AcceptedCmp3", "mean"),
            AcceptedCmp4=("AcceptedCmp4", "mean"),
            AcceptedCmp5=("AcceptedCmp5", "mean"),
            Response=("Response", "mean"),
            Any_Campaign_Accepted=("Any_Campaign_Accepted", "mean"),
        )
    )
    for column in [*CAMPAIGN_COLUMNS.keys(), "Any_Campaign_Accepted"]:
        segment_summary[column] = segment_summary[column] * 100

    segment_summary = segment_summary[segment_summary["Primary_Segment"] != "Campaign Responder"]
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
    st.markdown(
        "This chart shows response rates for each campaign, broken down by customer segment. "
        "Each colored bar represents a different campaign, and the height shows how many customers in that segment responded."
    )
    st.markdown(
        "#### What the axes mean in plain terms\n"
        "- `x-axis` = customer segment (like High Income, Young Customer, etc.)\n"
        "- `y-axis` = percentage of customers in that segment who responded to each campaign\n"
        "- `response rate` = the share of customers in the segment who said yes to that campaign\n"
    )
    st.altair_chart(chart, use_container_width=True)
    display_columns = [
        "Primary_Segment",
        "customer_count",
        "AcceptedCmp1",
        "AcceptedCmp2",
        "AcceptedCmp3",
        "AcceptedCmp4",
        "AcceptedCmp5",
    ]
    table_data = segment_summary[segment_summary["Primary_Segment"] != "Campaign Responder"]
    st.dataframe(
        table_data[display_columns].rename(columns={col: label for col, label in CAMPAIGN_COLUMNS.items()}),
        use_container_width=True,
        hide_index=True,
    )
    st.markdown(
        "#### Interpretation\n"
        "The chart and table show campaign acceptance rates for each customer segment. "
        "Segments with taller bars and higher table values are more responsive to Campaign 1 through Campaign 5."
    )


def chart_product_spending(df: pd.DataFrame) -> None:
    st.subheader("Product Spending by Demographic")
    st.markdown(
        "Use the dropdown below to compare average spending across wines, fruits, meat, fish, sweets, and gold by customer group. "
        "This chart shows average spend per customer in each group, not the total spend of the entire group."
    )
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

    st.markdown("**Average product spend across selected groups**")
    st.dataframe(
        grouped.style.format({
            product: "Rs {:.2f}" for product in SPEND_COLUMNS.values()
        }),
        use_container_width=True,
        hide_index=True,
    )
    st.markdown(
        "#### What the axes mean in plain terms\n"
        "- `x-axis` = the selected demographic group (age band, income band, marital status, or country)\n"
        "- `y-axis` = average amount spent on each product category\n"
        "- `average spend` = how much customers in that group typically spend on each product"
    )
    st.markdown(
        "#### Summary\n"
        "This section compares spending patterns across product categories for the chosen demographic dimension. It reveals whether certain groups allocate more budget to wines, meat, sweets, or other categories. "
        "These insights can guide product-focused campaign personalization by age band, income band, marital status, or country."
    )


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
    st.markdown(
        "#### What the axes mean in plain terms\n"
        "- `x-axis` = customer segment (only showing high-value customers)\n"
        "- `y-axis` = average number of purchases made through each channel\n"
        "- `average purchases` = how many items customers in that segment typically buy through each channel"
    )
    st.markdown(
        "#### Summary\n"
        "This chart shows channel usage patterns for high-value customers, helping to identify whether web, store, catalog, or deals purchases are most important for this group. "
        "The supporting metrics confirm that high-value customers also spend more and visit the web frequently, making them strong candidates for personalized channel campaigns."
    )


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
    st.markdown(
        "#### Interpretation\n"
        "This table shows underserved segments that spend below the median, visit the website often, and do not respond to the final campaign. "
        "Because this view is filtered by `Response = 0`, the `response_rate_pct` column is zero for every row. "
        "These segments are useful for identifying customers who may respond to better-targeted re-engagement efforts."
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
    st.markdown(
        "#### What the columns mean in plain terms\n"
        "- `Age_Band` = age group of the customers (e.g., 30-39, 40-49)\n"
        "- `Income_Band` = income level group (e.g., Lower, Mid, Upper-Mid)\n"
        "- `Family_Composition` = family status (e.g., Single, Married with Kids)\n"
        "- `Country` = country of residence\n"
        "- `Education` = education level\n"
        "- `Marital_Status` = marital status\n"
        "- `customer_count` = number of customers in this profile group\n"
        "- `avg_total_spend` = average amount spent by customers in this group\n"
        "- `response_rate_pct` = percentage of customers in this group who responded positively\n"
        "- `avg_web_purchases` = average number of web purchases by customers in this group\n"
        "- `avg_store_purchases` = average number of store purchases by customers in this group\n"
        "- `avg_catalog_purchases` = average number of catalog purchases by customers in this group\n"
    )
    st.markdown(
        "#### Interpretation\n"
        "This table highlights the most promising customer profiles based on high response rates and spending. "
        "Profiles with higher response rates and average spends are ideal for targeting in future campaigns. "
        "These segments combine demographic details with engagement metrics to guide personalized marketing strategies."
    )
    st.markdown("#### Final Verdict on Most Eligible Ideal Targets")
    st.markdown("Based on the data analysis, the top ideal target segments (ranked by response rate and average spend) are:")
    top_segments = summary.head(5)
    for idx, row in top_segments.iterrows():
        st.markdown(f"- **{row['Age_Band']}, {row['Income_Band']}, {row['Country']}, {row['Marital_Status']}**: {row['customer_count']} customers, {row['response_rate_pct']:.1f}% response rate, avg spend Rs {row['avg_total_spend']:.2f}")


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
    st.markdown(
        "#### Interpretation\n"
        "These recommendations are derived from the filtered data and focus on actionable strategies for improving campaign performance. "
        "They prioritize segments with high response rates, spending potential, and engagement patterns to maximize ROI in future marketing efforts."
    )


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
        .metric-card {
            padding: 1.2rem 1rem;
            border-radius: 1rem;
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
            margin-bottom: 1rem;
            color: #111827;
            min-height: 110px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .metric-card-label {
            font-size: 0.95rem;
            font-weight: 600;
            margin-bottom: 0.6rem;
            opacity: 0.8;
        }
        .metric-card-value {
            font-size: 1.8rem;
            font-weight: 700;
            line-height: 1.1;
        }
        div[data-testid="stMetric"] {
            padding: 1rem;
            border-radius: 1rem;
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
            color: #111827;
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

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "Executive Summary & Campaign Stats",
            "Segment Response",
            "Product Spending",
            "Channel Usage",
            "Under-Served Segments",
            "Ideal Targets & Recommendations",
        ]
    )

    with tab1:
        metric_block(filtered)
        campaign_columns = list(CAMPAIGN_COLUMNS.keys())[:-1]
        campaign_labels = [CAMPAIGN_COLUMNS[column] for column in campaign_columns]
        overall_campaign = pd.DataFrame(
            {
                "Campaign": campaign_labels,
                "Acceptance Rate (%)": [(filtered[column].mean() * 100) for column in campaign_columns],
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
        st.subheader("Campaign Acceptance Rate")
        st.markdown(
            "This chart shows how many customers said yes to each campaign. "
            "The bottom line (x-axis) lists the five campaigns, and the vertical scale (y-axis) shows the percentage of customers who accepted each one. "
            "So if a bar reaches 10 on the y-axis, that means 10% of customers accepted that campaign."
        )
        st.markdown(
            "#### What the axes mean in plain terms\n"
            "- `x-axis` = campaign name (Campaign 1 through Campaign 5)\n"
            "- `y-axis` = percentage of customers who said yes to that campaign\n"
            "- `acceptance rate` = the share of customers who accepted that campaign"
        )
        st.altair_chart(chart, use_container_width=True)
        st.markdown(
            "#### Summary\n"
            "Campaign 1 and Campaign 3 have the highest acceptance rates in this dataset. "
            "This means more customers said yes to these two campaigns compared to the others."
        )

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
