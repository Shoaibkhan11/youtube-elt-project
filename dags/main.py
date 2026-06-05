from airflow import DAG
import pendulum
from datetime import datetime,timedelta
from api.video_stats import get_playlist_id,get_video_ids,extract_video_data,save_to_json
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from datawarehouse.dwh import staging_table,core_table
from dataquality.soda import yt_elt_data_quality



#define local timezone
local_tz=pendulum.timezone("Asia/Kolkata")

#default args

default_args={
    "owner":"shoaib",
    "depends_on_past":False,
    "email_on_failure":False,
    "email_on_retry":False,
    "email":"shoaibkhan11374@gmail.com",
    "max_active_runs":1,
    "dagrun_timeout":timedelta(hours=1),
    "start_date": datetime(2025,1,1,tzinfo=local_tz),
}

staging_schema = "staging"
core_schema = "core"

with DAG(
    dag_id='produce_json',
    default_args=default_args,
    description='A DAG to produce JSON file with raw data',
    schedule='0 14 * * *',
    catchup=False
) as dag_produce:
    
    #define tasks
    playlist_id=get_playlist_id()
    video_id=get_video_ids(playlist_id)
    extracted_data=extract_video_data(video_id)
    save_to_json_task=save_to_json(extracted_data)

    trigger_update_db=TriggerDagRunOperator(
        task_id="trigger_update_db",
        trigger_dag_id="update_db"
    )

    # define dependencies
    playlist_id >> video_id >> extracted_data >> save_to_json_task>> trigger_update_db

with DAG(
    dag_id='update_db',
    default_args=default_args,
    description="DAG to process JSON file and insert data into both staging and core schemas",
    schedule=None,
    catchup=False
) as dag_update:
    
    update_staging=staging_table()
    update_core=core_table()

    trigger_data_quality=TriggerDagRunOperator(
        task_id="trigger_data_quality",
        trigger_dag_id="data_quality"
    )

    update_staging >> update_core >> trigger_data_quality

with DAG(
    dag_id='data_quality',
    default_args=default_args,
    description="DAG to perform data quality checks using Soda",
    schedule=None,
    catchup=False
) as data_quality:
    
    soda_validate_staging = yt_elt_data_quality(staging_schema)
    soda_validate_core = yt_elt_data_quality(core_schema)

    soda_validate_staging >> soda_validate_core