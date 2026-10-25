from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import boto3
import json

def get_secret():
    secret_name = "redshift-admin-password"
    region_name = "ap-southeast-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except Exception as e:
        raise e
    else:
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            return json.loads(secret)['password']

def main():
    # Get Redshift password from Secrets Manager
    redshift_password = get_secret()

    spark = SparkSession.builder \
        .appName("S3 to Redshift ETL") \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.2.0,com.amazonaws:aws-java-sdk:1.11.563,com.amazon.redshift:redshift-jdbc42:2.1.0.1") \
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
        .getOrCreate()

    # Set up S3 credentials
    spark.sparkContext._jsc.hadoopConfiguration().set("com.amazonaws.services.s3.enableV4", "true")
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.access.key", "S3 ACCESS KEY")
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.secret.key", "S3 SECRET KEY")

    # Extract: Read CSV from S3
    df = spark.read.csv("s3://etlkube/corporate_rating.csv", header=True, inferSchema=True)

    # Transform: Clean column names and select required columns
    columns = [
        "Rating", "Name", "Symbol", "RatingAgencyName", "Date", "Sector",
        "currentRatio", "quickRatio", "cashRatio", "daysOfSalesOutstanding",
        "netProfitMargin", "pretaxProfitMargin", "grossProfitMargin", "operatingProfitMargin",
        "returnOnAssets", "returnOnCapitalEmployed", "returnOnEquity", "assetTurnover",
        "fixedAssetTurnover", "debtEquityRatio", "debtRatio", "effectiveTaxRate",
        "freeCashFlowOperatingCashFlowRatio", "freeCashFlowPerShare", "cashPerShare",
        "companyEquityMultiplier", "ebitPerRevenue", "enterpriseValueMultiple",
        "operatingCashFlowPerShare", "operatingCashFlowSalesRatio", "payablesTurnover"
    ]

    # Convert to Parquet and save to S3
    transformed_df.write.parquet("s3a://etlkube/output/transformed_data.parquet")

    transformed_df = df.select([col(c).alias(c.lower()) for c in columns])

    # Load: Write to Redshift
    transformed_df.write \
        .format("jdbc") \
        .option("url", "jdbc:redshift://redshift-etlkube.cmlzubnbirp1.ap-southeast-1.redshift.amazonaws.com:5439/dev") \
        .option("dbtable", "corporate_rating") \
        .option("user", "redshift-admin") \
        .option("password", redshift_password) \
        .option("driver", "com.amazon.redshift.jdbc42.Driver") \
        .option("ssl", "true") \
        .option("sslmode", "verify-full") \
        .mode("overwrite") \
        .save()

    spark.stop()

if __name__ == "__main__":
    main()
