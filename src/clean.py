import os
import pandas as pd

def clean_and_deduplicate():
    raw_path = os.path.join("data", "raw_models.csv")
    cleaned_path = os.path.join("data", "cleaned_models.csv")

    if not os.path.exists(raw_path):
        print(f"Error: {raw_path} does not exist. Run extract.py first.")
        return

    df = pd.read_csv(raw_path)
    print(f"Initial raw rows loaded: {len(df)}")

    # 1. Clean string fields
    df['model_id'] = df['model_id'].astype(str).str.strip()
    df = df[df['model_id'] != ""]

    # 2. Strict Deduplication by unique model_id
    df_clean = df.drop_duplicates(subset=['model_id'], keep='first')
    print(f"Rows after strict deduplication: {len(df_clean)}")

    # 3. Fill missing values
    df_clean['pipeline_tag'] = df_clean['pipeline_tag'].fillna("uncategorized")
    df_clean['library_name'] = df_clean['library_name'].fillna("unknown")
    df_clean['downloads'] = df_clean['downloads'].fillna(0).astype(int)
    df_clean['likes'] = df_clean['likes'].fillna(0).astype(int)

    # 4. Enforce exactly 2,000 unique records target
    if len(df_clean) >= 2000:
        df_clean = df_clean.iloc[:2000]

    df_clean.to_csv(cleaned_path, index=False)
    print(f"Cleaned dataset saved successfully to {cleaned_path} with exactly {len(df_clean)} unique records.")

if __name__ == "__main__":
    clean_and_deduplicate()