# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from airflow_dag_artifact.tests import run_cov_test

    run_cov_test(__file__, "airflow_dag_artifact", is_folder=True, preview=False)
