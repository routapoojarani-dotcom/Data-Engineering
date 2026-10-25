# ATM Transaction Data Engineering & Analytics  PySpark, Sqoop, S3, Redshift
## Architecture

```text
Source RDS / MySQL
        |
        | Sqoop
        v
      HDFS
        |
        | PySpark ETL
        v
  Curated dimensions + fact
        |
        +-----------------> Amazon S3
        |                       |
        |                       | COPY
        v                       v
              Amazon Redshift
                    |
                    v
             Analytical SQL
```

## Project at a glance

| Area | Implementation |
|---|---|
| Source ingestion | RDS / MySQL → HDFS using Sqoop |
| Distributed processing | PySpark |
| Data lake / staging | HDFS + Amazon S3 |
| Warehouse | Amazon Redshift |
| Data model | Star schema |
| Validation | Record-count reconciliation |
| Analytics | SQL queries for operational and transaction analysis |
| Scale demonstrated | **2,468,572 transaction records** |

## Data engineering workflow

### 1. Ingestion

The source transaction table was imported from RDS/MySQL into HDFS using Sqoop. The project evidence reports **2,468,572 records** imported and reconciled against the validation document.

The public version uses a parameterized command template rather than the original connection string or credentials.

See [`ingestion/sqoop_import.sh`](ingestion/sqoop_import.sh).

### 2. Transformation

The ETL layer is represented as a clean PySpark reference implementation. It defines an explicit schema, derives dimensional attributes, creates a transaction fact dataset and writes curated datasets for downstream loading.

See [`src/pyspark_etl.py`](src/pyspark_etl.py).

### 3. Dimensional model

The warehouse uses a star-schema design with:

- `DIM_LOCATION`
- `DIM_ATM`
- `DIM_DATE`
- `DIM_CARD_TYPE`
- `FACT_ATM_TRANS`

The fact table contains transaction, ATM, date, card-type and weather-related attributes.

See [`sql/01_schema.sql`](sql/01_schema.sql).

### 4. S3 → Redshift

Curated datasets are staged in Amazon S3 and loaded into the Redshift dimensional model using `COPY`.

Public examples use placeholders:

```sql
COPY atm_data.dim_location
FROM 's3://<bucket>/dim_location/'
IAM_ROLE '<redshift-role-arn>'
FORMAT AS CSV;
```

See [`sql/02_load_templates.sql`](sql/02_load_templates.sql).

### 5. Analytical layer

The project includes analytical SQL addressing:

- ATMs with high inactive-transaction rates;
- ATM failures by weather condition;
- highest-volume ATMs;
- monthly inactive-transaction trends;
- highest withdrawal amounts;
- failures by card type;
- weekday vs weekend transaction volumes;
- most active day at a selected location.

See [`sql/03_analytical_queries.sql`](sql/03_analytical_queries.sql).

## Validation approach

The original project evidence provides a concrete control point: the Sqoop ingestion produced **2,468,572 records**, consistent with the supplied validation document.

For a production implementation, the same reconciliation principle should be applied at each boundary:

```text
source count
    =
HDFS landing count
    =
curated fact count
    =
warehouse fact count
```

Additional controls recommended for extension include duplicate transaction-ID detection, null-rate checks, referential-integrity checks, rejected-record counts and source-to-target aggregate reconciliation.

## Repository structure

```text
.
├── README.md
├── LICENSE
├── .gitignore
├── ingestion/
│   ├── README.md
│   └── sqoop_import.sh
├── src/
│   └── pyspark_etl.py
├── sql/
│   ├── 01_schema.sql
│   ├── 02_load_templates.sql
│   └── 03_analytical_queries.sql
├── docs/
│   ├── DATA_MODEL.md
│   ├── DATA_PROVENANCE.md
│   └── ENGINEERING_NOTES.md
└── tests/
    └── test_repository.py
```

## Reproducibility and security

This public repository deliberately excludes database passwords, AWS account IDs, IAM credentials, provider-specific screenshots, raw proprietary project documents and production connection strings.

Use environment variables, AWS IAM roles and a secrets manager for real deployments.

## Future improvements

- Add an executable local Spark test dataset.
- Add automated data-quality checks.
- Add CI for Python and SQL linting.
- Add Infrastructure-as-Code for S3/Redshift resources.
- Add orchestration such as Airflow.
- Add a BI/dashboard layer.
