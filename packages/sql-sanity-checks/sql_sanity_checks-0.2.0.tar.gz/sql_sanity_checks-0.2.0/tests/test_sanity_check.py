import pytest
from unittest.mock import MagicMock, patch, mock_open
from sanity_checks import SanityCheck, DefaultOutput


@pytest.fixture
def mock_connector():
    connector = MagicMock()
    return connector


@pytest.fixture
def mock_output():
    output = MagicMock(spec=DefaultOutput)
    return output


@patch.object(DefaultOutput, 'log')
@patch.object(DefaultOutput, 'error')
@patch.object(SanityCheck, 'run')
def test_check_results_no_errors(mock_run, mock_error, mock_log, mock_connector, mock_output):
    sanity_check_instance = SanityCheck(tests_path="../sql_tests/", connector=None, output_objects=[DefaultOutput()])
    # Simulate SQL execution with no errors
    sanity_check_instance.data = [{'filename': 'test1.sql', 'sql_code': 'SELECT * FROM table;', 'result': None}]
    sanity_check_instance.check_results()
    mock_log.assert_called_once_with('test1.sql', [], 'SELECT * FROM table;')
    mock_error.assert_not_called()


@patch.object(DefaultOutput, 'log')
@patch.object(DefaultOutput, 'error')
@patch.object(SanityCheck, 'run')
def test_check_results_with_errors(mock_run, mock_error, mock_log, mock_connector, mock_output):
    sanity_check_instance = SanityCheck(tests_path="../sql_tests/", connector=None, output_objects=[DefaultOutput()])
    # Simulate SQL execution with an error
    sanity_check_instance.data = [{'filename': 'test2.sql', 'sql_code': 'SELECT * FROM non_existing_table;', 'result': 'Error'}]
    # Assert that an exception is raised
    with pytest.raises(Exception):
        sanity_check_instance.check_results()
    mock_error.assert_called_once_with('test2.sql', 'Error', 'SELECT * FROM non_existing_table;')
    mock_log.assert_not_called()


@patch.object(SanityCheck, 'run')
def test_sanity_check_init(mock_run, mock_connector, mock_output):
    output_objects = [mock_output]
    tests_path = "../sql_tests/"
    sanity_check = SanityCheck(tests_path=tests_path, connector=mock_connector, output_objects=output_objects)
    assert sanity_check.connector == mock_connector
    assert sanity_check.output_objects == output_objects
    assert sanity_check.tests_path == tests_path
    assert sanity_check.data == []
    assert sanity_check.sql_files == []


@patch.object(SanityCheck, 'run')
def test_get_sql_files_with_mocked_files(mock_run):
    mock_filenames = ["test1.sql"]
    mock_file_content = "SELECT * FROM table;"
    with patch('os.listdir', return_value=mock_filenames), \
         patch('builtins.open', mock_open(read_data=mock_file_content)) as mocked_file:
        sanity_check_instance = SanityCheck(tests_path="../sql_tests/", connector=None, output_objects=None)
        sanity_check_instance.get_sql_files()
        assert len(sanity_check_instance.data) == 1, "Data should contain two items for two SQL files"
        for item in sanity_check_instance.data:
            assert item['sql_code'] == mock_file_content, "SQL code should match the mock file content"
        mocked_file.assert_called_with('../sql_tests/test1.sql', 'r', encoding='utf-8')


@patch.object(SanityCheck, 'get_sql_files')
@patch.object(SanityCheck, 'execute_sql')
@patch.object(SanityCheck, 'check_results')
def test_sanity_check_run(mock_check_results, mock_execute_sql, mock_get_sql_files, mock_connector, mock_output):
    SanityCheck(connector=mock_connector, output_objects=[mock_output])
    mock_get_sql_files.assert_called_once()
    mock_execute_sql.assert_called_once()
    mock_check_results.assert_called_once()
