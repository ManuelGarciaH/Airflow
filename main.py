from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 3, 8),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG('world_clock', default_args=default_args, schedule_interval='*/5 * * * *')

usa_task = BashOperator(
    task_id='usa',
    bash_command='echo "USA: $(TZ=America/New_York date)" >> /tmp/world_clock.txt',
    dag=dag,
)

germany_task = BashOperator(
    task_id='germany',
    bash_command='echo "Germany: $(TZ=Europe/Berlin date)" >> /tmp/world_clock.txt',
    dag=dag,
)

japan_task = BashOperator(
    task_id='japan',
    bash_command='echo "Japan: $(TZ=Asia/Tokyo date)" >> /tmp/world_clock.txt',
    dag=dag,
)

usa_task >> germany_task >> japan_task
