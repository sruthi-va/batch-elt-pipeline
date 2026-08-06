from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum

spark = SparkSession.builder.appName("ValidateTransformation").getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

bronze_path = "/app/data/raw/yellow_tripdata_2025-07.parquet"
silver_path = "/app/output/silver/yellow/year=2025/month=07"

bronze_df = spark.read.parquet(bronze_path)

silver_df = spark.read.parquet(silver_path)

bronze_count = bronze_df.count()
silver_count = silver_df.count()

print(f"Bronze row count: {bronze_count}")
print(f"Silver row count: {silver_count}")
print(f"Rows removed: {bronze_count - silver_count}")


def null_counts(df):
    return df.select([sum(col(c).isNull().cast("int")).alias(c) for c in df.columns])


print("Bronze null counts:")
null_counts(bronze_df).show()

print("Silver null counts:")
null_counts(silver_df).show()
