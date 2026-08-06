from pyspark.sql import SparkSession
from pyspark.sql.functions import col


def get_spark():
    return SparkSession.builder \
        .master("local[*]") \
        .appName("test") \
        .getOrCreate()


def test_duplicate_removal():

    spark = get_spark()

    data = [
        (1, "2025-07-01 10:00:00", "2025-07-01 10:30:00"),
        (1, "2025-07-01 10:00:00", "2025-07-01 10:30:00"),
        (2, "2025-07-01 11:00:00", "2025-07-01 11:20:00")
    ]

    columns = [
        "trip_id",
        "pickup_time",
        "dropoff_time"
    ]

    df = spark.createDataFrame(data, columns)

    cleaned = df.dropDuplicates()

    assert cleaned.count() == 2

def test_invalid_timestamp_removal():

    spark = get_spark()

    data = [
        (1, "2025-07-01 10:00:00", "2025-07-01 10:30:00"),
        (2, "2025-07-01 12:00:00", "2025-07-01 11:30:00")
    ]

    columns = [
        "trip_id",
        "pickup_time",
        "dropoff_time"
    ]

    df = spark.createDataFrame(data, columns)

    valid = df.filter(
        col("dropoff_time") > col("pickup_time")
    )

    assert valid.count() == 1

def test_derived_columns_created():

    spark = get_spark()

    data = [
        (2.0, 30)
    ]

    columns = [
        "trip_distance",
        "trip_duration_minutes"
    ]

    df = spark.createDataFrame(data, columns)

    result = df.withColumn(
        "average_speed_mph",
        col("trip_distance") /
        (col("trip_duration_minutes") / 60)
    )

    assert "average_speed_mph" in result.columns