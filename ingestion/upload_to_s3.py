import boto3

LOCAL_FILE = "data/raw/yellow_tripdata_2025-07.parquet"
BUCKET_NAME = "nyc-taxi-bronze-sruthi"
S3_KEY = (
    "bronze/yellow/"
    "year=2025/"
    "month=07/"
    "yellow_tripdata_2025-07.parquet"
)

s3 = boto3.client("s3")

def upload_file():
    print("Uploading NYC Taxi data...")

    s3.upload_file(LOCAL_FILE, BUCKET_NAME, S3_KEY)

    print("Upload complete!")

if __name__ == "__main__":
    upload_file()