from airflow import DAG
from airflow.operators.bash import BashOperator # type: ignore
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='validate_health_data',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['validation', 'health'],
) as dag:

    run_validation = BashOperator(
        task_id='validate_data',
        bash_command='python /opt/airflow/src/validation/validate_health_data.py',
    )
