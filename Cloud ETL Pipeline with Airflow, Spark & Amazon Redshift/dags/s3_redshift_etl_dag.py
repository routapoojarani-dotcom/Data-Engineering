from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    's3_redshift_etl',
    default_args=default_args,
    description='S3 to Redshift ETL job',
    schedule_interval=timedelta(days=1),
)

etl_task = KubernetesPodOperator(
    task_id='s3_redshift_etl_task',
    name='s3-redshift-etl',
    namespace='default',
    image='etlkubedocker/s3-redshift-etl:v1',
    cmds=["spark-submit", "--jars", "redshift-jdbc42-2.1.0.1.jar", "/app/etl_job.py"],
    env_vars={
        'AWS_SECRET_NAME': '{{ var.value.aws_secret_name }}',
        'AWS_REGION': '{{ var.value.aws_region }}',
        'REDSHIFT_HOST': '{{ var.value.redshift_host }}',
        'REDSHIFT_PORT': '{{ var.value.redshift_port }}',
        'REDSHIFT_DATABASE': '{{ var.value.redshift_database }}',
        'REDSHIFT_USER': '{{ var.value.redshift_user }}',
    },
    resources={'request_cpu': '1', 'request_memory': '2Gi', 'limit_cpu': '2', 'limit_memory': '4Gi'},
    is_delete_operator_pod=True,
    in_cluster=True,
    dag=dag
)