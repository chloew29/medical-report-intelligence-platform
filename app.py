
import streamlit as st

st.set_page_config(
    page_title="Medical Report Intelligence Platform",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Medical Report Intelligence Platform")

st.markdown("""
An end-to-end healthcare data and AI platform that combines structured hospital analytics,
clinical NLP, semantic evidence retrieval, clinical trial matching, PubMed literature synthesis,
and automated executive reporting.

This platform demonstrates practical healthtech data and ML skills across the full data lifecycle:
**data ingestion → analytics → clinical NLP → semantic retrieval → LLM summarization → public API integration → executive reporting.**
""")

st.caption(
    "Data policy: This project uses public, deidentified, or synthetic data only. "
    "It is for educational and research purposes and does not provide medical advice, diagnosis, or treatment recommendations."
)

st.divider()

st.subheader("Platform Modules")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 1. Clinical Note Analyzer
    Extracts diseases, symptoms, medications, and procedures from clinical notes using biomedical NLP.

    **Role focus:** ML / Clinical NLP

    ### 2. Clinical Evidence Search
    Retrieves relevant medical evidence chunks and generates source-grounded LLM summaries.

    **Role focus:** RAG / LLM / Health AI
    """)

with col2:
    st.markdown("""
    ### 3. Hospital KPI Dashboard
    Analyzes public CMS hospital quality data and estimates operational impact from readmission reduction.

    **Role focus:** Data Analyst / Healthcare Analytics

    ### 4. Clinical Trial Matcher
    Searches ClinicalTrials.gov and returns relevant trials for a selected medical condition.

    **Role focus:** API Integration / Healthtech Product
    """)

with col3:
    st.markdown("""
    ### 5. PubMed Evidence Assistant
    Searches PubMed articles and generates source-grounded biomedical evidence summaries.

    **Role focus:** Medical Literature Search / Research Synthesis

    ### 6. Executive Report Generator
    Combines outputs from all modules into an executive-ready healthcare AI report.

    **Role focus:** Reporting Automation / Product Delivery
    """)

st.divider()

st.subheader("Current Build Status")

status_col1, status_col2, status_col3 = st.columns(3)

with status_col1:
    st.success("✅ Clinical NLP")
    st.write("Clinical note entity extraction is working.")

with status_col2:
    st.success("✅ Evidence + Literature Search")
    st.write("Clinical evidence search and PubMed evidence assistant are working.")

with status_col3:
    st.success("✅ Reporting")
    st.write("Hospital KPI dashboard, trial matcher, and executive report generator are working.")

st.info(
    "MVP complete: the platform now includes six working modules covering healthcare analytics, NLP, RAG, API integration, literature evidence, and executive reporting."
)

st.divider()

st.subheader("System Architecture")

st.markdown("""
```text
Public / Synthetic Healthcare Data
        ↓
Data Cleaning + Local Storage
        ↓
Clinical NLP + Semantic Retrieval
        ↓
LLM Evidence-Grounded Summarization
        ↓
Clinical Trial + PubMed API Search
        ↓
Dashboard + Executive Reporting
````

""")

st.subheader("Healthcare AI Safety Design")

st.markdown("""

* Uses public, deidentified, or synthetic data only.
* Displays retrieved evidence alongside AI-generated summaries.
* Uses evidence-grounded prompts to reduce hallucination risk.
* Includes warnings and disclaimers for medical AI outputs.
* Does not provide diagnosis, treatment, financial, or operational advice.
* Requires human review before any real-world healthcare use.
  """)

st.divider()

st.caption(
"Built as a healthtech portfolio project focused on healthcare analytics, clinical NLP, LLM applications, public API integration, and automated reporting."
)


