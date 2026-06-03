import datetime
import streamlit as st


st.set_page_config(
    page_title="Executive Report Generator",
    page_icon="📄",
    layout="wide",
)

st.title("📄 Executive Report Generator")

st.markdown("""
This module creates an executive-ready healthcare AI report by combining insights from the platform's
analytics, clinical NLP, evidence search, clinical trial matching, and PubMed literature review modules.

The goal is to demonstrate end-to-end reporting automation for healthtech, healthcare analytics,
and AI product workflows.
""")

st.caption(
    "This report is for educational and portfolio purposes only. "
    "It does not provide medical advice, diagnosis, treatment, financial advice, or operational advice."
)

st.divider()


# -----------------------------
# Report Metadata
# -----------------------------
st.subheader("Report Metadata")

meta_col1, meta_col2, meta_col3 = st.columns(3)

with meta_col1:
    report_title = st.text_input(
        "Report Title",
        value="Medical Report Intelligence Platform Executive Summary",
    )

with meta_col2:
    organization_name = st.text_input(
        "Organization / Portfolio Name",
        value="HealthTech AI Portfolio Project",
    )

with meta_col3:
    report_date = st.date_input(
        "Report Date",
        value=datetime.date.today(),
    )


# -----------------------------
# Executive Summary
# -----------------------------
st.subheader("Executive Summary")

executive_summary = st.text_area(
    "Write a short executive overview:",
    height=140,
    value=(
        "This report summarizes outputs from an end-to-end healthcare data and AI platform. "
        "The platform combines hospital KPI analytics, clinical entity extraction, semantic evidence retrieval, "
        "clinical trial matching, and PubMed literature synthesis to support healthtech reporting workflows."
    ),
)


# -----------------------------
# Hospital KPI Findings
# -----------------------------
st.subheader("1. Hospital KPI Dashboard Findings")

kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

with kpi_col1:
    selected_state = st.text_input("Selected State", value="CA")

with kpi_col2:
    total_hospitals = st.number_input(
        "Hospitals Analyzed",
        min_value=0,
        value=378,
        step=1,
    )

with kpi_col3:
    avg_rating = st.text_input(
        "Average Overall Rating",
        value="3.10",
    )

hospital_kpi_summary = st.text_area(
    "Hospital KPI Interpretation",
    height=120,
    value=(
        "The hospital KPI dashboard provides a structured view of hospital distribution, quality ratings, "
        "and readmission-related operational impact. The dashboard can support benchmarking, quality monitoring, "
        "and initial operational planning."
    ),
)


# -----------------------------
# Clinical NLP Findings
# -----------------------------
st.subheader("2. Clinical NLP Findings")

clinical_entities = st.text_area(
    "Extracted Clinical Entities",
    height=120,
    value=(
        "- Diseases / Disorders: diabetes, hypertension, pneumonia\n"
        "- Signs / Symptoms: chest pain, shortness of breath, fever\n"
        "- Medications: metformin, amoxicillin\n"
        "- Procedures: ECG, stress test"
    ),
)

clinical_nlp_summary = st.text_area(
    "Clinical NLP Interpretation",
    height=120,
    value=(
        "The clinical note analyzer extracts structured medical entities from unstructured clinical text. "
        "This demonstrates how biomedical NLP can transform free-text notes into structured information for "
        "search, reporting, and downstream analytics."
    ),
)


# -----------------------------
# Clinical Evidence Search Findings
# -----------------------------
st.subheader("3. Clinical Evidence Search Findings")

clinical_search_query = st.text_input(
    "Clinical Evidence Search Query",
    value="chest pain",
)

clinical_evidence_summary = st.text_area(
    "Clinical Evidence Summary",
    height=140,
    value=(
        "The clinical evidence search module retrieved relevant medical record chunks and generated a summary "
        "grounded only in retrieved evidence. Retrieved evidence included chest wall tenderness, stress-related symptoms, "
        "and cardiac testing results."
    ),
)


# -----------------------------
# Clinical Trial Matcher Findings
# -----------------------------
st.subheader("4. Clinical Trial Matcher Findings")

trial_condition = st.text_input(
    "Clinical Trial Search Condition",
    value="diabetes",
)

trial_summary = st.text_area(
    "Clinical Trial Matching Summary",
    height=140,
    value=(
        "The clinical trial matcher searched ClinicalTrials.gov and returned relevant studies based on the selected condition. "
        "The module demonstrates API integration, public clinical trial search, and explainable matching."
    ),
)


# -----------------------------
# PubMed Evidence Findings
# -----------------------------
st.subheader("5. PubMed Evidence Findings")

pubmed_query = st.text_input(
    "PubMed Search Query",
    value="diabetes readmission risk",
)

pubmed_summary = st.text_area(
    "PubMed Evidence Summary",
    height=160,
    value=(
        "The PubMed evidence assistant retrieved biomedical articles and generated a source-grounded summary. "
        "The evidence suggested that diabetes is associated with higher readmission risk and that risk prediction, "
        "post-discharge follow-up, medication reconciliation, and interdisciplinary care may be relevant themes."
    ),
)


# -----------------------------
# Risk, Governance, and Limitations
# -----------------------------
st.subheader("6. AI Safety, Governance, and Limitations")

governance_summary = st.text_area(
    "Governance and Limitations",
    height=160,
    value=(
        "- The platform uses public, deidentified, or synthetic data only.\n"
        "- LLM summaries are generated from retrieved evidence and should not be treated as medical advice.\n"
        "- Clinical outputs require human review before real-world use.\n"
        "- Public datasets may be incomplete, biased, outdated, or missing operational context.\n"
        "- The platform is designed for educational and portfolio demonstration purposes."
    ),
)


# -----------------------------
# Generate Report
# -----------------------------
st.divider()
st.subheader("Generated Executive Report")

report_text = f"""# {report_title}

## Report Metadata
- Organization / Project: {organization_name}
- Report Date: {report_date}
- Report Type: Healthcare AI Executive Summary

## Executive Summary
{executive_summary}

## 1. Hospital KPI Dashboard Findings
- Selected state: {selected_state}
- Hospitals analyzed: {total_hospitals:,}
- Average overall rating: {avg_rating}

{hospital_kpi_summary}

## 2. Clinical NLP Findings
### Extracted Clinical Entities
{clinical_entities}

### Interpretation
{clinical_nlp_summary}

## 3. Clinical Evidence Search Findings
- Search query: {clinical_search_query}

{clinical_evidence_summary}

## 4. Clinical Trial Matcher Findings
- Trial search condition: {trial_condition}

{trial_summary}

## 5. PubMed Evidence Findings
- PubMed search query: {pubmed_query}

{pubmed_summary}

## 6. AI Safety, Governance, and Limitations
{governance_summary}

## Final Portfolio Interpretation
This platform demonstrates an end-to-end healthtech AI workflow that combines data engineering,
healthcare analytics, biomedical NLP, semantic retrieval, LLM summarization, public API integration,
and automated reporting.

The project is designed to show practical readiness for data analyst, data engineer, ML engineer,
healthcare analytics, and healthtech AI roles.

## Disclaimer
This report is for educational and portfolio purposes only. It does not provide medical advice,
diagnosis, treatment recommendations, financial advice, or operational advice.
"""

st.markdown(report_text)

st.download_button(
    label="Download Executive Report",
    data=report_text,
    file_name="medical_report_intelligence_executive_report.md",
    mime="text/markdown",
)