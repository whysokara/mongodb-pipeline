# Dagster MongoDB to Snowflake Pipeline

This project orchestrates a data pipeline that extracts movie data from MongoDB (sample_mflix), loads it into Snowflake as raw files, transforms it using dbt, and prepares it for visualization in Metabase.

## Project Structure

```text
dagster-mongodb/
├── .env                        # Secrets: Mongo URIs, Snowflake credentials (DO NOT COMMIT)
├── .gitignore                  # Git ignore file
├── requirements.txt            # Unified list of dependencies
├── README.md                   # Project documentation
│
├── extract_load/               # Step 1: Python scripts for Extract & Load
│   ├── __init__.py
│   ├── mongo_extract.py        # Logic to pull sample_mflix data from MongoDB
│   └── snowflake_load.py       # Logic to upload raw data into Snowflake
│
├── dbt_transform/              # Step 2: dbt project for Transformations
│   └── ... (to be initialized via dbt init)
│
├── orchestration/              # Step 3: Dagster for Orchestration
│   └── ... (to be initialized)
│
└── metabase/                   # Step 4: BI / Visualization
    └── metabase_setup.md       # Notes on connecting Metabase to dbt marts
```

## Progress & Current Status

### 1. Environment Setup
- [x] Created project folder structure.
- [x] Initialized virtual environment (`.venv`).
- [x] Created `requirements.txt` with Dagster, dbt, Snowflake, and MongoDB dependencies.
- [x] Resolved macOS SSL certificate issues using `certifi`.
- [x] Secured credentials using `.env` and `.gitignore`.

### 2. Extract & Load (Complete)
- [x] **MongoDB Connection:** Successfully connected to MongoDB Atlas `sample_mflix` database.
- [x] **Data Extraction:** Implemented logic to extract data into pandas DataFrames.
- [x] **Snowflake Loading:** Created `snowflake_load.py` using `write_pandas` with automatic table creation.
- [x] **Data Integrity:** Implemented string-only loading for the RAW layer to avoid conversion errors.
- [x] **Pipeline Test:** Successfully moved data from MongoDB to Snowflake `RAW_MOVIES` table.

### 3. dbt Transformation (Next Step)
- [ ] Initialize dbt project using `dbt init dbt_transform`.
- [ ] Configure `profiles.yml` for Snowflake connection.
- [ ] Create staging models to clean raw movie data.
- [ ] Create mart models for BI consumption.

## Getting Started

### Prerequisites
- Python 3.10+
- A MongoDB Atlas account with `sample_mflix` dataset.
- A Snowflake account.

### Installation

1. Clone the repository and navigate to the root:
   ```bash
   cd dagster-mongodb
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your `.env` file with your MongoDB and Snowflake credentials.

5. Run the full extraction and load process:
   ```bash
   python extract_load/mongo_extract.py
   ```
