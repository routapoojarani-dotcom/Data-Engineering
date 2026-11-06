# Retail Data Lake and Automated Analytics Platform Using AWS

An end-to-end, event-driven retail sales data engineering platform built on AWS. The project simulates a daily ERP/POS sales-feed workflow and demonstrates ingestion, orchestration, PySpark ETL, data-quality validation, curated analytics storage, SQL analytics, warehouse modeling, and BI reporting.

## Project Objective

Build a production-style data pipeline that:

- Ingests a new daily retail sales CSV into Amazon S3.
- Automatically triggers processing when a new sales file arrives.
- Orchestrates ETL using AWS Step Functions.
- Cleans, validates, deduplicates, and enriches data with AWS Glue PySpark.
- Separates valid and rejected records.
- Stores curated data as partitioned Parquet files.
- Catalogs curated data with AWS Glue Data Catalog.
- Provides serverless SQL analytics using Amazon Athena.
- Loads curated data into an Amazon Redshift warehouse for dimensional analytics.
- Supports BI reporting through Amazon QuickSight.
- Provides failure notification through Amazon SNS.

## Architecture

```text
                    ERP / POS DAILY SALES FILE
                              |
                              | CSV
                              v
                    +-------------------+
                    |   Amazon S3 RAW   |
                    |   raw/sales/       |
                    +-------------------+
                              |
                         ObjectCreated
                              |
                              v
                    +-------------------+
                    |    AWS Lambda     |
                    | S3 Event Trigger  |
                    +-------------------+
                              |
                              v
                    +-------------------+
                    | AWS Step Functions|
                    |  Orchestration     |
                    +-------------------+
                              |
                              v
                    +-------------------+
                    |   AWS Glue        |
                    |   PySpark ETL     |
                    +-------------------+
                         /           \
                        /             \
                       v               v
                VALID RECORDS     INVALID RECORDS
                     |                  |
                     v                  v
              S3 CURATED          S3 REJECTED
               Parquet/Date        CSV/Date
                     |
                     v
             Glue Data Catalog
                /          \
               /            \
              v              v
          Amazon Athena   Amazon Redshift
              |                |
              |                v
              |          Star Schema
              |                |
              +-------+--------+
                      |
                      v
              Amazon QuickSight

           Failure path -> Amazon SNS
```

## AWS Services

| Service | Purpose |
|---|---|
| Amazon S3 | Raw, curated, rejected and Athena-result storage |
| AWS Lambda | S3 event-driven ingestion trigger |
| AWS Step Functions | Pipeline orchestration |
| AWS Glue | PySpark ETL and data processing |
| Glue Data Catalog | Metadata and table/partition cataloging |
| Amazon Athena | Serverless SQL analytics on curated Parquet |
| Amazon Redshift Serverless | Data warehouse and dimensional analytics |
| Amazon QuickSight | BI dashboarding |
| Amazon SNS | Failure notifications |
| Amazon CloudWatch | Logs and operational monitoring |

## S3 Data Layout

```text
s3://retail-de-project-project/
|
├── raw/
│   ├── sales/
│   │   └── sales_YYYY_MM_DD.csv
│   ├── products/
│   │   └── products.csv
│   └── stores/
│       └── stores.csv
│
├── processed/
│
├── curated/
│   └── sales/
│       └── transaction_date=YYYY-MM-DD/
│           └── *.parquet
│
├── rejected/
│   └── sales/
│       └── transaction_date=YYYY-MM-DD/
│           └── *.csv
│
├── scripts/
│
└── athena-results/
```

## End-to-End Data Flow

### 1. Daily ERP File

A daily sales file is generated with a filename such as:

```text
sales_2026_09_25.csv
```

### 2. S3 Raw Layer

The file is uploaded to:

```text
raw/sales/
```

### 3. S3 Event

The `ObjectCreated` event triggers:

```text
retail-s3-ingestion-trigger
```

### 4. Lambda

Lambda extracts:

- Bucket name
- Object key
- File name

and starts:

```text
retail-daily-sales-pipeline
```

The execution name is deterministic, for example:

```text
sales_2026_09_25_csv
```

This supports duplicate execution protection for the same file.

### 5. Step Functions

The workflow passes the exact S3 object key to the Glue job.

```text
ValidateERPFile
      ↓
RunGlueETL
      ↓
CheckCuratedCrawler
      ↓
StartCuratedCrawler
      ↓
WaitForCrawler
      ↓
CheckCrawlerAfterWait
      ↓
PipelineSuccess
```

Failure path:

```text
Glue/Crawler Failure
        ↓
SNS Notification
        ↓
PipelineFailed
```

### 6. Glue PySpark ETL

The Glue job:

- Reads the daily sales CSV.
- Reads product master data.
- Reads store master data.
- Standardizes columns and data types.
- Removes duplicate master records.
- Detects duplicate transaction IDs.
- Validates business rules.
- Joins products and stores.
- Calculates revenue and profit.
- Adds ingestion metadata.
- Writes valid records as Parquet.
- Writes rejected records as CSV.

### 7. Data Quality Rules

The pipeline checks:

- Required transaction ID.
- Valid transaction date.
- Required store ID.
- Required product ID.
- Quantity greater than zero.
- Unit price greater than zero.
- Payment method in `UPI`, `CARD`, or `CASH`.
- Product exists in the product master.
- Store exists in the store master.
- Duplicate transaction IDs.

