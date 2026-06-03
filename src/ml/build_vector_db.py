import os
import pickle
import pandas as pd
from sentence_transformers import SentenceTransformer

def build_database():
    print("Starting Simple Vector Database Build...")

    input_path = "data/raw/mtsamples.csv"
    output_path = "data/simple_vector_db.pkl"

    if not os.path.exists(input_path):
        print(f"ERROR: Could not find {input_path}")
        return

    df = pd.read_csv(input_path)
    df = df.dropna(subset=["transcription"])

    # Keep MVP small and stable
    df_sample = df.head(2000)

    texts = []
    metadata = []

    for _, row in df_sample.iterrows():
        text = str(row["transcription"])

        # Split long notes into smaller chunks
        chunk_size = 700
        overlap = 100

        for start in range(0, len(text), chunk_size - overlap):
            chunk = text[start:start + chunk_size].strip()

            if len(chunk) < 100:
                continue

            texts.append(chunk)
            metadata.append({
                "specialty": str(row.get("medical_specialty", "Unknown")),
                "description": str(row.get("description", "Unknown"))
            })

    print(f"Created {len(texts)} text chunks.")

    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Creating embeddings...")
    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    vector_db = {
        "texts": texts,
        "metadata": metadata,
        "embeddings": embeddings
    }

    os.makedirs("data", exist_ok=True)

    with open(output_path, "wb") as f:
        pickle.dump(vector_db, f)

    print(f"Success! Simple vector database saved to: {output_path}")

if __name__ == "__main__":
    build_database()