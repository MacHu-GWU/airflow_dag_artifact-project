# -*- coding: utf-8 -*-

from boto_session_manager import BotoSesManager
from s3pathlib import S3Path
from pathlib_mate import Path
from airflow_dag_artifact.api import AWSMWAA

bsm = BotoSesManager(profile_name="awshsh_app_dev_us_east_1")
mwaa = AWSMWAA(
    s3dir_dags=S3Path(f"s3://{bsm.aws_account_id}-{bsm.aws_region}-airflow/dags/"),
    aws_region=bsm.aws_region,
    s3_bucket=f"{bsm.aws_account_id}-{bsm.aws_region}-artifacts",
    s3_prefix=f"versioned-artifacts",
    dynamodb_table_name="versioned-artifacts",
)
mwaa.bootstrap(bsm=bsm)

dir_dags = Path.dir_here(__file__) / "dags"
path_dag1 = dir_dags / "dag1.py"

# this is how you publish to latest (overwrite), for debug / test
mwaa.publish_dag(dag_id="dag1", path_airflow_dag_script=path_dag1)

# this is how you publish a new immutable version for production, blue / green deployment
mwaa.publish_dag_version(dag_id="dag1", path_airflow_dag_script=path_dag1)
