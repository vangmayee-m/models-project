# Hugging Face Models Dataset Pipeline (`models-project`)

This repository contains an end-to-end data processing pipeline that extracts model metadata from the Hugging Face Hub API, cleans and deduplicates the records, generates enriched descriptions, and saves the final dataset of exactly **2,000 unique models**.

---

## 📌 Project Overview

* **Data Source**: Hugging Face Hub API (`https://huggingface.co/api/models`)
* **Target Record Count**: Exactly 2,000 unique records (2,001 rows including CSV headers)
* **Deduplication Strategy**: Strict unique constraint on `model_id` to eliminate duplicates
* **Output Artifacts**: 
  * `data/raw_models.csv` (Raw extracted data)
  * `data/cleaned_models.csv` (Deduplicated top 2,000 records)
  * `data/final_models.csv` (Final processed dataset)

---

## 📁 Repository Structure

```text
models-project/
├── data/
│   ├── raw_models.csv
│   ├── cleaned_models.csv
│   └── final_models.csv
├── src/
│   ├── extract.py
│   ├── clean.py
│   └── generate_descriptions.py
├── README.md
└── requirements.txt