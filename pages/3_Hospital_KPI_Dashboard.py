
import os

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Hospital KPI Dashboard",
    page_icon="📊",
    layout="wide",
)

# -----------------------------
# Page Header
# -----------------------------
st.title("📊 Hospital KPI Dashboard")

st.markdown("""
This dashboard analyzes public CMS hospital quality data to demonstrate healthcare analytics,
KPI monitoring, operational reporting, and business impact analysis.

The goal is to show how hospital data can be transformed into clear insights for administrators,
analysts, and healthtech teams.
""")

st.caption(
    "Data source: public CMS hospital data. This dashboard is for educational and portfolio purposes only."
)


# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_hospital_data():
    cleaned_path = "data/processed/cms_hospital_data_cleaned.csv"
    raw_path = "data/raw/cms_hospital_data_raw.csv"

    if os.path.exists(cleaned_path):
        return pd.read_csv(cleaned_path)

    if os.path.exists(raw_path):
        return pd.read_csv(raw_path)

    return None


df = load_hospital_data()

if df is None:
    st.error(
        "Hospital data file not found. Please place your CMS hospital data in "
        "`data/raw/cms_hospital_data_raw.csv` or "
        "`data/processed/cms_hospital_data_cleaned.csv`."
    )
    st.stop()


# -----------------------------
# Basic Cleaning / Column Handling
# -----------------------------
df.columns = [col.strip() for col in df.columns]

possible_state_cols = ["State", "state"]
possible_rating_cols = [
    "Hospital overall rating",
    "hospital_overall_rating",
    "overall_rating",
    "Rating",
]
possible_name_cols = [
    "Hospital Name",
    "hospital_name",
    "Facility Name",
    "facility_name",
]
possible_type_cols = [
    "Hospital Type",
    "hospital_type",
    "Facility Type",
    "facility_type",
]
possible_ownership_cols = [
    "Hospital Ownership",
    "hospital_ownership",
    "Ownership",
]


def find_col(possible_cols):
    for col in possible_cols:
        if col in df.columns:
            return col
    return None


state_col = find_col(possible_state_cols)
rating_col = find_col(possible_rating_cols)
name_col = find_col(possible_name_cols)
type_col = find_col(possible_type_cols)
ownership_col = find_col(possible_ownership_cols)

if state_col is None:
    st.error("Could not find a State column in your dataset.")
    st.write("Available columns:", df.columns.tolist())
    st.stop()

if name_col is None:
    st.warning("Could not find a hospital name column. The table will still work.")

if rating_col is not None:
    df[rating_col] = pd.to_numeric(df[rating_col], errors="coerce")


# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Dashboard Filters")

states = sorted(df[state_col].dropna().unique().tolist())

if not states:
    st.error("No valid states found in the dataset.")
    st.stop()

default_state_index = states.index("CA") if "CA" in states else 0

selected_state = st.sidebar.selectbox(
    "Select State",
    options=states,
    index=default_state_index,
)

filtered_df = df[df[state_col] == selected_state].copy()

selected_type = "All Types"
if type_col is not None:
    hospital_types = sorted(filtered_df[type_col].dropna().unique().tolist())

    if hospital_types:
        selected_type = st.sidebar.selectbox(
            "Select Hospital Type",
            options=["All Types"] + hospital_types,
            index=0,
        )

        if selected_type != "All Types":
            filtered_df = filtered_df[filtered_df[type_col] == selected_type]

selected_ownership = "All Ownership Types"
if ownership_col is not None:
    ownership_types = sorted(filtered_df[ownership_col].dropna().unique().tolist())

    if ownership_types:
        selected_ownership = st.sidebar.selectbox(
            "Select Ownership Type",
            options=["All Ownership Types"] + ownership_types,
            index=0,
        )

        if selected_ownership != "All Ownership Types":
            filtered_df = filtered_df[filtered_df[ownership_col] == selected_ownership]

