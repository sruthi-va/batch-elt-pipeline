from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, sum, count, round, date_format

# initialize spark
spark = SparkSession.builder.appName("SilverToGold").getOrCreate()
print("Starting Silver to Gold transformation...")
spark.sparkContext.setLogLevel("ERROR")


# =========================
# Read Silver Layer
# =========================

silver_df = spark.read.parquet("data/silver/yellow/year=2025/month=07")

print("Silver schema:")
silver_df.printSchema()


# =========================
# GOLD TABLE 1
# Daily Trip Summary
# =========================

daily_trip_summary = (
    silver_df.withColumn("date", date_format(col("pickup_datetime"), "yyyy-MM-dd"))
    .groupBy("date")
    .agg(
        count("*").alias("total_trips"),
        round(avg("trip_distance"), 2).alias("avg_trip_distance"),
        round(avg("trip_duration_minutes"), 2).alias("avg_trip_duration_minutes"),
        round(avg("fare_amount"), 2).alias("avg_fare_amount"),
        round(avg("tip_amount"), 2).alias("avg_tip_amount"),
        round(sum("total_amount"), 2).alias("total_revenue"),
        round(avg("average_speed_mph"), 2).alias("avg_speed_mph"),
    )
    .withColumn("year", date_format(col("date"), "yyyy"))
    .withColumn("month", date_format(col("date"), "MM"))
)


print("Daily Summary")
daily_trip_summary.show(5)


# =========================
# GOLD TABLE 2
# Hourly Demand Analysis
# =========================

hourly_demand = silver_df.groupBy("pickup_hour", "is_weekend").agg(
    count("*").alias("total_trips"),
    round(avg("fare_amount"), 2).alias("avg_fare"),
    round(avg("trip_distance"), 2).alias("avg_distance"),
    round(avg("trip_duration_minutes"), 2).alias("avg_duration"),
)


print("Hourly Demand")
hourly_demand.show(5)


# =========================
# GOLD TABLE 3
# Location Performance
# =========================

location_metrics = silver_df.groupBy("pickup_location_id").agg(
    count("*").alias("total_trips"),
    round(sum("total_amount"), 2).alias("total_revenue"),
    round(avg("fare_amount"), 2).alias("avg_fare"),
    round(avg("tip_amount"), 2).alias("avg_tip_amount"),
    round(avg("trip_distance"), 2).alias("avg_trip_distance"),
)


print("Location Metrics")
location_metrics.show(5)


# =========================
# Write Gold Tables
# =========================

# Daily summary
daily_trip_summary.write.mode("overwrite").partitionBy("year", "month").parquet(
    "data/gold/daily_trip_summary"
)


hourly_demand.write.mode("overwrite").parquet("data/gold/hourly_demand")


location_metrics.write.mode("overwrite").parquet("data/gold/location_metrics")


print("Gold tables created successfully!")

print("Finished Gold table creation.")
spark.stop()
