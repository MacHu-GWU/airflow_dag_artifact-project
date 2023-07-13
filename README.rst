
.. .. image:: https://readthedocs.org/projects/airflow-dag-artifact/badge/?version=latest
    :target: https://airflow-dag-artifact.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/airflow_dag_artifact-project/workflows/CI/badge.svg
    :target: https://github.com/MacHu-GWU/airflow_dag_artifact-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/airflow_dag_artifact-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/airflow_dag_artifact-project

.. image:: https://img.shields.io/pypi/v/airflow-dag-artifact.svg
    :target: https://pypi.python.org/pypi/airflow-dag-artifact

.. image:: https://img.shields.io/pypi/l/airflow-dag-artifact.svg
    :target: https://pypi.python.org/pypi/airflow-dag-artifact

.. image:: https://img.shields.io/pypi/pyversions/airflow-dag-artifact.svg
    :target: https://pypi.python.org/pypi/airflow-dag-artifact

.. image:: https://img.shields.io/badge/Release_History!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/airflow_dag_artifact-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/airflow_dag_artifact-project

------

.. .. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://airflow-dag-artifact.readthedocs.io/en/latest/

.. .. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://airflow-dag-artifact.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/airflow_dag_artifact-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/airflow_dag_artifact-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/airflow_dag_artifact-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/airflow-dag-artifact#files


Welcome to ``airflow_dag_artifact`` Documentation
==============================================================================
A lot of serverless AWS Service supports versioning and alias for deployment. It made the blue / green deployment, canary deployment and rolling back super easy.

- `AWS Lambda Versioning and Alias <https://docs.aws.amazon.com/lambda/latest/dg/configuration-versions.html>`_
- `AWS StepFunction Versioning and Alias <https://docs.aws.amazon.com/step-functions/latest/dg/auth-version-alias.html>`_
- `AWS SageMaker Model Registry Versioning <https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html>`_

However, Airflow DAG does not support this feature yet. This library provides a way to manage Airflow DAG versioning and alias so you can deploy Airflow DAG with confidence.

Please `read this tutorial <https://github.com/MacHu-GWU/airflow_dag_artifact-project/blob/main/examples/deploy_versioned_airflow_dag_artifacts.ipynb>`_ to learn how to use this library.

It also has native `AWS MWAA <https://aws.amazon.com/managed-workflows-for-apache-airflow/>`_ support for DAG deployment automation, with the DAG versioning manage, which is not official supported by Apache Airflow. Please `read this example <https://github.com/MacHu-GWU/airflow_dag_artifact-project/blob/main/examples/aws_mwaa.py>`_ to learn how to use this library with AWS MWAA.


.. _install:

Install
------------------------------------------------------------------------------

``airflow_dag_artifact`` is released on PyPI, so all you need is to:

.. code-block:: console

    $ pip install airflow-dag-artifact

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade airflow-dag-artifact
