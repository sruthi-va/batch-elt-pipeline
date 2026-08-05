from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, when




spark = SparkSession.builder \
    .appName("NYCTaxiBronzeToSilver") \
    .getOrCreate()


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

# from pyspark.sql.functions import col

# invalid_timestamps = df.filter(
#     col("tpep_dropoff_datetime") < col("tpep_pickup_datetime")
# ).count()

# print(f"Trips with dropoff before pickup: {invalid_timestamps}")

#Data Cleaning and Transformation
print("Before cleaning:", df.count())
df = df.dropDuplicates()
df = df.filter(
    col("tpep_dropoff_datetime") >= col("tpep_pickup_datetime")
)

df = df.fillna({
    "congestion_surcharge": 0,
    "Airport_fee": 0
})
print("After cleaning:", df.count())

spark.stop()