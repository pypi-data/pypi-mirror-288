from output_default import DefaultOutput


class TestDefaultOutput:
    def test_log(self, capsys):
        default_output = DefaultOutput()
        default_output.log('test_name', 'test_result', 'code')
        captured = capsys.readouterr()
        assert '+++++++++++++++++++++++++++++++++++++++++++++++++++' in captured.out
        assert 'Test: test_name' in captured.out
        assert 'code' in captured.out
        assert 'Has returned: test_result' in captured.out
        assert '********************** ERROR *****************************' not in captured.out

    def test_error(self, capsys):
        default_output = DefaultOutput()
        default_output.error('test_name', 'test_result', 'code')
        captured = capsys.readouterr()
        assert 'ERROR' in captured.err
        assert 'Test: test_name' in captured.err
        assert 'code' in captured.err
        assert 'Has returned: test_result' in captured.err
