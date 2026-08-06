import snowflake.connector
import os


conn = snowflake.connector.connect(
    user=os.environ["SNOWFLAKE_USER"],
    password=os.environ["SNOWFLAKE_PASSWORD"],
    account=os.environ["SNOWFLAKE_ACCOUNT"],
    warehouse="COMPUTE_WH",
    database="TAXI_ANALYTICS",
    schema="GOLD"
)


cursor = conn.cursor()


# Upload parquet files
cursor.execute("""
PUT file:///opt/project/data/gold/daily_trip_summary/*.parquet
@gold_stage
AUTO_COMPRESS=TRUE;
""")


# Run SQL load commands
with open("/opt/project/snowflake/load_gold.sql") as file:
    sql_commands = file.read().split(";")

    for command in sql_commands:
        if command.strip():
            cursor.execute(command)


cursor.close()
conn.close()