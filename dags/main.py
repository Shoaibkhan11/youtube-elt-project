from airflow import DAG
import pendulum
from datetime import datetime,timedelta
from api.video_stats import get_playlist_id,get_video_ids,extract_video_data,save_to_json

from datawarehouse.dwh import staging_table,core_table

#define local timezone
local_tz=pendulum.timezone("Asia/Kolkata")

#default args

default_args={
    "owner":"shoaib",
    "depends_on_past":"False",
    "email_on_failure":"False",
    "email_on_retry":"False",
    "email":"shoaibkhan11374@gmail.com",
    "max_active_runs":1,
    "dagrun_timeout":timedelta(hours=1),
    "start_date": datetime(2025,1,1,tzinfo=local_tz),
}

with DAG(
    dag_id='produce_json',
    default_args=default_args,
    description='A DAG to produce JSON file with raw data',
    schedule='0 14 * * *',
    catchup=False
) as dag:
    
    #define tasks
    playlist_id=get_playlist_id()
    video_id=get_video_ids(playlist_id)
    extracted_data=extract_video_data(video_id)
    save_to_json_task=save_to_json(extracted_data)

    # define dependencies
    playlist_id >> video_id >> extracted_data >> save_to_json_task

with DAG(
    dag_id='update_db',
    default_args=default_args,
    description="DAG to process JSON file and insert data into both staging and core schemas",
    schedule='0 15 * * *',
    catchup=False
) as dag:
    
    update_staging=staging_table()
    update_core=core_table()

    update_staging >> update_core