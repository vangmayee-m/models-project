import os
import time
import pandas as pd
import requests

def fetch_huggingface_models(target_raw_count=3500):
    print(f"Starting extraction to fetch at least {target_raw_count} raw models...")
    all_models = []
    limit_per_page = 100
    skip = 0
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    while len(all_models) < target_raw_count:
        url = f"https://huggingface.co/api/models?limit={limit_per_page}&skip={skip}&full=true"
        headers = {"User-Agent": "Mozilla/5.0"}
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if not data:
                    print("No more models found on Hugging Face.")
                    break
                all_models.extend(data)
                skip += limit_per_page
                print(f"Fetched {len(all_models)} raw records...")
            else:
                print(f"Error fetching data: HTTP {response.status_code}")
                break
        except Exception as e:
            print(f"Request exception: {e}")
            break
            
        time.sleep(0.1)  # Respect API rate limits

    # Parse key metadata into DataFrame
    parsed_data = []
    for m in all_models:
        parsed_data.append({
            "model_id": m.get("id", ""),
            "author": m.get("author", ""),
            "downloads": m.get("downloads", 0),
            "likes": m.get("likes", 0),
            "pipeline_tag": m.get("pipeline_tag", "uncategorized"),
            "library_name": m.get("library_name", ""),
            "last_modified": m.get("lastModified", "")
        })

    df_raw = pd.DataFrame(parsed_data)
    raw_path = os.path.join("data", "raw_models.csv")
    df_raw.to_csv(raw_path, index=False)
    print(f"Successfully saved {len(df_raw)} raw records to {raw_path}")

if __name__ == "__main__":
    fetch_huggingface_models()