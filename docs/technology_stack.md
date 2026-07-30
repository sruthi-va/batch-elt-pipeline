# Technology Stack

This document provides an overview of the technologies used in the NYC Taxi Batch ELT Pipeline and their role within the architecture.

## Python

Python is used as the primary programming language for data ingestion, pipeline logic, and automation. It is used to extract data from external sources, interact with cloud services, and support transformation workflows.

## Git & GitHub

Git is used for version control and tracking changes throughout development. GitHub hosts the repository and stores pipeline code, documentation, infrastructure configuration, and project history.

## Docker

Docker is used to create consistent development environments by packaging applications and dependencies into containers. In this project, Docker will be used to run services such as Airflow locally.

## Parquet

Parquet is a column-based file format optimized for analytical workloads. It provides efficient storage and faster querying compared to formats such as CSV. Parquet files are used for storing raw and transformed datasets.

## S3 / Cloud Storage

Cloud object storage is used as the data lake layer for storing datasets throughout the pipeline. Raw data will be stored in the bronze layer, while cleaned and transformed data will be stored in later layers.

## Apache Spark / PySpark

PySpark is used for large-scale data transformation and processing. It will be used to clean raw taxi data, handle missing values, remove invalid records, create derived features, and prepare datasets for analytics.

## Airflow

Apache Airflow is used for workflow orchestration. It manages the order and scheduling of pipeline tasks, including data ingestion, transformations, quality checks, and loading data into the warehouse.

## Terraform

Terraform is used for Infrastructure as Code (IaC). It allows cloud resources such as storage buckets and warehouse resources to be created and managed through configuration files instead of manual setup.

## Snowflake

Snowflake is used as the cloud data warehouse for storing curated datasets. Gold-layer tables will be loaded into Snowflake to support analytics and business reporting.

## Power BI / Tableau

A BI visualization tool is used to create dashboards and communicate insights from the final gold-layer datasets.

---

## Pipeline Architecture Summary

The overall workflow is:

1. **Ingestion:** Python extracts NYC Taxi data and stores raw files.
2. **Bronze Layer:** Raw data is stored in cloud storage.
3. **Silver Layer:** PySpark cleans and transforms the data.
4. **Gold Layer:** Business-ready tables are created for analytics.
5. **Warehouse:** Curated data is loaded into Snowflake.
6. **Visualization:** BI dashboards display insights from the processed data.

Supporting technologies:

* GitHub manages code and documentation.
* Docker manages local environments.
* Airflow orchestrates workflows.
* Terraform provisions infrastructure.
