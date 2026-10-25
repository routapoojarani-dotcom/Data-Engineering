from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import (
    IntegerType,
    LongType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)

SOURCE_SCHEMA = StructType([
    StructField("trans_id", LongType(), False),
    StructField("atm_id", IntegerType(), True),
    StructField("atm_number", StringType(), True),
    StructField("atm_manufacturer", StringType(), True),
    StructField("atm_location_id", IntegerType(), True),
    StructField("location", StringType(), True),
    StructField("streetname", StringType(), True),
    StructField("street_number", IntegerType(), True),
    StructField("zipcode", IntegerType(), True),
    StructField("lat", StringType(), True),
    StructField("lon", StringType(), True),
    StructField("full_date_time", TimestampType(), True),
    StructField("card_type_id", IntegerType(), True),
    StructField("card_type", StringType(), True),
    StructField("atm_status", StringType(), True),
    StructField("currency", StringType(), True),
    StructField("service", StringType(), True),
    StructField("transaction_amount", IntegerType(), True),
    StructField("message_code", StringType(), True),
    StructField("message_text", StringType(), True),
    StructField("rain_3h", StringType(), True),
    StructField("clouds_all", IntegerType(), True),
    StructField("weather_id", IntegerType(), True),
    StructField("weather_main", StringType(), True),
    StructField("weather_description", StringType(), True),
])


def build_dimensions(df: DataFrame) -> dict[str, DataFrame]:
    """Build the four dimension datasets used by the warehouse model."""
    dim_location = (
        df.select(
            F.col("atm_location_id").alias("location_id"),
            "location",
            "streetname",
            "street_number",
            "zipcode",
            "lat",
            "lon",
        )
        .dropDuplicates(["location_id"])
    )

    dim_atm = (
        df.select(
            "atm_id",
            "atm_number",
            "atm_manufacturer",
            "atm_location_id",
        )
        .dropDuplicates(["atm_id"])
    )

    dim_date = (
        df.select(
            F.date_format("full_date_time", "yyyyMMdd").cast("int").alias("date_id"),
            "full_date_time",
            F.year("full_date_time").alias("year"),
            F.date_format("full_date_time", "MMMM").alias("month"),
            F.dayofmonth("full_date_time").alias("day"),
            F.hour("full_date_time").alias("hour"),
            F.date_format("full_date_time", "EEEE").alias("weekday"),
        )
        .dropDuplicates(["date_id"])
    )

    dim_card_type = (
        df.select("card_type_id", "card_type")
        .dropDuplicates(["card_type_id"])
    )

    return {
        "dim_location": dim_location,
        "dim_atm": dim_atm,
        "dim_date": dim_date,
        "dim_card_type": dim_card_type,
    }


def build_fact(df: DataFrame) -> DataFrame:
    """Build the transaction fact dataset used by the Redshift model."""
    return (
        df.select(
            "trans_id",
            "atm_id",
            F.col("atm_location_id").alias("weather_loc_id"),
            F.date_format("full_date_time", "yyyyMMdd").cast("int").alias("date_id"),
            "card_type_id",
            "atm_status",
            "currency",
            "service",
            "transaction_amount",
            "message_code",
            "message_text",
            "rain_3h",
            "clouds_all",
            "weather_id",
            "weather_main",
            "weather_description",
        )
        .dropDuplicates(["trans_id"])
    )


def run(input_path: str, output_path: str) -> None:
    """Run the reference ETL from CSV input to curated CSV outputs."""
    spark = SparkSession.builder.appName("ATMDataEngineering").getOrCreate()

    source = (
        spark.read
        .option("header", True)
        .schema(SOURCE_SCHEMA)
        .csv(input_path)
    )

    dimensions = build_dimensions(source)
    fact = build_fact(source)

    for name, frame in dimensions.items():
        frame.write.mode("overwrite").option("header", True).csv(
            f"{output_path}/{name}"
        )

    fact.write.mode("overwrite").option("header", True).csv(
        f"{output_path}/fact_atm_trans"
    )

    spark.stop()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    run(args.input, args.output)
