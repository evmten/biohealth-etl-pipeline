from airflow import DAG
from airflow.operators.bash import BashOperator # type: ignore
from datetime import datetime, timedelta
from airflow.operators.trigger_dagrun import TriggerDagRunOperator # type: ignore

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    dag_id='health_data_pipeline',
    default_args=default_args,
    schedule_interval=None, 
    catchup=False,
    tags=['health', 'pipeline']
) as dag:

    run_etl = BashOperator(
        task_id='run_health_etl',
        bash_command='python /opt/airflow/src/run_health_etl.py',
    )


trigger_validation = TriggerDagRunOperator(
    task_id='trigger_validation_dag',
    trigger_dag_id='validate_health_data',
)

run_etl >> trigger_validation
