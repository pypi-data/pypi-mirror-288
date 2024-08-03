import pytest
from connector_sqlite import SQLiteDBConnector


@pytest.fixture
def db():
    with SQLiteDBConnector(':memory:') as db:
        db.execute_query("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)")
        yield db


def test_connection(db):
    assert db.connection is not None
    assert db.cursor is not None


def test_execute_query(db):
    db.execute_query("INSERT INTO test (name) VALUES (?)", ('Alice',))
    result = db.execute_query("SELECT * FROM test")
    assert len(result) == 1
    assert result[0][1] == 'Alice'


def test_execute_query_with_params(db):
    db.execute_query("INSERT INTO test (name) VALUES (?)", ('Bob',))
    result = db.execute_query("SELECT * FROM test WHERE name = ?", ('Bob',))
    assert len(result) == 1
    assert result[0][1] == 'Bob'


def test_query_error_handling(db):
    result = db.execute_query("SELECT * FROM non_existing_table")
    assert result is None


def test_connection_closing(db):
    db.close()
    assert db.closed
