````md
# Medical Report Intelligence Platform

An end-to-end healthcare data and AI platform that combines structured hospital analytics, clinical NLP, semantic evidence retrieval, clinical trial matching, PubMed literature synthesis, and automated executive reporting.

This project was built as a healthtech portfolio project to demonstrate practical skills for data analyst, data engineer, ML engineer, healthcare analytics, and AI product roles.

---

## Project Overview

Healthcare data is often fragmented across structured datasets, free-text clinical notes, public research databases, and operational reporting systems. This platform demonstrates how different healthcare data sources can be connected into one workflow:

```text
Public / Synthetic Healthcare Data
        ↓
Data Cleaning + Local Storage
        ↓
Clinical NLP + Semantic Retrieval
        ↓
LLM Evidence-Grounded Summarization
        ↓
Clinical Trial / PubMed Search
        ↓
Dashboard + Executive Reporting
````

The platform uses public, deidentified, or synthetic data only. It is for educational and research purposes and does not provide medical advice, diagnosis, or treatment recommendations.

---

## Working Modules

### 1. Clinical Note Analyzer

Extracts structured medical entities from clinical notes using biomedical named entity recognition.

**Features**

* Loads sample notes from the MTSamples dataset
* Allows users to select notes by medical specialty
* Extracts diseases, symptoms, medications, and procedures
* Uses a Hugging Face biomedical NER model

**Skills demonstrated**

* Clinical NLP
* Biomedical entity extraction
* Hugging Face Transformers
* Streamlit UI development

---

### 2. Clinical Evidence Search

Retrieves relevant clinical text chunks from a local semantic search database and generates evidence-grounded LLM summaries.

**Features**

* Builds a local vector search backend from medical text chunks
* Uses sentence embeddings and cosine similarity for semantic retrieval
* Displays retrieved evidence with similarity scores
* Generates LLM summaries only from retrieved context
* Includes safety warnings and not-medical-advice disclaimers

**Skills demonstrated**

* Semantic search
* RAG-style retrieval
* LLM grounding
* Evidence traceability
* Healthcare AI safety design

---

### 3. Hospital KPI Dashboard

Analyzes public CMS hospital quality data and presents healthcare KPI insights.

**Features**

* Loads cleaned CMS hospital data
* Filters by state, hospital type, and ownership type
* Shows KPI cards for hospital count, rating coverage, and average rating
* Visualizes hospital type distribution and rating distribution
* Includes a readmission reduction savings calculator
* Generates a downloadable executive summary report

**Skills demonstrated**

* Healthcare analytics
* KPI reporting
* Data visualization
* Operational impact analysis
* Streamlit dashboard development

---

### 4. Clinical Trial Matcher

Searches ClinicalTrials.gov and returns clinical trials relevant to a medical condition.

**Features**

* Searches public ClinicalTrials.gov API records
* Returns NCT ID, trial title, status, phase, location, and trial link
* Provides explainable match summaries
* Generates a downloadable trial matching report

**Skills demonstrated**

* Public API integration
* Clinical trial data retrieval
* Healthtech product thinking
* Explainable matching workflow

---

### 5. PubMed Evidence Assistant

Searches PubMed biomedical literature and generates a source-grounded evidence summary from retrieved abstracts.

**Features**

* Uses NCBI PubMed E-utilities
* Retrieves PMID, title, journal, year, abstract, and URL
* Supports literature evidence summarization
* Generates AI summaries from retrieved PubMed evidence
* Exports a downloadable PubMed evidence report

**Skills demonstrated**

* Biomedical literature search
* Research synthesis
* LLM summarization
* Evidence-based reporting

---

### 6. Executive Report Generator

Combines insights from all platform modules into one executive-ready healthcare AI report.

**Features**

* Summarizes hospital KPI findings
* Summarizes clinical NLP outputs
* Summarizes clinical evidence search results
* Summarizes clinical trial matching findings
* Summarizes PubMed evidence findings
* Includes AI governance, safety, and limitations
* Generates a downloadable executive report

**Skills demonstrated**

* Reporting automation
* Healthcare communication
* Executive summary writing
* End-to-end product workflow

---

## Tech Stack

**Languages and Libraries**

* Python
* Pandas
* NumPy
* scikit-learn
* Plotly
* Streamlit

**Machine Learning / NLP**

* Hugging Face Transformers
* Biomedical NER
* Sentence Transformers
* Semantic similarity search

**LLM / RAG**

* Gemini API
* LangChain prompt templates
* Evidence-grounded summarization

**Healthcare Data Sources**

* CMS hospital quality data
* MTSamples clinical text dataset
* ClinicalTrials.gov API
* PubMed / NCBI E-utilities

**Reporting**

* Markdown report generation
* Downloadable executive summaries
* Dashboard-based analytics reports

---

## Repository Structure

```text
medical-report-intelligence-platform/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── pages/
│   ├── 1_Clinical_Note_Analyzer.py
│   ├── 2_Clinical_Search.py
│   ├── 3_Hospital_KPI_Dashboard.py
│   ├── 4_Clinical_Trial_Matcher.py
│   ├── 5_PubMed_Evidence_Assistant.py
│   └── 6_Executive_Report_Generator.py
│
├── src/
│   ├── ml/
│   │   ├── extractor.py
│   │   └── build_vector_db.py
│   │
│   ├── search/
│   │   └── retriever.py
│   │
│   ├── trials/
│   │   └── clinical_trials_api.py
│   │
│   └── literature/
│       └── pubmed_api.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── synthetic/
│
├── docs/
├── pipelines/
├── reports/
└── sql/
```

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/chloew29/medical-report-intelligence-platform.git
cd medical-report-intelligence-platform
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

On Mac/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create environment file

Create a `.env` file:

```txt
GOOGLE_API_KEY=your_google_api_key_here
```

Do not commit your `.env` file.

### 5. Run the app

```bash
streamlit run app.py
```

---

## Data Policy

This project uses public, deidentified, or synthetic data only.

The project does not use real patient-identifiable information. Any clinical text used in the demo should come from public sample datasets, synthetic examples, or deidentified sources.

---

## AI Safety and Governance

This platform includes basic healthcare AI safety design:

* LLM summaries are grounded in retrieved evidence.
* Retrieved source text is displayed alongside generated summaries.
* The app includes disclaimers that outputs are not medical advice.
* Public datasets may be incomplete, biased, outdated, or missing clinical context.
* Human review is required before any real-world healthcare use.

---

## Portfolio Value

This project demonstrates readiness for roles such as:

* Healthcare Data Analyst
* Health Informatics Analyst
* Data Analyst
* Data Engineer
* ML Engineer
* Clinical NLP Engineer
* LLM Application Engineer
* Healthtech AI Analyst

It shows the full workflow from data ingestion and analytics to NLP, semantic retrieval, public API integration, LLM summarization, and executive reporting.

---

## Disclaimer

This project is for educational and portfolio purposes only. It does not provide medical advice, diagnosis, treatment recommendations, financial advice, or operational advice.

```
```
