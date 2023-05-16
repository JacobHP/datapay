from datetime import datetime, date

from airflow import DAG
from airflow.providers.google.cloud.operators.cloud_build import CloudBuildCreateBuildOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

PROJECT_ID = 'jacobhp-personal'
BUCKET = 'datapay'
DATASET = 'datapay'

default_args = {
    'depends_on_past': False,
    'project_id': PROJECT_ID,
    'gcp_conn_id': 'google_cloud_default',
    'bucket': BUCKET,
    'dataset': DATASET
}

today_date = datetime.now().strftime("%Y%m%d")
listings_table_name = f'datapay.stg_listings${today_date}' 
details_table_name = f'datapay.stg_details${today_date}' 


with DAG("reed_dag",
         start_date=datetime(2023, 1, 1),
         schedule_interval=None
         ) as dag:

    extract_build_steps = {
        "steps": [{"name": "gcr.io/cloud-builders/docker",
                   "entrypoint": "docker",
                   "args":
                   ["run", "europe-west1-docker.pkg.dev/jacobhp-personal/datapay-extract/extract:latest"]
                   }]
    }

    # this is easier than creating a custom cloud run operator
    extract = CloudBuildCreateBuildOperator(
        task_id='extract',
        build=extract_build_steps,
        project_id='jacobhp-personal'
    )

    # want to pull the filename xcom from this
    # and add file sensors hereß

    copy_bigquery_listings = GCSToBigQueryOperator(
        task_id='gcs_to_bq_listings',
        bucket=default_args['bucket'],
        source_objects=f"reed/reed_listings_{date.today().strftime('%Y%m%d')}.json",
        source_format='NEWLINE_DELIMITED_JSON',
        write_disposition='WRITE_TRUNCATE',
        create_disposition='CREATE_IF_NEEDED',
        autodetect=True,
        destination_project_dataset_table=listings_table_name
    )

    copy_bigquery_details = GCSToBigQueryOperator(
        task_id='gcs_to_bq_details',
        bucket=default_args['bucket'],
        source_objects=f"reed/reed_details_{date.today().strftime('%Y%m%d')}.json",
        source_format='NEWLINE_DELIMITED_JSON',
        write_disposition='WRITE_TRUNCATE',
        create_disposition='CREATE_IF_NEEDED',
        autodetect=True,
        destination_project_dataset_table=details_table_name
    )

    dbt_build_steps = {
        "steps": [{"name": "gcr.io/cloud-builders/docker",
                   "entrypoint": "docker",
                   "args":
                   ["run", "europe-west1-docker.pkg.dev/jacobhp-personal/datapay-dbt/dbt:latest"]
                   }]
    }

    run_dbt = CloudBuildCreateBuildOperator(
        task_id='dbt',
        build=dbt_build_steps, 
        project_id='jacobhp-personal'
    )

    extract >> [copy_bigquery_listings, copy_bigquery_details] >> run_dbt
