import os
import requests
import pandas as pd

def fetch_models_dev():
    print("Fetching models from models.dev API...")
    url = "https://raw.githubusercontent.com/anomalyco/models.dev/main/models.json"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            records = []
            
            items = data.values() if isinstance(data, dict) else data
            for item in items:
                if not isinstance(item, dict):
                    continue
                records.append({
                    "model_name": item.get("name") or item.get("id"),
                    "model_family": item.get("family", ""),
                    "company_creator": item.get("provider") or item.get("company", ""),
                    "official_website": item.get("website", ""),
                    "model_category": item.get("category") or item.get("type", "General LLM"),
                    "release_date": item.get("release_date", ""),
                    "input_modalities": ", ".join(item.get("modalities", {}).get("input", ["text"])) if isinstance(item.get("modalities"), dict) else "text",
                    "output_modalities": ", ".join(item.get("modalities", {}).get("output", ["text"])) if isinstance(item.get("modalities"), dict) else "text",
                    "context_window": item.get("context_limit") or item.get("context_window", ""),
                    "open_weights_status": "Open-weight" if item.get("open_weights") else "Closed",
                    "license": item.get("license", ""),
                    "huggingface_url": item.get("huggingface_url", ""),
                    "github_url": item.get("github_url", ""),
                    "logo_url": item.get("logo", ""),
                    "description": item.get("description", ""),
                    "quality_score": 85
                })
            return records
    except Exception as e:
        print(f"Failed to fetch from models.dev: {e}")
    return []

def fetch_huggingface_top_models(limit=500):
    print("Fetching top models from Hugging Face Hub API...")
    url = f"https://huggingface.co/api/models?sort=downloads&direction=-1&limit={limit}"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            records = []
            for item in data:
                model_id = item.get("id", "")
                parts = model_id.split("/")
                creator = parts[0] if len(parts) > 1 else "Community"
                name = parts[1] if len(parts) > 1 else parts[0]
                
                # Filter out fine-tunes / GGUF / quant variants as per guidelines
                if any(tag in name.lower() for tag in ["gguf", "awq", "gptq", "lora", "adapter", "v0.", "checkpoints"]):
                    continue

                records.append({
                    "model_name": name,
                    "model_family": name.split("-")[0],
                    "company_creator": creator,
                    "official_website": f"https://huggingface.co/{model_id}",
                    "model_category": item.get("pipeline_tag", "General ML"),
                    "release_date": item.get("createdAt", "")[:10] if item.get("createdAt") else "",
                    "input_modalities": "text",
                    "output_modalities": "text",
                    "context_window": "",
                    "open_weights_status": "Open-weight",
                    "license": "",
                    "huggingface_url": f"https://huggingface.co/{model_id}",
                    "github_url": "",
                    "logo_url": "",
                    "description": f"{name} is an AI model developed by {creator} for {item.get('pipeline_tag', 'general ML tasks')}.",
                    "quality_score": 80
                })
            return records
    except Exception as e:
        print(f"Failed to fetch from Hugging Face API: {e}")
    return []

def main():
    os.makedirs("data", exist_ok=True)
    models_dev = fetch_models_dev()
    hf_models = fetch_huggingface_top_models(limit=500)
    
    combined = models_dev + hf_models
    df = pd.DataFrame(combined)
    
    # Simple Deduplication on Model Name
    df.drop_duplicates(subset=["model_name"], inplace=True)
    
    output_path = "data/raw_models.csv"
    df.to_csv(output_path, index=False)
    print(f"Successfully extracted {len(df)} records to {output_path}")

if __name__ == "__main__":
    main()