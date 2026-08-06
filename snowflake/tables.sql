CREATE TABLE IF NOT EXISTS GOLD.DAILY_TRIP_SUMMARY (
    trip_date DATE,
    total_trips INTEGER,
    avg_trip_distance FLOAT,
    avg_trip_duration_minutes FLOAT,
    avg_fare_amount FLOAT,
    avg_tip_amount FLOAT,
    total_revenue FLOAT,
    avg_speed_mph FLOAT
);