if filtered_df.empty:
    st.warning("No hospitals match the selected filters. Please choose a different filter.")
    st.stop()


# -----------------------------
# KPI Calculations
# -----------------------------
total_hospitals = len(filtered_df)
total_states = filtered_df[state_col].nunique()

if rating_col is not None:
    avg_rating = filtered_df[rating_col].mean()
    rated_hospitals = filtered_df[rating_col].notna().sum()
else:
    avg_rating = None
    rated_hospitals = 0

avg_rating_text = (
    f"{avg_rating:.2f}"
    if avg_rating is not None and not pd.isna(avg_rating)
    else "N/A"
)


# -----------------------------
# KPI Cards
# -----------------------------
st.subheader("Key Hospital Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Hospitals", f"{total_hospitals:,}")

with col2:
    st.metric("Selected State", selected_state)

with col3:
    st.metric("Average Overall Rating", avg_rating_text)

with col4:
    st.metric("Hospitals With Rating", f"{rated_hospitals:,}")


# -----------------------------
# Executive Summary
# -----------------------------
st.subheader("Executive Summary")

if avg_rating_text != "N/A":
    executive_summary = (
        f"The filtered dataset contains {total_hospitals:,} hospitals in {selected_state}. "
        f"The average overall hospital rating is {avg_rating_text}, based on "
        f"{rated_hospitals:,} hospitals with available ratings. "
        "This dashboard supports hospital benchmarking, quality monitoring, and operational planning."
    )
else:
    executive_summary = (
        f"The filtered dataset contains {total_hospitals:,} hospitals in {selected_state}. "
        "Hospital rating data is not available for the current filter. "
        "This dashboard still supports hospital distribution and operational analysis."
    )

st.info(executive_summary)

st.divider()


# -----------------------------
# Charts
# -----------------------------
st.subheader("Hospital Distribution and Quality Overview")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    if type_col is not None:
        type_counts = (
            filtered_df.groupby(type_col)
            .size()
            .reset_index(name="Hospital Count")
            .sort_values("Hospital Count", ascending=True)
        )

        if not type_counts.empty:
            fig_type = px.bar(
                type_counts,
                x="Hospital Count",
                y=type_col,
                orientation="h",
                title=f"Hospital Count by Type in {selected_state}",
            )
            fig_type.update_layout(
                yaxis_title="",
                xaxis_title="Hospital Count",
                height=420,
            )
            st.plotly_chart(fig_type, use_container_width=True)
        else:
            st.info("No hospital type data available for the selected filters.")
    else:
        st.info("No hospital type column found.")

with chart_col2:
    if rating_col is not None:
        rating_counts = (
            filtered_df.dropna(subset=[rating_col])
            .groupby(rating_col)
            .size()
            .reset_index(name="Hospital Count")
            .sort_values(rating_col)
        )

        if not rating_counts.empty:
            fig_rating = px.bar(
                rating_counts,
                x=rating_col,
                y="Hospital Count",
                title=f"Hospital Overall Rating Distribution in {selected_state}",
            )
            fig_rating.update_layout(
                xaxis_title="Overall Rating",
                yaxis_title="Hospital Count",
                height=420,
            )
            st.plotly_chart(fig_rating, use_container_width=True)
        else:
            st.info("No rating data available for the selected filters.")
    else:
        st.info("No hospital rating column found.")


# -----------------------------
# Ownership Analysis
# -----------------------------
if ownership_col is not None:
    st.subheader("Hospital Ownership Overview")

    ownership_counts = (
        filtered_df.groupby(ownership_col)
        .size()
        .reset_index(name="Hospital Count")
        .sort_values("Hospital Count", ascending=True)
    )

    if not ownership_counts.empty:
        fig_ownership = px.bar(
            ownership_counts,
            x="Hospital Count",
            y=ownership_col,
            orientation="h",
            title=f"Hospital Count by Ownership in {selected_state}",
        )
        fig_ownership.update_layout(
            yaxis_title="",
            xaxis_title="Hospital Count",
            height=420,
        )
        st.plotly_chart(fig_ownership, use_container_width=True)

