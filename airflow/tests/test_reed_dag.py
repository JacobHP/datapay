import pytest 
from airflow.models import DagBag
# for tests need to run 'airflow db init'
# and potentially export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
#https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#dag-loader-test
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
    pass 

def test_reed_dag():
    pass
