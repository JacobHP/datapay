import pytest
from airflow.models import DagBag
# if on machine
# for tests need to run 'airflow db init'
# export AIRFLOW_HOME
# and potentially export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# if using docker
# docker exec airflow-airflow-worker-1 pytest

# https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#dag-loader-test


@pytest.fixture()
def dagbag():
    return DagBag()


def test_reed_dag_loaded(dagbag):
    dag = dagbag.get_dag(dag_id='reed_dag')
    print(dagbag.import_errors)
    assert dagbag.import_errors == {}
    assert dag is not None
    assert len(dag.tasks) == 4


def assert_dag_dict_equal(source, dag):
    assert dag.task_dict.keys() == source.keys()
    for task_id, downstream_list in source.items():
        assert dag.has_task(task_id)
        task = dag.get_task(task_id)
        assert task.downstream_task_ids == set(downstream_list)


source = {
    'extract': ['gcs_to_bq_details', 'gcs_to_bq_listings'],
    'gcs_to_bq_details': ['dbt'],
    'gcs_to_bq_listings': ['dbt'],
    'dbt': []
}


def test_reed_dag(dagbag):
    dag = dagbag.get_dag(dag_id='reed_dag')
    assert_dag_dict_equal(source, dag)
