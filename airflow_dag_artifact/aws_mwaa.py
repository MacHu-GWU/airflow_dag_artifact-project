# -*- coding: utf-8 -*-

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
    """

    s3dir_dags: S3Path = dataclasses.field()
    aws_region: str = dataclasses.field()
    s3_bucket: str = dataclasses.field()
    s3_prefix: str = dataclasses.field()
    dynamodb_table_name: str = dataclasses.field()

    def bootstrap(
        self,
        bsm: BotoSesManager,
        dynamodb_write_capacity_units: T.Optional[int] = None,
        dynamodb_read_capacity_units: T.Optional[int] = None,
    ):
        self.get_airflow_dag_artifact(
            artifact_name="",
            path_airflow_dag_script=__file__,
        ).bootstrap(
            bsm=bsm,
            dynamodb_write_capacity_units=dynamodb_write_capacity_units,
            dynamodb_read_capacity_units=dynamodb_read_capacity_units,
        )

    def get_airflow_dag_artifact(
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

    def publish_dag(
        self,
        dag_id: str,
        path_airflow_dag_script: PT,
        metadata: T.Dict[str, str] = NOTHING,
        tags: T.Dict[str, str] = NOTHING,
    ):
        dag_artifact = self.get_airflow_dag_artifact(
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

    def publish_dag_version(
        self,
        dag_id: str,
        path_airflow_dag_script: PT,
    ):
        dag_artifact = self.get_airflow_dag_artifact(
            artifact_name=dag_id,
            path_airflow_dag_script=path_airflow_dag_script,
        )
        artifact = dag_artifact.publish_artifact_version()
        content = artifact.s3path.read_text()
        before = f'dag_id = "{dag_id}"'
        after = f'dag_id = "{dag_id}_v{artifact.version}"'
        if before not in content:
            raise ValueError
        content = content.replace(before, after)
        self.s3dir_dags.joinpath(f"{dag_id}_v{artifact.version}.py").write_text(content)
