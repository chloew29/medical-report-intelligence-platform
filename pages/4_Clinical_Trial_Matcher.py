import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.trials.clinical_trials_api import ClinicalTrialsAPI


st.set_page_config(
    page_title="Clinical Trial Matcher",
    page_icon="🧬",
    layout="wide",
)

st.title("🧬 Clinical Trial Matcher")

st.markdown("""
This module searches public ClinicalTrials.gov records and returns clinical trials
that may be relevant to a medical condition or patient profile.

The goal is to demonstrate healthtech product thinking, API integration,
clinical search, and explainable matching.
""")

st.caption(
    "Data source: ClinicalTrials.gov public API. "
    "This tool is for educational and portfolio purposes only and does not provide medical advice."
)


@st.cache_resource
def load_api_client():
    return ClinicalTrialsAPI()


api_client = load_api_client()


# -----------------------------
# Search Input
# -----------------------------
st.subheader("Search for Clinical Trials")

example_conditions = [
    "diabetes",
    "breast cancer",
    "depression",
    "asthma",
    "hypertension",
    "pneumonia",
]

col1, col2 = st.columns([3, 1])

with col1:
    condition = st.text_input(
        "Enter a condition, disease, or clinical term:",
        value="diabetes",
    )

with col2:
    max_results = st.number_input(
        "Max Results",
        min_value=1,
        max_value=25,
        value=10,
        step=1,
    )

st.markdown("**Example searches:** " + ", ".join(example_conditions))


# -----------------------------
# Search Button
# -----------------------------
if st.button("Search Clinical Trials", type="primary"):
    if not condition.strip():
        st.warning("Please enter a condition or disease.")
        st.stop()

    with st.spinner("Searching ClinicalTrials.gov..."):
        try:
            trials = api_client.search_trials(
                condition=condition,
                max_results=int(max_results),
            )
        except Exception as e:
            st.error(f"ClinicalTrials.gov API error: {e}")
            st.stop()

    if not trials:
        st.info("No clinical trials found for this search.")
        st.stop()

    st.success(f"Found {len(trials)} clinical trial records.")

    # -----------------------------
    # Summary Table
    # -----------------------------
    st.subheader("Trial Match Overview")

    table_rows = []
    for trial in trials:
        table_rows.append(
            {
                "NCT ID": trial["nct_id"],
                "Title": trial["title"],
                "Status": trial["status"],
                "Phase": trial["phase"],
                "Location": trial["location"],
            }
        )

    df_trials = pd.DataFrame(table_rows)
    st.dataframe(df_trials, use_container_width=True)

    # -----------------------------
    # Detailed Trial Cards
    # -----------------------------
    st.subheader("Detailed Trial Results")

    for idx, trial in enumerate(trials, start=1):
        with st.expander(f"Trial #{idx}: {trial['title']}"):
            st.markdown(f"**NCT ID:** {trial['nct_id']}")
            st.markdown(f"**Status:** {trial['status']}")
            st.markdown(f"**Phase:** {trial['phase']}")
            st.markdown(f"**Location:** {trial['location']}")

            if trial["conditions"]:
                st.markdown("**Listed Conditions:**")
                st.write(", ".join(trial["conditions"]))

            if trial["interventions"]:
                st.markdown("**Interventions:**")
                st.write(", ".join(trial["interventions"]))
            else:
                st.markdown("**Interventions:** Not listed")

            st.markdown("**Match Explanation:**")
            st.info(trial["match_reason"])

            st.markdown(f"[Open Trial on ClinicalTrials.gov]({trial['url']})")

    # -----------------------------
    # Downloadable Report
    # -----------------------------
    report_lines = [
        "# Clinical Trial Matching Report",
        "",
        f"## Search Condition",
        condition,
        "",
        f"## Number of Trials Returned",
        str(len(trials)),
        "",
        "## Trial Results",
        "",
    ]

    for idx, trial in enumerate(trials, start=1):
        report_lines.extend(
            [
                f"### Trial {idx}: {trial['title']}",
                f"- NCT ID: {trial['nct_id']}",
                f"- Status: {trial['status']}",
                f"- Phase: {trial['phase']}",
                f"- Location: {trial['location']}",
                f"- Conditions: {', '.join(trial['conditions']) if trial['conditions'] else 'Not listed'}",
                f"- Interventions: {', '.join(trial['interventions']) if trial['interventions'] else 'Not listed'}",
                f"- URL: {trial['url']}",
                f"- Match explanation: {trial['match_reason']}",
                "",
            ]
        )

    report_lines.extend(
        [
            "## Disclaimer",
            "This report is for educational and portfolio purposes only. "
            "It does not determine patient eligibility and is not medical advice.",
        ]
    )

    report_text = "\n".join(report_lines)

    st.download_button(
        label="Download Trial Matching Report",
        data=report_text,
        file_name=f"clinical_trial_matches_{condition.replace(' ', '_')}.md",
        mime="text/markdown",
    )


st.divider()

st.subheader("How This Module Fits the Platform")

st.markdown("""
This module can later connect with the Clinical Note Analyzer:

```text
Clinical note
    ↓
Extract disease or condition
    ↓
Search ClinicalTrials.gov
    ↓
Rank relevant trials
    ↓
Generate an explainable matching report
            """)