# Spotify Data Lake and Serverless Analytics Pipeline on AWS

This project demonstrates an end-to-end data engineering pipeline on AWS. It shows how to build a scalable, cloud-based data lake architecture to ingest, transform, catalog, query, and visualize data in a cost-effective and efficient way.

## 🚀 Features

- **Amazon S3**: Stores raw and transformed data in separate logical folders (staging and data warehouse)
- **AWS Glue**: Serverless ETL jobs to transform CSV data to optimized Parquet format
- **AWS Glue Crawler**: Catalogs data for Athena by creating schema metadata
- **Amazon Athena**: Enables serverless, SQL-based analytics directly on data stored in S3
- **Amazon QuickSight**: Visualizes the final data with interactive dashboards
- **IAM Roles**: Follows least-privilege access patterns to securely connect services

## 📂 Dataset

The raw CSV dataset used for this pipeline consists of three files:

- `albums.csv`
- `artists.csv`
- `tracks.csv`

## 🛠️ How It Works
![Architecture Diagram](images/Aws-data-pipeline-architecture.png)

1. **Upload raw CSV data** (albums, artists, tracks) to the `staging` folder in your S3 bucket  
2. **AWS Glue ETL job**:
   - Joins data across CSVs
   - Cleans and transforms columns
   - Converts to Parquet with Snappy compression
   - Writes output to the `datawarehouse` folder in S3  
   ![Glue ETL Workflow](images/Glue_ETL_workflow.PNG)  
   ![Data Warehouse Parquet Files](images/DatawareHouse(parquet).PNG)
3. **AWS Glue Crawler**:
   - Crawls the `datawarehouse` folder
   - Registers the schema in Glue Data Catalog (as `spotify_db`)  
   ![Glue Data Catalog](images/Glue_DataCatlog.PNG)
4. **Amazon Athena**:
   - Uses the Data Catalog to query data with serverless SQL
   - Saves query results to a separate S3 bucket (`athena-query-results`)  
   ![Athena Query Output](images/Athena_query_output.jpg)
5. **Amazon QuickSight**:
   - Connects to Athena to build interactive dashboards
6. **IAM Roles**:
   - Provide least-privilege permissions between Glue, Athena, S3, and QuickSight  
   ![IAM Roles](images/IAM_roles.PNG)


## 🔍 Sample Athena Queries

You can find sample SQL queries in [`queries/sample_queries.sql`](queries/sample_queries.sql). For example:

```sql
SELECT track_name, track_popularity
FROM spotify_db.datawarehouse
ORDER BY track_popularity DESC
LIMIT 5;
```