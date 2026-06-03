import streamlit as st
import sys
import os
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.search.retriever import MedicalRetriever

# Import Google Gemini and Prompt components
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# Configure Google API Key
load_dotenv()

st.set_page_config(page_title="Clinical Search Engine", layout="wide")

st.title("Clinical Evidence Search and Summarization")
st.markdown("Retrieves local medical records and uses LLM reasoning to generate evidence-backed clinical summaries.")

@st.cache_resource
def init_retriever():
    return MedicalRetriever()

@st.cache_resource
def init_llm():
    # Initializing the requested Gemini 1.5 Flash model
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

try:
    retriever = init_retriever()
    llm = init_llm()
    
    st.sidebar.header("Search Settings")
    num_results = st.sidebar.slider("Number of documents to retrieve (K):", min_value=1, max_value=5, value=3)
    
    query = st.text_input("Enter clinical terms, symptoms, or medical procedures:", "")
    
    if st.button("Run Semantic Search and Summarize"):
        if not query.strip():
            st.warning("Please enter a valid search term.")
        else:
            with st.spinner("Retrieving evidence and generating summary..."):
                # 1. Retrieve relevant data from ChromaDB
                results = retriever.get_clinical_evidence(query, k=num_results)
                
                if not results:
                    st.info("No matching clinical records found.")
                else:
                    # 2. Format the retrieved context blocks
                    context_text = "\n\n".join([f"Source ({res['specialty']}): {res['content']}" for res in results])
                    
                    # 3. Define the strict clinical prompt template
                    prompt_template = PromptTemplate(
                        input_variables=["context", "question"],
                        template="""You are an expert Clinical AI Assistant. 
                        You must answer the user's medical query using ONLY the provided clinical context below. 
                        If the answer cannot be found in the context, explicitly state "I cannot answer this based on the retrieved evidence."
                        Do NOT invent or hallucinate information.

                        Query: {question}

                        Clinical Context:
                        {context}

                        Clinical Summary:"""
                    )
                    
                    # 4. Generate response using Gemini
                    final_prompt = prompt_template.format(question=query, context=context_text)
                    ai_response = llm.invoke(final_prompt)
                    
                    st.success("Analysis Complete!")
                    top_similarity = results[0].get("similarity_score", 0)

                    if top_similarity < 0.45:
                        st.warning(
                            "The retrieved evidence may be weak. Interpret the generated summary carefully."
                        )
                    # Display the generated summary
                    st.markdown("### AI Clinical Summary")
                    st.info(ai_response.content)
                    st.caption(
                        "This summary is generated only from retrieved evidence. "
                        "It is for educational and research purposes and is not medical advice."
                    )
                    st.markdown("---")
                    
                    # Display the supporting database fragments
                    st.markdown("### Supporting Evidence (Retrieved Chunks)")
                    for i, res in enumerate(results):
                        with st.expander(
                            f"Source #{i+1} | {res['specialty']} "
                            f"(Similarity: {res.get('similarity_score', 'N/A')})"
                        ):
                            st.markdown(f"**File Description:** {res['document']}")
                            st.write(res['content'])

except Exception as e:
    st.error(f"System Error: {e}")