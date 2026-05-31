import pandas as pd
import numpy as np
import os

def clean_cms_data():
    print("Starting Data Cleaning Process...")
    
    input_path = "data/raw/cms_hospital_data_raw.csv"
    output_dir = "data/processed"
    output_path = os.path.join(output_dir, "cms_hospital_data_cleaned.csv")
    
    if not os.path.exists(input_path):
        print(f"Error: Could not find {input_path}. Run ingest_cms.py first.")
        return
        
    # Load raw data
    df = pd.read_csv(input_path)
    print(f"Loaded {len(df)} records for cleaning.")
    
    # 1. Standardize column names (lowercase, replace spaces with underscores)
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    
    # 2. Select the columns we care about for the KPI Dashboard
    desired_columns = ['facility_id', 'facility_name', 'state', 'hospital_overall_rating', 'hospital_type']
    
    # Only keep columns that actually exist in the dataframe to prevent key errors
    available_columns = [col for col in desired_columns if col in df.columns]
    df = df[available_columns]
    
    # 3. Handle missing data (CMS uses "Not Available" as text)
    if 'hospital_overall_rating' in df.columns:
        df['hospital_overall_rating'] = df['hospital_overall_rating'].replace('Not Available', np.nan)
        # Convert to numeric, forcing any weird text into proper NaN values
        df['hospital_overall_rating'] = pd.to_numeric(df['hospital_overall_rating'], errors='coerce')
    
    # 4. Drop rows that are missing a core facility ID
    if 'facility_id' in df.columns:
        df = df.dropna(subset=['facility_id'])
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the processed data
    df.to_csv(output_path, index=False)
    print(f"Successfully cleaned data. Saved {len(df)} records to: {output_path}")

if __name__ == "__main__":
    clean_cms_data()