st.divider()


# -----------------------------
# Financial Impact Calculator
# -----------------------------
st.subheader("Readmission Reduction Impact Calculator")

st.markdown("""
This calculator estimates potential savings from reducing avoidable readmissions.
It is not a formal financial model. It demonstrates how healthcare analytics can connect
quality improvement to operational cost impact.
""")

calc_col1, calc_col2, calc_col3 = st.columns(3)

with calc_col1:
    annual_admissions = st.number_input(
        "Estimated Annual Admissions",
        min_value=0,
        value=10000,
        step=500,
    )

with calc_col2:
    current_readmission_rate = st.number_input(
        "Current Readmission Rate (%)",
        min_value=0.0,
        max_value=100.0,
        value=14.0,
        step=0.5,
    )

with calc_col3:
    target_reduction = st.number_input(
        "Readmission Reduction Goal (%)",
        min_value=0.0,
        max_value=100.0,
        value=2.0,
        step=0.5,
    )

avg_cost_per_readmission = st.number_input(
    "Estimated Cost per Readmission ($)",
    min_value=0,
    value=15000,
    step=1000,
)

current_readmissions = annual_admissions * (current_readmission_rate / 100)
avoided_readmissions = annual_admissions * (target_reduction / 100)
estimated_savings = avoided_readmissions * avg_cost_per_readmission

impact_col1, impact_col2, impact_col3 = st.columns(3)

with impact_col1:
    st.metric("Estimated Current Readmissions", f"{current_readmissions:,.0f}")

with impact_col2:
    st.metric("Avoided Readmissions", f"{avoided_readmissions:,.0f}")

with impact_col3:
    st.metric("Estimated Savings", f"${estimated_savings:,.0f}")

st.caption(
    "Assumption: savings are estimated as avoided readmissions multiplied by an assumed average cost per readmission."
)


# -----------------------------
# Downloadable Executive Report
# -----------------------------
st.subheader("Download Executive Report")

report_text = f"""# Hospital KPI Executive Summary

## Dashboard Filters
- Selected state: {selected_state}
- Selected hospital type: {selected_type}
- Selected ownership type: {selected_ownership}

## Key Metrics
- Total hospitals analyzed: {total_hospitals:,}
- Hospitals with ratings: {rated_hospitals:,}
- Average overall rating: {avg_rating_text}

## Executive Interpretation
{executive_summary}

## Readmission Impact Model
- Estimated annual admissions: {annual_admissions:,}
- Current readmission rate: {current_readmission_rate:.1f}%
- Readmission reduction goal: {target_reduction:.1f}%
- Estimated current readmissions: {current_readmissions:,.0f}
- Estimated avoided readmissions: {avoided_readmissions:,.0f}
- Estimated savings: ${estimated_savings:,.0f}

## Assumptions and Limitations
- This is a simplified operational estimate.
- Savings are estimated as avoided readmissions multiplied by an assumed average cost per readmission.
- CMS hospital quality data may be incomplete or may not include all operational variables.
- This report is for educational and portfolio purposes only.
- This report is not medical, financial, or operational advice.
"""

st.download_button(
    label="Download Executive Summary Report",
    data=report_text,
    file_name=f"hospital_kpi_summary_{selected_state}.md",
    mime="text/markdown",
)

st.divider()


# -----------------------------
# Data Table
# -----------------------------
st.subheader("Filtered Hospital Data")

if name_col is not None:
    display_cols = [name_col, state_col]
else:
    display_cols = [state_col]

for optional_col in [type_col, ownership_col, rating_col]:
    if optional_col is not None and optional_col not in display_cols:
        display_cols.append(optional_col)

st.dataframe(
    filtered_df[display_cols].head(500),
    use_container_width=True,
)

st.caption("Showing up to 500 rows from the filtered dataset.")
