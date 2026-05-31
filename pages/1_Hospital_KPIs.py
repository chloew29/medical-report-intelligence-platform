import streamlit as st
import pandas as pd
import os
from src.ml.extractor import ClinicalEntityExtractor

st.set_page_config(page_title="Note Analyzer", layout="wide")
st.title("🏥 Clinical Note Entity Extractor")
st.markdown("Powered by Hugging Face `BioMedical-NER` and the MTSamples Dataset.")

# --- 1. CACHE THE HEAVY ASSETS ---
@st.cache_resource
def load_model():
    # This prevents the 1GB model from reloading every time you click a button
    return ClinicalEntityExtractor()

@st.cache_data
def load_data():
    file_path = "data/raw/mtsamples.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        # Clean out any empty notes
        df = df.dropna(subset=['transcription']) 
        return df
    return None

extractor = load_model()
df = load_data()

# --- 2. BUILD THE SIDEBAR SELECTOR ---
default_text = "Dataset not found. Please place mtsamples.csv in data/raw/"

if df is not None:
    st.sidebar.subheader("📂 Select Patient Data")
    
    # Get unique medical specialties
    specialties = df['medical_specialty'].unique()
    selected_specialty = st.sidebar.selectbox("1. Medical Specialty", specialties)
    
    # Filter dataset based on specialty
    filtered_df = df[df['medical_specialty'] == selected_specialty]
    
    # Let user select a specific note by its index/description
    note_options = filtered_df['description'].tolist()
    selected_note_desc = st.sidebar.selectbox("2. Patient Note", note_options)
    
    # Get the actual transcription text
    selected_row = filtered_df[filtered_df['description'] == selected_note_desc].iloc[0]
    default_text = selected_row['transcription']

# --- 3. THE MAIN INTERFACE ---
clinical_note = st.text_area(
    "Raw Clinical Text:",
    height=300,
    value=default_text
)

if st.button("Extract Medical Entities", type="primary"):
    with st.spinner("Running Neural Pipeline..."):
        results = extractor.extract_entities(clinical_note)
        
        st.subheader("Extracted Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🦠 Diseases & Disorders")
            if results["Disease_disorder"]:
                for item in set(results["Disease_disorder"]): # use set() to remove duplicates
                    st.error(f"• {item}")
            else:
                st.write("None detected.")
                
            st.markdown("### 🤒 Signs & Symptoms")
            if results["Sign_symptom"]:
                for item in set(results["Sign_symptom"]):
                    st.warning(f"• {item}")
            else:
                st.write("None detected.")
                
        with col2:
            st.markdown("### 💊 Medications")
            if results["Medication"]:
                for item in set(results["Medication"]):
                    st.success(f"• {item}")
            else:
                st.write("None detected.")
                
            st.markdown("### 🔬 Procedures")
            if results["Diagnostic_procedure"]:
                for item in set(results["Diagnostic_procedure"]):
                    st.info(f"• {item}")
            else:
                st.write("None detected.")