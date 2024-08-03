import pytest
from unittest.mock import patch, MagicMock
from connector_postgresql import PostgreSQLConnector


@pytest.fixture
def mock_db():
    with patch('psycopg2.connect') as mock_connect:
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        db_params = {
            "host": "localhost",
            "port": 5432,
            "database": "test_db",
            "user": "test_user",
            "password": "test_password"
        }
        with PostgreSQLConnector(db_params) as db:
            yield db, mock_connection, mock_cursor


def test_connection(mock_db):
    db, mock_connection, mock_cursor = mock_db
    assert db.connection == mock_connection
    assert db.cursor == mock_cursor


def test_execute_query(mock_db):
    db, mock_connection, mock_cursor = mock_db
    mock_cursor.fetchall.return_value = [('Alice',)]
    result = db.execute_query("SELECT * FROM test")
    mock_cursor.execute.assert_called_once_with("SELECT * FROM test")
    assert result == [('Alice',)]


def test_execute_query_with_params(mock_db):
    db, mock_connection, mock_cursor = mock_db
    mock_cursor.fetchall.return_value = [('Bob',)]
    result = db.execute_query("SELECT * FROM test WHERE name = %s", ('Bob',))
    mock_cursor.execute.assert_called_once_with("SELECT * FROM test WHERE name = %s", ('Bob',))
    assert result == [('Bob',)]


def test_query_error_handling(mock_db):
    db, mock_connection, mock_cursor = mock_db
    mock_cursor.execute.side_effect = Exception("Query error")
    with pytest.raises(Exception, match="Query error"):
        db.execute_query("SELECT * FROM non_existing_table")


def test_connection_closing(mock_db):
    db, mock_connection, mock_cursor = mock_db
    db.close()
    mock_cursor.close.assert_called_once()
    mock_connection.close.assert_called_once()
    assert db.closed
