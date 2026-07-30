# NYC Taxi Data Exploration

## Dataset

**Source:** NYC TLC Yellow Taxi Trip Records  
**Dataset:** July 2025 Yellow Taxi Data  
**Format:** Parquet

## Columns

The dataset contains 20 columns:

- `VendorID`
- `tpep_pickup_datetime`
- `tpep_dropoff_datetime`
- `passenger_count`
- `trip_distance`
- `RatecodeID`
- `store_and_fwd_flag`
- `PULocationID`
- `DOLocationID`
- `payment_type`
- `fare_amount`
- `extra`
- `mta_tax`
- `tip_amount`
- `tolls_amount`
- `improvement_surcharge`
- `total_amount`
- `congestion_surcharge`
- `Airport_fee`
- `cbd_congestion_fee`

## Initial Observations

### Time Information

- `tpep_pickup_datetime` and `tpep_dropoff_datetime` can be used to calculate trip duration.
- A new feature such as `trip_duration_minutes` could be created during the silver transformation layer.

### Financial Information

The following columns contain financial information:

- `fare_amount`
- `extra`
- `mta_tax`
- `tip_amount`
- `tolls_amount`
- `improvement_surcharge`
- `total_amount`
- `congestion_surcharge`
- `Airport_fee`
- `cbd_congestion_fee`

These columns can be used later to create gold-layer analytics such as:
- total revenue
- average fare
- average tip percentage
- revenue trends over time

## Data Quality Observations

### Missing Values

The following columns contain a large number of missing values (~1,038,755 rows):

- `passenger_count`
- `RatecodeID`
- `store_and_fwd_flag`
- `congestion_surcharge`
- `Airport_fee`

These columns will need to be handled during the cleaning/transformation stage.

### Potential Data Issues

From the summary statistics:

- Although this dataset is labeled as July 2025 data, there are records with pickup/dropoff timestamps from **January 1, 2009**. These records may need to be investigated or removed during cleaning.
- Several numerical columns contain unexpected minimum values:
  - `passenger_count` has a minimum value of 0.
  - `trip_distance` has a minimum value of 0.
  - Financial columns contain negative minimum values:
    - `fare_amount`
    - `extra`
    - `mta_tax`
    - `tip_amount`
    - `tolls_amount`
    - `improvement_surcharge`
    - `total_amount`
    - `congestion_surcharge`
    - `Airport_fee`
    - `cbd_congestion_fee`

These values should be investigated to determine whether they represent valid cases (such as refunds or adjustments) or invalid records.