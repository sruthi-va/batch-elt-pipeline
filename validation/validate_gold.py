from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import sys


spark = (
    SparkSession.builder
    .appName("GoldDataQualityChecks")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

print("Starting Gold data quality checks...")

daily_df = spark.read.parquet(
    "data/gold/daily_trip_summary"
)

hourly_df = spark.read.parquet(
    "data/gold/hourly_demand"
)

location_df = spark.read.parquet(
    "data/gold/location_metrics"
)

def check_daily_row_count(df):

    total_rows = df.count()

    unique_dates = (
        df.select("date")
        .distinct()
        .count()
    )

    if total_rows != unique_dates:
        raise Exception(
            f"Daily table failed row count check. "
            f"Rows={total_rows}, Unique dates={unique_dates}"
        )

    print("Daily row count check passed")

def check_revenue(df):

    invalid_rows = (
        df.filter(
            col("total_revenue") < 0
        )
        .count()
    )


    if invalid_rows > 0:
        raise Exception(
            f"Found {invalid_rows} rows with negative revenue"
        )

    print(" Revenue validation passed")

def check_duration(df):

    invalid_rows = (
        df.filter(
            col("avg_trip_duration_minutes") <= 0
        )
        .count()
    )


    if invalid_rows > 0:
        raise Exception(
            f"Found {invalid_rows} invalid duration values"
        )

    print("Duration validation passed")

def check_distance(df):

    invalid_rows = (
        df.filter(
            col("avg_trip_distance") < 0
        )
        .count()
    )


    if invalid_rows > 0:
        raise Exception(
            f"Found {invalid_rows} invalid distance values"
        )

    print("Distance validation passed")

expected_daily_columns = {
    "date",
    "total_trips",
    "avg_trip_distance",
    "avg_trip_duration_minutes",
    "avg_fare_amount",
    "avg_tip_amount",
    "total_revenue",
    "avg_speed_mph"
}

def check_schema(df, expected_columns, table_name):

    actual_columns = set(df.columns)

    missing = expected_columns - actual_columns
    extra = actual_columns - expected_columns


    if missing:
        raise Exception(
            f"{table_name} missing columns: {missing}"
        )

    if extra:
        raise Exception(
            f"{table_name} has unexpected columns: {extra}"
        )


    print(f"{table_name} schema check passed")

check_daily_row_count(daily_df)

check_revenue(daily_df)

check_duration(daily_df)

check_distance(daily_df)


check_schema(
    daily_df,
    expected_daily_columns,
    "daily_trip_summary"
)


print("All Gold validation checks passed!")

spark.stop()