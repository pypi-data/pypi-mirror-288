import pytest
from unittest.mock import patch, Mock
from output_slack import SlackOutput


@pytest.fixture
def slack_output():
    token = "test_token"
    channel = "#test_channel"
    with patch('output_slack.WebClient') as MockWebClient:
        mock_client = MockWebClient.return_value
        mock_client.chat_postMessage.return_value = {"message": {"text": "test message"}}
        yield SlackOutput(token, channel), mock_client


def test_initialization(slack_output):
    slack_output_instance, _ = slack_output
    assert slack_output_instance.channel == "#test_channel"
    assert isinstance(slack_output_instance.client, Mock)


def test_post_message_success(slack_output):
    slack_output_instance, mock_client = slack_output
    message = "test message"
    slack_output_instance.post_message(message)
    mock_client.chat_postMessage.assert_called_once_with(channel="#test_channel", text=message)


@patch.object(SlackOutput, 'post_message')
def test_log_with_test_result(mock_post_message):
    slacker = SlackOutput("test_token", "#test_channel")
    slacker.log("test_name", [], "code")
    mock_post_message.assert_called_with("[sql_sanity_checks] test_name has returned no error")


@patch.object(SlackOutput, 'post_message')
def test_error(mock_post_message):
    slacker = SlackOutput("test_token", "#test_channel")
    slacker.error("test_name", "test_result", "code")
    mock_post_message.assert_called_with("[sql_sanity_checks] Errors returned for the test test_name. Please check the logs for more information.")
