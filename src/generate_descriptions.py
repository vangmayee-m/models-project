import os
import pandas as pd

def enrich_descriptions():
    input_path = "data/cleaned_models.csv"
    output_path = "data/final_models.csv"
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found!")
        return

    print("Generating standardized model descriptions...")
    df = pd.read_csv(input_path)

    # Template-based rapid enrichment for standardized, concise LLM-style descriptions
    def build_desc(row):
        name = row.get("model_name", "Model")
        creator = row.get("company_creator", "the AI ecosystem")
        category = row.get("model_category", "general ML")
        weights = row.get("open_weights_status", "Open-weight")
        
        return f"{name} is a high-performance {weights.lower()} AI model developed by {creator}, optimized for {category} applications and production workflows."

    df["description"] = df.apply(build_desc, axis=1)

    # Save to final CSV
    df.to_csv(output_path, index=False)
    print(f"Successfully generated descriptions and created final dataset at {output_path} with {len(df)} records!")

if __name__ == "__main__":
    enrich_descriptions()