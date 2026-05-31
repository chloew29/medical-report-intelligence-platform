import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Hospital KPIs", layout="wide")

st.title("📊 Hospital Quality KPIs")
st.markdown("Analyzing operational quality metrics from the CMS dataset.")

# Load the cleaned data
data_path = "data/processed/cms_hospital_data_cleaned.csv"

if not os.path.exists(data_path):
    st.error(f"Cannot find data at {data_path}. Please run the ETL pipeline first.")
else:
    df = pd.read_csv(data_path)
    
    # --- TOP ROW: High-Level Metrics ---
    st.subheader("National Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Facilities Analyzed", f"{len(df):,}")
    
    with col2:
        # Calculate national average rating
        avg_rating = df['hospital_overall_rating'].mean()
        st.metric("National Avg Rating (Out of 5)", f"{avg_rating:.2f}" if pd.notnull(avg_rating) else "N/A")
        
    with col3:
        # Count how many unique states are in our dataset
        states_count = df['state'].nunique()
        st.metric("States Represented", states_count)

    st.divider()

    # --- MIDDLE ROW: Visualizations ---
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Average Rating by State")
        # Group by state and calculate average rating, dropping nulls
        state_avg = df.groupby('state')['hospital_overall_rating'].mean().reset_index()
        state_avg = state_avg.dropna().sort_values('hospital_overall_rating', ascending=False)
        
        # Plot using Plotly
        fig1 = px.bar(
            state_avg.head(15), # Show top 15 states to keep it clean
            x='state', 
            y='hospital_overall_rating',
            labels={'state': 'State', 'hospital_overall_rating': 'Avg Rating'},
            color='hospital_overall_rating',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col_chart2:
        st.subheader("Hospital Type Distribution")
        type_counts = df['hospital_type'].value_counts().reset_index()
        type_counts.columns = ['hospital_type', 'count']
        
        fig2 = px.pie(
            type_counts, 
            names='hospital_type', 
            values='count',
            hole=0.4 # Makes it a donut chart
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # --- BOTTOM ROW: Raw Data Explorer ---
    st.subheader("Raw Data Explorer")
    st.markdown("Filter and search the processed dataset below.")
    st.dataframe(df, use_container_width=True)