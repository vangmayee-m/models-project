\# AIOrbit - Models Dataset \& Pipeline



An automated end-to-end pipeline for discovering, cleaning, deduplicating, and enriching metadata for 427 AI/ML models into a unified dataset.



\---



\## 🏗️ System Architecture \& Data Pipeline



```text

&#x20; \[ models.dev API ]        \[ Hugging Face Hub ]

&#x20;         │                          │

&#x20;         └───────────┐  ┌───────────┘

&#x20;                     ▼  ▼

&#x20;           ┌──────────────────────┐

&#x20;           │   src/extract.py     │  ──> Raw Data Ingestion

&#x20;           └──────────┬───────────┘

&#x20;                      │ (data/raw\_models.csv)

&#x20;                      ▼

&#x20;           ┌──────────────────────┐

&#x20;           │    src/clean.py      │  ──> Deduplication \& Quality Filtering (>70 score)

&#x20;           └──────────┬───────────┘

&#x20;                      │ (data/cleaned\_models.csv)

&#x20;                      ▼

&#x20;           ┌──────────────────────┐

&#x20;           │src/generate\_descs.py │  ──> LLM Description Standardization (Gemini API)

&#x20;           └──────────┬───────────┘

&#x20;                      │ (data/final\_models.csv)

&#x20;                      ▼

&#x20;        ┌────────────────────────────┐

&#x20;        │ Public Google Sheets Sync  │  ──> Final AIOrbit Dataset (427 Models)

&#x20;        └────────────────────────────┘

models-project/

│

├── data/

│   ├── raw\_models.csv         # Raw extracted API records

│   ├── cleaned\_models.csv     # Deduplicated \& filtered records

│   └── final\_models.csv       # Standardized \& LLM-enriched dataset (427 rows)

│

├── src/

│   ├── extract.py             # API fetching module

│   ├── clean.py               # Data hygiene \& quality evaluation logic

│   └── generate\_descriptions.py # Gemini API enrichment script

│

├── README.md                  # Project documentation \& architecture

└── requirements.txt           # Environment dependencies

