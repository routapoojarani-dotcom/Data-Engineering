# Cloud ETL Pipeline with Airflow, Spark & Amazon Redshift

## Overview
This project implements an automated ETL (Extract, Transform, Load) pipeline using Apache Airflow running on Kubernetes. The pipeline moves data from Amazon S3 to Amazon Redshift.

An AWS S3 bucket is used as a Data Lake in which json files are stored. The data is extracted from a json and parsed (cleaned). It is then transformed/processed with SparkSQL (PySpark) and loaded/stored in an Amazon Redshift Data Warehouse.

## Flow Diagram

A[S3 Bucket] --> B[Kubernetes Pod] --> C[Amazon Redshift]

![etl](https://github.com/user-attachments/assets/1c8eea1e-1c6a-4946-80de-773b0da41b75)

## Credit risk assessment

Current Ratio:
- Strong (>2.0): Texas Instruments (2.91), BioMarin (6.04)
- Adequate (1.5-2.0): Honeywell (1.50), Schlumberger (1.90)
- Weak (<1.0): Enbridge (0.63), Fortis (0.54)

Quick Ratio:
- Strong (>1.5): Applied Materials (6.96)
- Adequate (1.0-1.5): Schlumberger (1.54)
- Weak (<1.0): Murphy Oil (0.89)

🌟 Profitability Indicators

Return on Assets (ROA):
- Strong (>15%): Texas Instruments (15.9%)
- Average (5-15%): Honeywell (8.6%)
- Weak (<5%): YRC Worldwide (-33%)

Operating Margins:
- High Tech: 20-30%
- Industrial: 10-20%
- Energy: 5-15%

🌟 Risk Factors Correlation

1. Debt Metrics:
 - Debt/Equity > 3.0
 - Interest coverage < 2.0
 - High leverage in cyclical industries

2. Operational Concerns:
 - Operating margin < 5%
 - Negative cash flow from operations
 - High working capital requirements

3. Industry-Specific Risks:
 - Energy: Oil price sensitivity
 - Technology: R&D investment needs
 - Finance: Market volatility exposure

## Project Flow
1. **Data Source**: Raw data stored in Amazon S3
2. **Processing**: Kubernetes pods spin up to execute ETL tasks
3. **Destination**: Processed data loaded into Amazon Redshift