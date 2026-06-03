import os
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class MedicalRetriever:
    def __init__(self):
        self.db_path = "data/simple_vector_db.pkl"

        if not os.path.exists(self.db_path):
            raise FileNotFoundError(
                "Simple vector database not found. Please run: python src/ml/build_vector_db.py"
            )

        print("Loading simple vector database...")
        with open(self.db_path, "rb") as f:
            self.vector_db = pickle.load(f)

        print("Loading embedding model...")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def get_clinical_evidence(self, query: str, k: int = 3):
        query_embedding = self.model.encode([query], convert_to_numpy=True)

        similarities = cosine_similarity(
            query_embedding,
            self.vector_db["embeddings"]
        )[0]

        top_indices = np.argsort(similarities)[::-1][:k]

        evidence_list = []

        for idx in top_indices:
            meta = self.vector_db["metadata"][idx]

            evidence_list.append({
                "content": self.vector_db["texts"][idx],
                "specialty": meta.get("specialty", "Unknown"),
                "document": meta.get("description", "Unknown"),
                "distance_score": round(float(1 - similarities[idx]), 4),
                "similarity_score": round(float(similarities[idx]), 4)
            })

        return evidence_list

if __name__ == "__main__":
    retriever = MedicalRetriever()

    test_query = "What are the symptoms of upper respiratory infection?"
    print(f"\nSearching database for: {test_query}")

    results = retriever.get_clinical_evidence(test_query, k=3)

    for i, res in enumerate(results):
        print(f"\n--- Evidence #{i+1} ---")
        print(f"Similarity: {res['similarity_score']}")
        print(f"Specialty: {res['specialty']}")
        print(f"Description: {res['document']}")
        print(f"Text: {res['content'][:500]}...")