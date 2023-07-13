# -*- coding: utf-8 -*-

"""
This is an example of how to use ``airflow_dag_artifact`` to publish Airflow DAG
 and manage versions on AWS MWAA.
"""

from boto_session_manager import BotoSesManager
from pathlib_mate import Path
from airflow_dag_artifact.api import AWSMWAA

# Create a boto session manager object using your credential
bsm = BotoSesManager(profile_name="awshsh_app_dev_us_east_1")

# Create an AWSMWAA object that will be used to publish DAGs
mwaa = AWSMWAA(
    s3uri_dags=f"s3://{bsm.aws_account_id}-{bsm.aws_region}-airflow/dags/",
    aws_region=bsm.aws_region,
    s3_bucket=f"{bsm.aws_account_id}-{bsm.aws_region}-artifacts",
    s3_prefix=f"versioned-artifacts",
    dynamodb_table_name="versioned-artifacts",
)
# Create the required S3 bucket and DynamoDB table for the artifact store backend.
mwaa.bootstrap(bsm=bsm)

# Locate the DAG file on your local machine
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
