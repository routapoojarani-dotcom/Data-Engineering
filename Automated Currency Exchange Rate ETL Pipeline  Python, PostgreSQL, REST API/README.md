# Automated Currency Exchange Rate ETL Pipeline | Python, PostgreSQL, REST API

A daily ETL pipeline that fetches official currency exchange rates from the
**National Bank of Poland (NBP) API** and loads them into PostgreSQL with
incremental loading — so you always have the latest data without duplicates.

---

## What problem does it solve?

Businesses that operate in multiple currencies need up-to-date exchange rates
to calculate prices, invoices, and reports. Manual updates are slow and error-prone.

This pipeline automates the whole process:
- Fetches rates from the official NBP API (table A — 30+ currencies)
- Validates the data before loading
- Loads only new records (incremental load — no duplicates)
- Can backfill up to 12 months of history on first run
- Runs automatically twice a day via scheduler

---

## Architecture

```
┌──────────────────┐
│   NBP REST API   │   ← official exchange rates, 30+ currencies
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   EXTRACT        │   requests + tenacity retries
│   (Python)       │   handles weekends & holidays (404)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   TRANSFORM      │   Pandas: cleaning, type casting
│   + VALIDATION   │   validate currency codes, positive rates
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  INCREMENTAL     │   only new rows (WHERE date > last_loaded)
│  LOAD            │   PostgreSQL COPY protocol
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   PostgreSQL     │   table: currency_rates
│                  │   unique constraint (currency_code, effective_date)
└──────────────────┘
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| **Python 3.12** | Core language |
| **requests** | HTTP client for NBP API |
| **Tenacity** | Retries with exponential backoff |
| **Pandas** | Data transformation |
| **psycopg2** | PostgreSQL driver |
| **PostgreSQL 15** | Target database |
| **Docker & Compose** | Reproducibility |
| **schedule** | Daily cron-like scheduler |
| **pytest** | Unit testing |
| **GitHub Actions** | CI/CD |

---

## Project Structure

```
nbp-etl-pipeline/
├── .github/workflows/       # GitHub Actions (tests on push)
├── config/
│   └── config.yaml          # DB + API configuration
├── data/raw/                # (not in repo)
├── docs/
│   ├── architecture.png
│   └── screenshots/
├── sql/
│   ├── 01_init_schema.sql   # table + indexes
│   └── 02_analytics.sql     # example queries
├── src/
│   ├── cli.py               # argparse CLI
│   ├── config_loader.py     # YAML + .env loader
│   ├── extract.py           # API client with retries
│   ├── transform.py         # Pandas transformations
│   ├── validation.py        # data validation rules
│   ├── load.py              # incremental load via COPY
│   ├── pipeline.py          # orchestration
│   ├── scheduler.py         # daily runs at 08:00 & 15:00
│   └── logging_config.py    # rotating file logger
├── tests/
│   ├── conftest.py          # pytest fixtures
│   └── test_transform.py    # 11 unit tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---
---


### Table `currency_rates`

| currency_code | currency_name | rate | effective_date | table_no |
|---|---|---|---|---|
| USD | dolar amerykański | 3.8404 | 2026-09-25 | 187/A/NBP/2026 |
| EUR | euro | 4.2810 | 2026-09-25 | 187/A/NBP/2026 |
| GBP | funt szterling | 4.9812 | 2026-09-25 | 187/A/NBP/2026 |
| UAH | hrywna | 0.0855 | 2026-09-25 | 187/A/NBP/2026 |



## What This Project Demonstrates

- **REST API integration** — HTTP client with retry logic and error handling
- **Incremental loading** — only new rows, no duplicates
- **Backfill strategy** — first run fills history, next runs are fast
- **Data validation** — before data reaches the database
- **Scheduling** — daily automated runs
- **PostgreSQL COPY** — high-performance bulk loading
- **Docker Compose** — reproducible environment
- **Unit testing** — 11 tests, GitHub Actions CI

---