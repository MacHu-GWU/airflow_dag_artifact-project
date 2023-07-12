# -*- coding: utf-8 -*-

import moto

from airflow_dag_artifact.tests.mock_aws import BaseMockTest

from airflow_dag_artifact.model import (
    AirflowDagArtifact,
)


class Test(BaseMockTest):
    use_mock = True

    mock_list = [
        moto.mock_sts,
        moto.mock_s3,
        moto.mock_dynamodb,
    ]

    def _test(self):
        aws_region = "us-east-1"
        s3_bucket = "my-bucket"
        s3_prefix = "airflow-artifact"
        dynamodb_table_name = "airflow-artifact"

        glue_etl_script_artifact = AirflowDagArtifact(
            aws_region=aws_region,
            s3_bucket=s3_bucket,
            s3_prefix=s3_prefix,
            dynamodb_table_name=dynamodb_table_name,
            artifact_name="airflow_dag_script_1",
            path_airflow_dag_script=__file__,
        )
        glue_etl_script_artifact.bootstrap(bsm=self.bsm)
        artifact = glue_etl_script_artifact.put_artifact(metadata={"foo": "bar"})
        assert (
            artifact.s3uri
            == f"s3://{s3_bucket}/{s3_prefix}/airflow_dag_script_1/LATEST.py"
        )

        s3path = glue_etl_script_artifact.get_artifact_s3path()
        assert (
            s3path.uri == f"s3://{s3_bucket}/{s3_prefix}/airflow_dag_script_1/LATEST.py"
        )
        artifact = glue_etl_script_artifact.publish_artifact_version()
        assert (
            artifact.s3uri
            == f"s3://{s3_bucket}/{s3_prefix}/airflow_dag_script_1/000001.py"
        )
        print(artifact)

    def test(self):
        self._test()


if __name__ == "__main__":
    from airflow_dag_artifact.tests import run_cov_test

    run_cov_test(__file__, "airflow_dag_artifact.model", preview=False)
