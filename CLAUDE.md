# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Does

An ELT data pipeline that moves movie data from MongoDB Atlas (`sample_mflix`) to Snowflake, transforms it with dbt, and orchestrates everything via Dagster. The four stages are:

1. **Extract & Load** (`extract_load/`) — Python scripts pull from MongoDB and push raw strings into Snowflake `RAW.RAW_MOVIES`
2. **Transform** (`dbttransform/`) — dbt casts types in staging, applies business logic in marts
3. **Orchestrate** (`orchestration/`) — Dagster wraps the dbt project as software-defined assets
4. **Visualize** — Metabase connects to the dbt mart tables in Snowflake

## Environment Setup

Credentials live in `.env` (not committed). Required variables:

```
MONGO_URI
SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PASSWORD
SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA, SNOWFLAKE_WAREHOUSE, SNOWFLAKE_ROLE
```

Activate the virtual environment before running anything:

```bash
source .venv/bin/activate
```

## Commands

### Extract & Load

```bash
# Run from repo root (mongo_extract.py imports snowflake_load via relative import)
cd extract_load && python mongo_extract.py
```

### dbt

```bash
cd dbttransform
dbt run          # run all models
dbt run --select stg_movies   # run a single model
dbt test
dbt build        # run + test together
```

### Dagster

The Dagster package is installed from `orchestration/` (editable install via `pyproject.toml`):

```bash
cd orchestration
pip install -e ".[dev]"
dagster dev      # starts the Dagster UI at localhost:3000
```

The Dagster entry point is `orchestration.definitions` (set in `pyproject.toml` `[tool.dagster]`).

## Architecture Notes

### Data flow and type strategy
Raw data lands in Snowflake as **all strings** (enforced in `snowflake_load.py` via `df.astype(str)`). Type casting happens exclusively in the dbt staging layer (`stg_movies.sql` uses `try_to_number`, `to_varchar`). This prevents load failures from MongoDB's mixed-type BSON fields.

### dbt schema layout
- Source: `MONGODB.RAW.RAW_MOVIES` (defined in `models/staging/sources.yml`)
- Staging models → `MONGODB.STAGING.*` (materialized as views)
- Mart models → `MONGODB.MARTS.*` (materialized as tables)

The custom `generate_schema_name.sql` macro in `dbttransform/macros/` controls schema naming.

### Dagster ↔ dbt integration
`orchestration/orchestration/project.py` resolves the dbt project path relative to the Python package location. `DbtProject.prepare_if_dev()` auto-generates the dbt manifest during local development so `@dbt_assets(manifest=...)` works without a manual `dbt parse` step.

### Scheduling
`orchestration/orchestration/schedules.py` has a daily schedule stubbed out but commented. Uncomment and configure `build_schedule_from_dbt_selection` to activate it.
