from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.sdk import TaskInstance


default_args = {
    "owner" : "airflow",
    "retries" : 1,
    "retry_delay" : timedelta(minutes=5)
}

@dag(
    dag_id="test_dag",
    default_args=default_args,
    description="TEST DAG",
    start_date=datetime(2026,1,1),
    schedule="@daily",
    catchup=False
)

def my_test():

    @task
    def task_1(task_instance: TaskInstance):
        print(f"Run ID: {task_instance.run_id}")
        print("This is task 1")

    @task
    def task_2():
        print("This is task 2")

    task_1()
    task_2()

my_test()