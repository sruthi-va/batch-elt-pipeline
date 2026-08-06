import boto3
import logging
import os
from pathlib import Path

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

LOCAL_FILE = "data/raw/yellow_tripdata_2025-07.parquet"
BUCKET_NAME = os.getenv(
    "BUCKET_NAME", 
    "nyc-taxi-bronze-sruthi"
)

S3_KEY = (
    "bronze/yellow/"
    "year=2025/"
    "month=07/"
    "yellow_tripdata_2025-07.parquet"
)

s3 = boto3.client("s3")
def upload_file():
    logging.info("Uploading NYC Taxi data...")

    if not Path(LOCAL_FILE).exists():
        logging.error("File does not exist")
        return

    try:
        s3.upload_file(LOCAL_FILE, BUCKET_NAME, S3_KEY)
        logging.info("Upload complete!")
    except Exception as e:
        logging.error(f"Error occurred while uploading file: {e}")




if __name__ == "__main__":
    print("Starting Bronze upload...")

    upload_file()
    print("Finished Bronze upload successfully.")