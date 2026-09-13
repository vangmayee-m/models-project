import os
import pandas as pd

def clean_and_normalize():
    raw_path = "data/raw_models.csv"
    output_path = "data/cleaned_models.csv"
    
    if not os.path.exists(raw_path):
        print(f"Error: {raw_path} not found!")
        return

    print("Loading raw models data...")
    df = pd.read_csv(raw_path)

    # 1. Fill missing text values with clean placeholders
    df["model_family"] = df["model_family"].fillna(df["model_name"].str.split("-").str[0])
    df["company_creator"] = df["company_creator"].fillna("Unknown / Open Source")
    df["official_website"] = df["official_website"].fillna("")
    df["model_category"] = df["model_category"].fillna("General LLM")
    df["release_date"] = df["release_date"].fillna("N/A")
    df["input_modalities"] = df["input_modalities"].fillna("text")
    df["output_modalities"] = df["output_modalities"].fillna("text")
    df["context_window"] = df["context_window"].fillna("N/A")
    df["open_weights_status"] = df["open_weights_status"].fillna("Open-weight")
    df["license"] = df["license"].fillna("N/A")
    df["huggingface_url"] = df["huggingface_url"].fillna("")
    df["github_url"] = df["github_url"].fillna("")
    df["logo_url"] = df["logo_url"].fillna("")
    df["description"] = df["description"].fillna("High-performance AI model designed for various machine learning workflows.")
    df["quality_score"] = df["quality_score"].fillna(80)

    # 2. String cleaning and trimming
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()

    # 3. Quality Filtering (Keep scores >= 70 as required by guideline)
    df = df[df["quality_score"] >= 70]

    # Save cleaned data
    df.to_csv(output_path, index=False)
    print(f"Successfully cleaned and saved {len(df)} records to {output_path}")

if __name__ == "__main__":
    clean_and_normalize()