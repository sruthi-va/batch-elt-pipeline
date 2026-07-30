## Architecture

```mermaid
flowchart TD

A[NYC TLC Yellow Taxi Dataset<br/>July 2025] --> B

B[Bronze Layer<br/>Raw Data<br/>S3 / Data Lake] --> C

C[Silver Layer<br/>PySpark Transformations<br/>Cleaned Parquet Files] --> D

D[Gold Layer<br/>Analytics Tables<br/>Aggregations] --> E

E[Snowflake Data Warehouse] --> F

F[Power BI Dashboard]
```