# -*- coding: utf-8 -*-

from boto_session_manager import BotoSesManager
from pathlib_mate import Path
from airflow_dag_artifact.api import AWSMWAA

bsm = BotoSesManager(profile_name="awshsh_app_dev_us_east_1")
mwaa = AWSMWAA(
    s3uri_dags=f"s3://{bsm.aws_account_id}-{bsm.aws_region}-airflow/dags/",
    aws_region=bsm.aws_region,
    s3_bucket=f"{bsm.aws_account_id}-{bsm.aws_region}-artifacts",
    s3_prefix=f"versioned-artifacts",
    dynamodb_table_name="versioned-artifacts",
)
mwaa.bootstrap(bsm=bsm)

dir_dags = Path.dir_here(__file__) / "dags"
path_dag1 = dir_dags / "dag1.py"

# this is how you publish to latest (overwrite), for debug / test
artifact = mwaa.publish_dag(dag_id="dag1", path_airflow_dag_script=path_dag1)
print(f"{artifact.name} {artifact.version}: {artifact.s3path.console_url}")

# this is how you publish a new immutable version for production, blue / green deployment
# artifact = mwaa.publish_dag_version(dag_id="dag1")
# print(f"{artifact.name} {artifact.version}: {artifact.s3path.console_url}")

# this will purge all dag artifacts in the backend repository
# mwaa.purge_all_dag()
