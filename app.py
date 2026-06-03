
import streamlit as st

st.set_page_config(
    page_title="Medical Report Intelligence Platform",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Medical Report Intelligence Platform")

st.markdown("""
An end-to-end healthcare data and AI platform that combines structured hospital analytics,
clinical NLP, semantic evidence retrieval, clinical trial matching, and automated executive reporting.

This platform is designed to demonstrate practical healthtech data and ML skills across the full data lifecycle:
data ingestion, analytics, retrieval, NLP, LLM summarization, and report generation.
""")

st.divider()

st.subheader("Platform Modules")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 1. CMS Data Pipeline
    Ingests and cleans public CMS hospital quality data for downstream analytics.
    
    ### 2. Hospital KPI Dashboard
    Tracks healthcare quality metrics such as readmission, mortality, and hospital performance.
    """)

with col2:
    st.markdown("""
    ### 3. Clinical Note Analyzer
    Extracts medical entities such as diseases, symptoms, medications, and procedures from clinical text.
    
    ### 4. Clinical Evidence Search
    Retrieves relevant medical evidence chunks and generates source-grounded LLM summaries.
    """)

with col3:
    st.markdown("""
    ### 5. Clinical Trial Matcher
    Matches patient profiles or extracted clinical entities with relevant clinical trials.
    
    ### 6. Executive PDF Reports
    Converts analytics, evidence, and model outputs into administrator-ready reports.
    """)

st.divider()

st.subheader("Current Build Status")

st.success("Environment setup, GitHub connection, Streamlit app, and clinical evidence search backend are working.")

st.info(
    "Next step: continue improving the Clinical Evidence Search module, then build the CMS hospital KPI dashboard."
)

st.caption(
    "Data policy: This project uses public, deidentified, or synthetic data only. "
    "It is for educational and research purposes and does not provide medical advice, diagnosis, or treatment recommendations."
)

