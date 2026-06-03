import os
import sys

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.literature.pubmed_api import PubMedAPI

from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()

st.set_page_config(
    page_title="PubMed Evidence Assistant",
    page_icon="📚",
    layout="wide",
)

st.title("📚 PubMed Evidence Assistant")

st.markdown("""
This module searches PubMed biomedical literature and generates a source-grounded evidence summary
from retrieved article abstracts.

The goal is to demonstrate medical literature search, research synthesis, and safe LLM-based summarization.
""")

st.caption(
    "Data source: PubMed via NCBI E-utilities. This tool is for educational and portfolio purposes only and is not medical advice."
)


@st.cache_resource
def load_pubmed_client():
    return PubMedAPI()


@st.cache_resource
def load_llm():
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)


pubmed_client = load_pubmed_client()


# -----------------------------
# Search Input
# -----------------------------
st.subheader("Search Biomedical Literature")

example_queries = [
    "diabetes readmission risk",
    "depression digital health intervention",
    "asthma emergency department children",
    "heart failure hospital readmission",
    "breast cancer clinical trial eligibility",
]

col1, col2 = st.columns([3, 1])

with col1:
    query = st.text_input(
        "Enter a research topic, disease, intervention, or outcome:",
        value="diabetes readmission risk",
    )

with col2:
    max_results = st.number_input(
        "Max Articles",
        min_value=1,
        max_value=20,
        value=5,
        step=1,
    )

filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    start_year = st.number_input(
        "Start Year",
        min_value=1990,
        max_value=2026,
        value=2020,
        step=1,
    )

with filter_col2:
    end_year = st.number_input(
        "End Year",
        min_value=1990,
        max_value=2026,
        value=2026,
        step=1,
    )

with filter_col3:
    article_type = st.selectbox(
        "Article Type",
        options=[
            "Any Article Type",
            "Systematic Review",
            "Clinical Trial",
            "Review",
            "Meta-Analysis",
            "Randomized Controlled Trial",
        ],
        index=0,
    )

st.markdown("**Example searches:** " + ", ".join(example_queries))


# -----------------------------
# Search Button
# -----------------------------
if st.button("Search PubMed and Summarize", type="primary"):
    if not query.strip():
        st.warning("Please enter a research query.")
        st.stop()

    with st.spinner("Searching PubMed..."):
        try:
            articles = pubmed_client.search_pubmed(
                query=query,
                max_results=int(max_results),
                start_year=int(start_year),
                end_year=int(end_year),
                article_type=article_type,
            )
        except Exception as e:
            st.error(f"PubMed API error: {e}")
            st.stop()

    if not articles:
        st.info("No PubMed articles found for this search.")
        st.stop()

    st.success(f"Retrieved {len(articles)} PubMed articles.")

    # -----------------------------
    # Article Table
    # -----------------------------
    st.subheader("Retrieved Articles")

    article_rows = []
    for article in articles:
        article_rows.append(
            {
                "PMID": article["pmid"],
                "Title": article["title"],
                "Journal": article["journal"],
                "Year": article["year"],
                "Publication Type": ", ".join(article.get("publication_types", [])) or "Not listed",
                "URL": article["url"],
            }
        )

    df_articles = pd.DataFrame(article_rows)
    st.dataframe(df_articles, use_container_width=True)

    # -----------------------------
    # LLM Evidence Summary
    # -----------------------------
    st.subheader("AI Evidence Summary")

    context_blocks = []
    for i, article in enumerate(articles, start=1):
        context_blocks.append(
            f"""
Source {i}
PMID: {article['pmid']}
Title: {article['title']}
Journal: {article['journal']}
Year: {article['year']}
Abstract:
{article['abstract']}
"""
        )

    context_text = "\n\n".join(context_blocks)

    prompt_template = PromptTemplate(
        input_variables=["query", "context"],
        template="""
You are a careful biomedical evidence assistant.

Use ONLY the PubMed article information provided below.
Do not invent studies, statistics, clinical recommendations, or medical advice.
If the retrieved abstracts do not provide enough evidence, say that the evidence is limited.

User research query:
{query}

Retrieved PubMed evidence:
{context}

Write a concise evidence summary with:
1. Key findings
2. Common themes across studies
3. Limitations of the retrieved evidence
4. Practical relevance for healthcare data or healthtech work

Evidence Summary:
""",
    )

    try:
        llm = load_llm()
        final_prompt = prompt_template.format(query=query, context=context_text)
        ai_response = llm.invoke(final_prompt)

        st.info(ai_response.content)
        st.caption(
            "This summary is generated only from retrieved PubMed metadata and abstracts. "
            "It is not medical advice."
        )
    except Exception as e:
        st.warning(
            "PubMed search worked, but LLM summary failed. "
            "Check your GOOGLE_API_KEY in .env."
        )
        st.error(str(e))

    st.divider()

    # -----------------------------
    # Detailed Article Expanders
    # -----------------------------
    st.subheader("Detailed Article Evidence")

    for idx, article in enumerate(articles, start=1):
        with st.expander(f"Article #{idx}: {article['title']}"):
            st.markdown(f"**PMID:** {article['pmid']}")
            st.markdown(f"**Journal:** {article['journal']}")
            st.markdown(f"**Year:** {article['year']}")
            st.markdown(f"[Open on PubMed]({article['url']})")
            st.markdown("**Abstract:**")
            st.write(article["abstract"])

    # -----------------------------
    # Downloadable Report
    # -----------------------------
    report_lines = [
        "# PubMed Evidence Report",
        "",
        "## Research Query",
        query,
        "",
        "## Search Filters",
        f"- Start year: {start_year}",
        f"- End year: {end_year}",
        f"- Article type: {article_type}",
        "",
        f"## Number of Articles Retrieved",
        str(len(articles)),
        "",
        "## Retrieved Articles",
        "",
    ]

    for idx, article in enumerate(articles, start=1):
        report_lines.extend(
            [
                f"### Article {idx}: {article['title']}",
                f"- PMID: {article['pmid']}",
                f"- Journal: {article['journal']}",
                f"- Year: {article['year']}",
                f"- URL: {article['url']}",
                "",
                "Abstract:",
                article["abstract"],
                "",
            ]
        )

    report_lines.extend(
        [
            "## Disclaimer",
            "This report is for educational and portfolio purposes only. "
            "It is generated from retrieved PubMed abstracts and is not medical advice.",
        ]
    )

    report_text = "\n".join(report_lines)

    st.download_button(
        label="Download PubMed Evidence Report",
        data=report_text,
        file_name=f"pubmed_evidence_{query.replace(' ', '_')}.md",
        mime="text/markdown",
    )