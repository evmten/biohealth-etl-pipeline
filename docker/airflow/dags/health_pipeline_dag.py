# health_pipeline_dag.py

from airflow import DAG
from airflow.operators.bash import BashOperator # type: ignore
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    dag_id='health_data_pipeline',
    default_args=default_args,
    schedule_interval=None,  # Manual for now
    catchup=False,
    tags=['health', 'pipeline']
) as dag:

    run_etl = BashOperator(
        task_id='run_health_etl',
        bash_command='python /opt/airflow/dags/run_etl.py',
    )
