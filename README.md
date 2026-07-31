# Batch ELT Pipeline

## Project Overview

This project builds an end-to-end batch ELT pipeline using NYC TLC Yellow Taxi trip data.

The goal is to simulate a real-world data engineering workflow by ingesting raw data, storing it in a cloud data lake, transforming it into analytics-ready datasets, and visualizing insights.

Current progress:
- Automated data ingestion using Python
- Stored raw data in AWS S3 Bronze layer
- Provisioned AWS infrastructure using Terraform

Planned:
- PySpark transformations
- Snowflake warehouse integration
- Airflow orchestration
- Power BI dashboard


## Architecture

```mermaid
flowchart TD

A[NYC TLC Yellow Taxi Dataset<br/>July 2025] --> B

B[Bronze Layer<br/>Raw Data<br/>AWS S3] --> C

C[Silver Layer<br/>PySpark Cleaning<br/>Processed Parquet] --> D

D[Gold Layer<br/>Analytics Tables] --> E

E[Snowflake Warehouse] --> F

F[Power BI Dashboard]
````

## Technology Stack

| Technology | Purpose                          |
| ---------- | -------------------------------- |
| Python     | Data ingestion                   |
| AWS S3     | Raw data storage                 |
| Terraform  | Infrastructure as Code           |
| boto3      | Upload data to S3                |
| PySpark    | Data transformation (planned)    |
| Snowflake  | Data warehouse (planned)         |
| Airflow    | Pipeline orchestration (planned) |
| Power BI   | Visualization (planned)          |

## Project Structure

```
batch-elt-pipeline/

├── ingestion/
│   ├── download_taxi_data.py
│   └── upload_to_s3.py
├── terraform/
├── data/
├── notebooks/
├── docs/
├── requirements.txt
└── README.md
```

# Running the Ingestion Pipeline

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Download Dataset

```bash
python ingestion/download_taxi_data.py
```

Saves data locally:

```
data/raw/yellow_tripdata_2025-07.parquet
```

## Upload to S3

```bash
python ingestion/upload_to_s3.py
```

Stored in:

```
bronze/
└── yellow/
    └── year=2025/
        └── month=07/
            └── yellow_tripdata_2025-07.parquet
```

# AWS Setup

Configure AWS credentials:

```bash
aws configure
```

The ingestion script uses boto3 to authenticate and upload data to S3.

# Terraform Setup

Navigate to the Terraform folder:

```bash
cd terraform
```

Initialize:

```bash
terraform init
```

Preview changes:

```bash
terraform plan
```

Create resources:

```bash
terraform apply
```

# Data Layers

## Bronze

Raw immutable data stored in S3.

## Silver

Cleaned and transformed data using PySpark.

## Gold

Analytics-ready tables used for reporting and dashboards.
