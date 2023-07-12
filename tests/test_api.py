# -*- coding: utf-8 -*-

from airflow_dag_artifact import api


def test():
    _ = api
    _ = api.AirflowDagArtifact


if __name__ == "__main__":
    from airflow_dag_artifact.tests import run_cov_test

    run_cov_test(__file__, "airflow_dag_artifact.api", preview=False)
