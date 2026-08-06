from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, when, hour
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import unix_timestamp, dayofweek

print("Starting Bronze to Silver transformation...")
spark = (
    SparkSession.builder
    .appName("BronzeToSilver")
    .config("spark.hadoop.hadoop.home.dir", "C:/hadoop")
    .getOrCreate()
)


spark.sparkContext.setLogLevel("ERROR")


file_path = "data/raw/yellow_tripdata_2025-07.parquet"


df = spark.read.parquet(file_path)


# Profiling code:
#null_counts = df.select([
#    count(when(col(c).isNull(), c)).alias(c)
#    for c in df.columns
#])

#null_counts.show(vertical=True, truncate=False)


#null_counts.show()

#df.groupBy("passenger_count") \
#    .count() \
#    .orderBy("passenger_count") \
#    .show()

# numeric_columns = ["trip_distance", "fare_amount", "tip_amount", "total_amount"]

# for column in numeric_columns:
#     negative_count = df.filter(col(column) < 0).count()

#     print(f"Negative values in '{column}': {negative_count}")

# print("Negative fare examples:")
# df.filter(col("fare_amount") < 0) \
#   .select(
#       "fare_amount",
#       "total_amount",
#       "tip_amount",
#       "payment_type"
#   ) \
#   .show(10, truncate=False)

# total_rows = df.count()
# distinct_rows = df.dropDuplicates().count()

# print(f"Total rows: {total_rows}")
# print(f"Distinct rows: {distinct_rows}")
# print(f"Duplicate rows: {total_rows - distinct_rows}")


# invalid_timestamps = df.filter(
#     col("tpep_dropoff_datetime") < col("tpep_pickup_datetime")
# ).count()

# print(f"Trips with dropoff before pickup: {invalid_timestamps}")

#Data Cleaning and Transformation
#print("Before cleaning:", df.count())
df = df.dropDuplicates()
df = df.filter(
    col("tpep_dropoff_datetime") >= col("tpep_pickup_datetime")
)

df = df.fillna({
    "congestion_surcharge": 0,
    "Airport_fee": 0
})
#print("After cleaning:", df.count())


null_check = df.select(
    count(when(col("congestion_surcharge").isNull(), True)).alias("congestion_nulls"),
    count(when(col("Airport_fee").isNull(), True)).alias("airport_fee_nulls")
)

#null_check.show()

df = (
    df
    .withColumnRenamed("VendorID", "vendor_id")
    .withColumnRenamed("tpep_pickup_datetime", "pickup_datetime")
    .withColumnRenamed("tpep_dropoff_datetime", "dropoff_datetime")
    .withColumnRenamed("RatecodeID", "rate_code_id")
    .withColumnRenamed("PULocationID", "pickup_location_id")
    .withColumnRenamed("DOLocationID", "dropoff_location_id")
    .withColumnRenamed("Airport_fee", "airport_fee")
)

#df.groupBy("store_and_fwd_flag").count().show()

df = (
    df
    .withColumn(
        "passenger_count",
        col("passenger_count").cast(IntegerType())
    )
    .withColumn(
        "rate_code_id",
        col("rate_code_id").cast(IntegerType())
    )
    .withColumn(
        "payment_type",
        col("payment_type").cast(IntegerType())
    )
)

#df.printSchema()


#Derived Columns
df = df.withColumn(
    "trip_duration_minutes",
    (
        unix_timestamp(col("dropoff_datetime")) -
        unix_timestamp(col("pickup_datetime"))
    ) / 60
)

df = df.withColumn(
    "average_speed_mph",
    when(
        col("trip_duration_minutes") > 0,
        col("trip_distance") / (col("trip_duration_minutes") / 60)
    )
)

df = df.withColumn(
    "pickup_hour",
    hour(col("pickup_datetime"))
)

df = df.withColumn(
    "pickup_day_of_week",
    dayofweek(col("pickup_datetime"))
)

df = df.withColumn(
    "is_weekend",
    when(
        col("pickup_day_of_week").isin(1,7),
        True
    ).otherwise(False)
)

df = df.withColumn(
    "trip_distance_category",
    when(col("trip_distance") < 5, "short")
    .when(col("trip_distance") < 15, "medium")
    .otherwise("long")
)

# df.select(
#     "pickup_datetime",
#     "dropoff_datetime",
#     "trip_duration_minutes",
#     "trip_distance",
#     "average_speed_mph",
#     "pickup_hour",
#     "pickup_day_of_week",
#     "is_weekend",
#     "trip_distance_category"
# ).show(10)

print("Writing Silver parquet files...")
silver_path = "/app/output/silver/yellow/year=2025/month=07"
df.write.mode("overwrite").parquet(silver_path)

silver_df = spark.read.parquet(silver_path)

print("Silver row count:", silver_df.count())

silver_df.printSchema()

silver_df.show(5)
print("Finished Silver transformation.")
spark.stop()
