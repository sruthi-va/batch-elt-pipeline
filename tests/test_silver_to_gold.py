from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, avg


def get_spark():

    return SparkSession.builder \
        .master("local[*]") \
        .appName("gold_test") \
        .getOrCreate()


def test_daily_revenue_calculation():

    spark = get_spark()

    data = [
        ("2025-07-01", 10.0),
        ("2025-07-01", 20.0),
        ("2025-07-02", 15.0)
    ]

    columns = [
        "date",
        "fare_amount"
    ]

    df = spark.createDataFrame(data, columns)


    gold = df.groupBy("date") \
        .agg(
            sum("fare_amount")
            .alias("total_revenue")
        )


    result = gold \
        .filter("date='2025-07-01'") \
        .collect()[0]


    assert result["total_revenue"] == 30

