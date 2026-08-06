from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="taxi_pipeline",
    start_date=datetime(2026, 8, 1),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
) as dag:
    download_data = BashOperator(
        task_id="download_data",
        bash_command="python /opt/project/ingestion/download_taxi_data.py",
    )

    upload_to_bronze = BashOperator(
        task_id="upload_to_bronze",
        bash_command="python /opt/project/ingestion/upload_to_s3.py",
    )

    bronze_to_silver = BashOperator(
        task_id="bronze_to_silver",
        bash_command="""
        docker exec spark \
        spark-submit /opt/project/transform/bronze_to_silver.py
        """,
    )

    silver_to_gold = BashOperator(
        task_id="silver_to_gold",
        bash_command="""
        docker exec spark \
        spark-submit /opt/project/transform/silver_to_gold.py
        """,
    )

    validate_gold = BashOperator(
        task_id="validate_gold",
        bash_command="""
        docker exec spark spark-submit /opt/project/validation/validate_gold.py
        """,
    )

    load_to_snowflake = BashOperator(
        task_id="load_to_snowflake",
        bash_command="python /opt/project/snowflake/load_gold.py",
        retries=3,
        retry_delay=timedelta(minutes=10),
    )

    (
        download_data
        >> upload_to_bronze
        >> bronze_to_silver
        >> silver_to_gold
        >> validate_gold
        >> load_to_snowflake
    )
