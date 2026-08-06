import snowflake.connector
from dotenv import load_dotenv
import os
import glob

load_dotenv()


print("Connecting to Snowflake...")

conn = snowflake.connector.connect(
    user=os.environ["SNOWFLAKE_USER"],
    password=os.environ["SNOWFLAKE_PASSWORD"],
    account=os.environ["SNOWFLAKE_ACCOUNT"],
    warehouse="COMPUTE_WH",
    database="TAXI_ANALYTICS",
    schema="GOLD",
)

cursor = conn.cursor()

print("Connected to Snowflake")


# Create Stage

print("Creating Snowflake stage...")

cursor.execute("""
CREATE STAGE IF NOT EXISTS GOLD_STAGE;
""")

print("Stage ready")


# Upload Gold Parquet Files

print("Uploading Gold parquet files...")


gold_tables = ["daily_trip_summary", "hourly_demand", "location_metrics"]


for table in gold_tables:

    path = f"/opt/project/data/gold/{table}"

    print(f"\nUploading {table}...")

    parquet_files = glob.glob(f"{path}/**/*.parquet", recursive=True)

    if not parquet_files:
        raise Exception(f"No parquet files found for {table}")

    for file in parquet_files:

        print(f"Uploading file: {file}")

        cursor.execute(f"""
        PUT file://{file}
        @GOLD_STAGE
        AUTO_COMPRESS=TRUE;
        """)


print("\nAll Gold parquet files uploaded")


# Run Snowflake Load SQL

print("Running Snowflake load SQL...")

with open("/opt/project/snowflake/load_gold.sql") as file:

    sql_commands = file.read().split(";")

    for command in sql_commands:

        if command.strip():
            cursor.execute(command)


print("Gold data loaded successfully!")


cursor.close()
conn.close()

print("Snowflake connection closed")
