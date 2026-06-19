from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import os

default_args = {
    'owner': 'data_engineer',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(hours=1),
    'email_on_failure': True,  # need to configure Airflow SMTP
}

DBT_PROJECT_DIR = os.path.expanduser('~/code_repo/credit-risk-elt-engine/dbt_project')

with DAG(
    dag_id='credit_risk_dbt_pipeline',
    default_args=default_args,
    description='Orchestrates dbt build for Credit Risk ELT Engine (Snapshot -> Run -> Test)',
    schedule_interval='0 2 * * *',  # launch at 02:00 every day
    start_date=days_ago(1),
    catchup=False,
    tags=['credit_risk', 'dbt', 'snowflake'],
    max_active_runs=1,
) as dag:

    # dbt build seed → snapshot → run → test
    dbt_build = BashOperator(
        task_id='dbt_build',
        bash_command=(
            f'cd {DBT_PROJECT_DIR} && '
            'source ../.env && '
            'dbt build '
            '--target prod '
            '--profiles-dir ./.dbt '
            '--vars \'{"run_date": "{{ ds }}"}\' '
            '--no-partial-parse'
        ),
        env={**os.environ, 'PYTHONPATH': os.path.join(DBT_PROJECT_DIR, '..')},
    )

    #
    check_freshness = BashOperator(
        task_id='check_source_freshness',
        bash_command=f'cd {DBT_PROJECT_DIR} && source ../.env && dbt source freshness --profiles-dir ./.dbt --target prod',
        retries=1,
    )

    dbt_build >> check_freshness