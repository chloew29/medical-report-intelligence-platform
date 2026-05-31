import streamlit as st

st.set_page_config(
    page_title="Medical Report Intelligence Platform",
    layout="wide"
)

st.title("Medical Report Intelligence Platform")

st.markdown("""
An end-to-end healthcare data and AI platform for:

1. CMS hospital data ingestion
2. Healthcare KPI analytics
3. Clinical entity extraction
4. PubMed evidence retrieval
5. Clinical trial matching
6. Executive PDF reporting

This project uses public, deidentified, or synthetic data only.
""")

st.info("Day 1 setup complete. Next step: build the CMS data ingestion pipeline.")