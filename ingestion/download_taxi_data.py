import logging
import requests
from pathlib import Path
import os

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

DATA_URL = os.getenv(
    "DATA_URL",
    "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-07.parquet",
)

OUTPUT_PATH = Path("data/raw/yellow_tripdata_2025-07.parquet")


def download_data():
    logging.info("Starting download...")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    try:
        response = requests.get(DATA_URL, stream=True)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Error occurred while downloading data: {e}")
        return

    logging.info("Downloading NYC Taxi July 2025 data...")

    with open(OUTPUT_PATH, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    logging.info(f"Download complete! Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    download_data()