### 8. Curated Layer

Valid sales records are written as partitioned Parquet:

```text
curated/sales/transaction_date=YYYY-MM-DD/
```

Invalid data is written separately:

```text
rejected/sales/transaction_date=YYYY-MM-DD/
```

### 9. Glue Data Catalog

The curated crawler updates metadata and partitions for Athena.

### 10. Athena

Athena queries the curated Parquet layer and provides analytics such as:

- Daily sales.
- Product performance.
- Store/state performance.
- Category performance.
- Payment-method performance.
- Customer analysis.
- Revenue and profit analysis.
- Data-quality checks.

### 11. Redshift

The warehouse layer uses:

```text
retail_dw
├── sales_stage_raw
├── sales_stage
├── product_stage
├── store_stage
├── dim_product
├── dim_store
├── dim_date
├── fact_sales
└── etl_file_control
```

The warehouse follows a star-schema approach:

```text
                 dim_date
                    |
                    |
 dim_product ---- fact_sales ---- dim_store
                    |
                    |
              customer_id
```

Daily curated partitions are loaded into staging and merged into `fact_sales` using `transaction_id` as the business key.

### 12. QuickSight

The BI layer can present:

- Total revenue.
- Total profit.
- Transactions.
- Units sold.
- Daily revenue trend.
- Revenue by state.
- Revenue by category.
- Top products.
- Profit by state.
- Payment methods.

## Incremental Loading

This project uses **incremental file-based ingestion**.

A new daily file is processed independently:

```text
Day 1 -> sales_2026_09_25.csv
Day 2 -> sales_2026_09_26.csv
Day 3 -> sales_2026_09_27.csv
```

Glue writes daily partitions:

```text
curated/sales/transaction_date=2026-09-25/
curated/sales/transaction_date=2026-09-26/
curated/sales/transaction_date=2026-09-27/
```

Manual S3 upload is used to simulate the ERP system. The pipeline itself is event-driven and processes the newly arrived object key rather than reprocessing the entire historical dataset.

The Redshift warehouse uses staging plus `MERGE` to avoid duplicate insertion of previously loaded transactions.

## Data Model

### Sales Source

| Column | Description |
|---|---|
| transaction_id | Sales transaction identifier |
| transaction_date | Transaction date |
| store_id | Store identifier |
| product_id | Product identifier |
| customer_id | Customer identifier |
| quantity | Units purchased |
| unit_price | Selling price per unit |
| payment_method | Payment method |

### Product Master

| Column | Description |
|---|---|
| product_id | Product identifier |
| product_name | Product name |
| category | Product category |
| brand | Product brand |
| cost_price | Product cost |

### Store Master

| Column | Description |
|---|---|
| store_id | Store identifier |
| store_name | Store name |
| city | Store city |
| state | Store state |
| region | Store region |


## Important Project Files

### Lambda

```text
lambda/retail_s3_ingestion_trigger.py
```

### Step Functions

```text
step-functions/retail_daily_sales_pipeline.json
```

### Glue

```text
glue/retail_sales_pyspark_etl.py
```

### Athena

```text
athena/
```

### Redshift

```text
redshift/
```

## Configuration and Secrets

AWS credentials, secret keys, database passwords, tokens, and other sensitive information must never be committed to GitHub.

The configuration files in `config/` use placeholders such as:

```text
YOUR_STATE_MACHINE_ARN
YOUR_REDSHIFT_IAM_ROLE_ARN
YOUR_SNS_TOPIC_ARN
```

Use AWS IAM roles, Lambda environment variables, Secrets Manager, or other secure configuration mechanisms for deployment-specific values.

## Deployment / Test Flow

1. Upload a new daily ERP CSV to `raw/sales/`.
2. Verify the S3 ObjectCreated event.
3. Check Lambda CloudWatch logs.
4. Open the Step Functions execution.
5. Verify Glue completes successfully.
6. Verify curated Parquet is created.
7. Verify the curated crawler succeeds.
8. Run Athena validation queries.
9. Run Redshift staging/load/merge SQL.
10. Verify warehouse row counts and data-quality checks.
11. Refresh or query the QuickSight dashboard.

## Monitoring

CloudWatch is used for Lambda and operational logs.

Step Functions provides execution-level workflow status.

Glue provides ETL execution monitoring.

Athena provides query execution history.

Redshift provides warehouse load/query monitoring.

SNS is used for pipeline failure notifications.

## Troubleshooting

### Lambda AccessDenied for Step Functions

Verify that the Lambda execution role has:

```text
states:StartExecution
```

on the correct state-machine ARN.

### Glue Cannot Read S3

Verify the Glue IAM role and S3 permissions, source key, and bucket paths.

### Athena Table Is Empty

Verify the Glue crawler, database, table, S3 curated path, and partitions.

### Redshift COPY Fails

Verify the Redshift IAM role, S3 permissions, S3 prefix, Parquet format, and target table schema.

### Duplicate Rows in Redshift

Verify the daily source partition, staging data, `transaction_id`, and `MERGE` condition.

## Project Status

The AWS ingestion, orchestration, ETL, data-quality, curated-storage, Glue Catalog, and Athena portions are implemented and tested in the project workflow.

The Redshift warehouse layer is maintained in the `redshift/` folder and should be marked complete in project documentation only after the Redshift load, merge, and validation steps have been successfully tested.