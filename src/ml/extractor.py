from transformers import pipeline

class ClinicalEntityExtractor:
    def __init__(self):
        # We load the model once when the class is initialized
        self.model_name = "d4data/biomedical-ner-all"
        print(f"Loading {self.model_name}...")
        self.ner_pipeline = pipeline(
            "token-classification", 
            model=self.model_name, 
            tokenizer=self.model_name, 
            aggregation_strategy="simple" # Critical for medical terminology
        )

    def extract_entities(self, text: str) -> dict:
        """
        Takes raw clinical text and returns a categorized dictionary of entities.
        """
        # If the text is too long, we truncate it to avoid crashing the model
        if len(text) > 2000:
            text = text[:2000]
            
        raw_results = self.ner_pipeline(text)
        
        # Initialize categorized output
        categorized_data = {
            "Sign_symptom": [],
            "Medication": [],
            "Disease_disorder": [],
            "Diagnostic_procedure": []
        }
        
        for entity in raw_results:
            group = entity['entity_group']
            word = entity['word'].strip()
            
            # Map the model's tags to our clean categories
            if group in categorized_data and word not in categorized_data[group]:
                categorized_data[group].append(word)
                
        return categorized_data