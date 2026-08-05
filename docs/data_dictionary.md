# NYC Yellow Taxi Data Dictionary

## Dataset Information

**Dataset:** NYC TLC Yellow Taxi Trip Records  
**Date:** July 2025  
**Source:** NYC Taxi & Limousine Commission (TLC)

This document describes the schema and purpose of each column in the dataset.

---

## Schema

| Column | Description | Data Type |
|---|---|---|
| VendorID | Identifier for the taxi provider/vendor | Integer |
| tpep_pickup_datetime | Date and time when the passenger was picked up | Timestamp |
| tpep_dropoff_datetime | Date and time when the passenger was dropped off | Timestamp |
| passenger_count | Number of passengers in the taxi | Integer |
| trip_distance | Total distance traveled during the trip in miles | Float |
| RatecodeID | Final rate code assigned to the trip | Integer |
| store_and_fwd_flag | Indicates whether the trip record was stored locally before being sent to the vendor | String |
| PULocationID | TLC Taxi Zone ID where the trip started | Integer |
| DOLocationID | TLC Taxi Zone ID where the trip ended | Integer |
| payment_type | Numeric identifier for payment method | Integer |
| fare_amount | Base fare charged for the trip | Float |
| extra | Additional charges such as rush hour or overnight fees | Float |
| mta_tax | MTA tax applied to the trip | Float |
| tip_amount | Tip amount paid by the passenger | Float |
| tolls_amount | Total toll charges paid during the trip | Float |
| improvement_surcharge | Improvement surcharge applied to the trip | Float |
| total_amount | Total amount charged including fares, fees, and tips | Float |
| congestion_surcharge | Congestion pricing surcharge | Float |
| Airport_fee | Additional fee for airport trips | Float |
| cbd_congestion_fee | Central Business District congestion fee | Float |

---

## Derived Features (Future Silver Layer)

Potential features that can be created during transformation:

| Feature | Description |
|---|---|
| trip_duration_minutes | Difference between dropoff and pickup timestamps |
| average_speed | Trip distance divided by trip duration |
| tip_percentage | Tip amount as a percentage of fare |
| pickup_hour | Hour extracted from pickup timestamp |
| pickup_day_of_week | Day of week extracted from pickup timestamp |

# Gold Layer

## gold_daily_trip_summary

**Purpose**

Provides daily aggregated metrics for taxi demand, trip characteristics, and revenue. This table supports trend analysis and executive reporting.

**Grain**

One row per pickup date.

---

## gold_hourly_demand

**Purpose**

Aggregates taxi demand by pickup hour to identify peak travel periods and hourly revenue patterns.

**Grain**

One row per pickup date and pickup hour.

---

## gold_location_metrics

**Purpose**

Summarizes trip activity and financial performance by pickup location to support geographic analysis.

**Grain**

One row per pickup location.

# Snowflake Warehouse Design

Database:
TAXI_ANALYTICS

Schemas:

## GOLD

Contains analytics-ready aggregated tables used by BI tools.

Tables:

### DAILY_TRIP_SUMMARY

Purpose:
Tracks daily taxi activity and revenue trends.

Primary use cases:
- Daily demand analysis
- Revenue trends
- Trip performance monitoring


### HOURLY_DEMAND

Purpose:
Analyzes taxi demand by pickup hour and weekday/weekend patterns.


### LOCATION_METRICS

Purpose:
Measures taxi zone performance including revenue and trip volume.