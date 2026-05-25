from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'credit_risk_team',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2026, 1, 1),
}

dag = DAG(
    'credit_risk_elt_pipeline',
    default_args=default_args,
    description='Credit Risk ELT Pipeline',
    schedule_interval='0 2 * * *',  # Daily at 2 AM
    catchup=False,
)

def ingestion_task():
    """Data ingestion phase"""
    print("Starting data ingestion...")

def transformation_task():
    """Data transformation phase"""
    print("Starting data transformation...")

def serving_task():
    """Data serving phase"""
    print("Starting data serving...")

# Define tasks
t1 = PythonOperator(
    task_id='ingestion',
    python_callable=ingestion_task,
    dag=dag,
)

t2 = PythonOperator(
    task_id='transformation',
    python_callable=transformation_task,
    dag=dag,
)

t3 = PythonOperator(
    task_id='serving',
    python_callable=serving_task,
    dag=dag,
)

# Define dependencies
t1 >> t2 >> t3
