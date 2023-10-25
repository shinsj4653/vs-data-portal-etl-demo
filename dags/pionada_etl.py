from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from sqlalchemy import create_engine
import pandas as pd

# load varaibles from the .env file
load_dotenv()

# Define your default_args, schedule_interval, and other DAG configurations
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 24),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'pionada_etl',
    default_args=default_args,
    description='An example DAG to copy data from one PostgreSQL DB to another',
    schedule_interval=timedelta(days=1),  # Set your schedule interval
)

# Define a function to fetch data from source PostgreSQL DB
def fetch_data_from_source_db():
    source_engine = create_engine(f'postgresql://{FETCH_USER_NAME}:{FETCH_USER_PW}@{FETCH_DB_URL}/{FETCH_DB_NAME}')
    df = pd.read_sql(f'SELECT * FROM {FETCH_TABLE_NAME}', source_engine)
    return df

# Define a function to write data to target PostgreSQL DB
def write_data_to_target_db(**kwargs):
    target_engine = create_engine(f'postgresql://{WRITE_USER_NAME}:{WRITE_USER_PW}@{WRITE_DB_URL}/{WRITE_DB_NAME}')
    ti = kwargs['ti']
    df = ti.xcom_pull(task_ids='fetch_data_from_source_db')
    df.to_sql(f'{WRITE_TABLE_NAME}', target_engine, if_exists='replace', index=False)

# Define tasks
fetch_data_task = PythonOperator(
    task_id='fetch_data_from_source_db',
    python_callable=fetch_data_from_source_db,
    dag=dag,
)

write_data_task = PythonOperator(
    task_id='write_data_to_target_db',
    python_callable=write_data_to_target_db,
    provide_context=True,
    dag=dag,
)

# Set task dependencies
fetch_data_task >> write_data_task