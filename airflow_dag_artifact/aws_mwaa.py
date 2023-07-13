# -*- coding: utf-8 -*-

"""
This module integrations the ``airflow_dag_artifact`` Python library with
AWS MWAA. The DAG deployment in AWS MWAA is just uploading the DAG Python script
to s3://my-mwaa-bucket/prefix/dags/`` folder. This module uses a custom S3 folder
to store the versioned artifact and copy them to the MWAA DAG folder for deployment.

Usage: see https://github.com/MacHu-GWU/airflow_dag_artifact-project/blob/main/examples/aws_mwaa.py
"""

import typing as T
import dataclasses

from s3pathlib import S3Path
from boto_session_manager import BotoSesManager
from func_args import NOTHING
from .model import PT, AirflowDagArtifact


@dataclasses.dataclass
class AWSMWAA:
    """
    Airflow DAG management for AWS MWAA.

    :param s3uri_dags: the S3 folder to store MWAA DAGs. Read
        https://docs.aws.amazon.com/mwaa/latest/userguide/create-environment.html#create-environment-start
        for more information.
    :param aws_region: AWS region name of the artifact store.
    :param s3_bucket: S3 bucket name of the artifact store.
    :param s3_prefix: S3 prefix name of the artifact store.
    :param dynamodb_table_name: DynamoDB table name of the artifact store metadata.
    """

    s3uri_dags: str = dataclasses.field()
    aws_region: str = dataclasses.field()
    s3_bucket: str = dataclasses.field()
    s3_prefix: str = dataclasses.field()
    dynamodb_table_name: str = dataclasses.field()

    @property
    def s3dir_dags(self) -> S3Path:
        return S3Path(self.s3uri_dags).to_dir()

    def _get_airflow_dag_artifact(
        self,
        artifact_name: str,
        path_airflow_dag_script: PT,
    ) -> AirflowDagArtifact:
        return AirflowDagArtifact(
            aws_region=self.aws_region,
            s3_bucket=self.s3_bucket,
            s3_prefix=self.s3_prefix,
            dynamodb_table_name=self.dynamodb_table_name,
            artifact_name=artifact_name,
            path_airflow_dag_script=path_airflow_dag_script,
        )

    @property
    def _dummy_dag_artifact(self):
        return self._get_airflow_dag_artifact(
            artifact_name="",
            path_airflow_dag_script=__file__,
        )

    def bootstrap(
        self,
        bsm: BotoSesManager,
        dynamodb_write_capacity_units: T.Optional[int] = None,
        dynamodb_read_capacity_units: T.Optional[int] = None,
    ):
        """
        Create the required S3 bucket and DynamoDB table for the artifact store backend.
        """
        self._dummy_dag_artifact.bootstrap(
            bsm=bsm,
            dynamodb_write_capacity_units=dynamodb_write_capacity_units,
            dynamodb_read_capacity_units=dynamodb_read_capacity_units,
        )

    def publish_dag(
        self,
        dag_id: str,
        path_airflow_dag_script: PT,
        metadata: T.Dict[str, str] = NOTHING,
        tags: T.Dict[str, str] = NOTHING,
    ):
        """
        Publish a dag artifact to the ``LATEST`` and deploy it to AWS MWAA.

        :param dag_id: dag id.
        :param path_airflow_dag_script: The path of the Airflow DAG Python script
            for artifact.
        :param metadata: optional S3 object metadata.
        :param tags: optional S3 object tags.
        """
        dag_artifact = self._get_airflow_dag_artifact(
            artifact_name=dag_id,
            path_airflow_dag_script=path_airflow_dag_script,
        )
        artifact = dag_artifact.put_artifact(metadata=metadata, tags=tags)
        content = artifact.s3path.read_text()
        before = f'dag_id = "{dag_id}"'
        after = f'dag_id = "{dag_id}_latest"'
        if before not in content:
            raise ValueError
        content = content.replace(before, after)
        self.s3dir_dags.joinpath(f"{dag_id}_latest.py").write_text(content)
        return artifact

    def publish_dag_version(
        self,
        dag_id: str,
    ):
        """
        Publish a new version of dag artifact and deploy it to AWS MWAA.

        :param dag_id: dag id.
        """
        dag_artifact = self._get_airflow_dag_artifact(
            artifact_name=dag_id,
            path_airflow_dag_script=__file__,
        )
        artifact = dag_artifact.publish_artifact_version()
        content = artifact.s3path.read_text()
        before = f'dag_id = "{dag_id}"'
        after = f'dag_id = "{dag_id}_v{artifact.version}"'
        if before not in content:
            raise ValueError
        content = content.replace(before, after)
        self.s3dir_dags.joinpath(f"{dag_id}_v{artifact.version}.py").write_text(content)
        return artifact

    def purge_dag(self, dag_id: str):
        """
        Completely delete all artifacts of the given dag.
        This operation is irreversible. It will remove all related S3 artifacts
        and DynamoDB items.

        :param dag_id: dag id.
        """
        self._dummy_dag_artifact.repo.purge_artifact(name=dag_id)

    def purge_all_dag(self):
        """
        Completely delete all dag artifacts in the backend Repository
        This operation is irreversible. It will remove all related S3 artifacts
        and DynamoDB items.
        """
        _dummy_dag_artifact = self._dummy_dag_artifact
        _dummy_dag_artifact.repo.purge_all()
