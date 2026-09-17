from datetime import datetime, timedelta
from airflow.decorators import dag
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
import os


default_args = {
    "owner" : "airflow",
    "retries" : 1,
    "retry_delay" : timedelta(minutes=5)
}


@dag(
    dag_id="weather_pipeline",
    default_args=default_args,
    description="Weather pipeline",
    start_date=datetime(2026,1,1),
    schedule="@hourly",
    catchup=False,
    max_active_runs=1
)

def weather_pipeline():

    fetch = DockerOperator(
        task_id="fetch_weather",
        image="weather-pipeline",
        command=["python", "fetch_weather_data.py"],
        docker_url="unix://var/run/docker.sock",
        mounts=[
            Mount(
                source=os.environ["WEATHER_DATA_HOST_PATH"],
                target='/app/data',        # Path inside the container
                type='bind',
            )
        ],
        environment={
            "PIPELINE_RUN_ID": "{{ run_id }}"
        },
        mount_tmp_dir=False,
        auto_remove="success",
    )

    quality_checks = DockerOperator(
        task_id="run_quality_checks",
        image="weather-pipeline",
        command=["python", "data_quality.py"],
        docker_url="unix://var/run/docker.sock",
        mounts=[
            Mount(
                source=os.environ["WEATHER_DATA_HOST_PATH"],
                target='/app/data',        # Path inside the container
                type='bind',
            )
        ],
        mount_tmp_dir=False,
        auto_remove="success",
    )

    fetch >> quality_checks

weather_pipeline()