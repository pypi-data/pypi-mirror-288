import json
import logging
import uuid
from unittest.mock import ANY

import pytest
import responses
from orchestra_sdk.decorators import orchestra_run

logger = logging.getLogger(__name__)

MOCK_WEBHOOK_URL = "http://orchestra-webhook-123.com/update"
EXPECTED_TASK_FUNC_LOG_TUPLE = (
    "tests.test_decorators",
    20,
    "A",
)


def mock_task_func(throw_error: bool = False) -> None:
    @orchestra_run
    def test_function(throw_error: bool):
        if throw_error:
            raise Exception("ERROR IN YOUR FUNCTION!")
        logger.info("A")

    test_function(throw_error)


class TestEnvVarsNotValid:
    def test_null_os_environ(self, mocker, caplog):
        mocker.patch.dict("os.environ", clear=True)
        with caplog.at_level(logging.INFO):
            mock_task_func()
        assert caplog.record_tuples == [
            (
                "orchestra_sdk.decorators",
                40,
                "No environment variables loaded",
            ),
            (
                "orchestra_sdk.decorators",
                20,
                "Environment configured correctly for Orchestra.",
            ),
            EXPECTED_TASK_FUNC_LOG_TUPLE,
        ]

    def test_missing_env_vars(self, mocker, caplog):
        mocker.patch.dict("os.environ", clear=True)
        mocker.patch.dict("os.environ", {"ORCHESTRA_API_KEY": "api_key"})
        with caplog.at_level(logging.INFO):
            mock_task_func()
        assert "Missing environment variables" in caplog.record_tuples[0][2]
        assert "ORCHESTRA_WEBHOOK_URL" in caplog.record_tuples[0][2]
        assert "ORCHESTRA_TASK_RUN_ID" in caplog.record_tuples[0][2]
        assert "ORCHESTRA_PIPELINE_RUN_ID" in caplog.record_tuples[0][2]
        assert caplog.record_tuples[2] == EXPECTED_TASK_FUNC_LOG_TUPLE

    def test_malformed_env_vars(self, mocker, caplog):
        mocker.patch.dict("os.environ", clear=True)
        mocker.patch.dict(
            "os.environ",
            {
                "ORCHESTRA_API_KEY": "api_key",
                "ORCHESTRA_WEBHOOK_URL": "webhook_url",
                "ORCHESTRA_TASK_RUN_ID": "task_run_id",
                "ORCHESTRA_PIPELINE_RUN_ID": "pipeline_run_id",
            },
        )
        with caplog.at_level(logging.INFO):
            mock_task_func()
        assert caplog.record_tuples == [
            (
                "orchestra_sdk.decorators",
                40,
                "Error processing environment variables: badly formed hexadecimal UUID string",
            ),
            (
                "orchestra_sdk.decorators",
                20,
                "Environment configured correctly for Orchestra.",
            ),
            EXPECTED_TASK_FUNC_LOG_TUPLE,
        ]


class TestSendingTaskUpdates:
    @pytest.fixture
    def mock_task_run_id(self):
        return uuid.uuid4()

    @pytest.fixture
    def mock_pipeline_run_id(self):
        return uuid.uuid4()

    @pytest.fixture(autouse=True)
    def set_correct_env_vars(self, mocker, mock_task_run_id, mock_pipeline_run_id):
        mocker.patch.dict(
            "os.environ",
            {
                "ORCHESTRA_API_KEY": "api_key",
                "ORCHESTRA_WEBHOOK_URL": MOCK_WEBHOOK_URL,
                "ORCHESTRA_TASK_RUN_ID": str(mock_task_run_id),
                "ORCHESTRA_PIPELINE_RUN_ID": str(mock_pipeline_run_id),
            },
        )

    @responses.activate
    def test_webhook_non_200(self, caplog):
        responses.add(
            responses.POST,
            MOCK_WEBHOOK_URL,
            status=404,
            json={"error": "Could not find API"},
        )

        with caplog.at_level(logging.ERROR):
            mock_task_func()

        assert caplog.record_tuples == [
            (
                "orchestra_sdk.http",
                40,
                "Failed request (404): {'error': 'Could not find API'}",
            ),
            (
                "orchestra_sdk.http",
                40,
                "Failed request (404): {'error': 'Could not find API'}",
            ),
        ]

    @responses.activate
    def test_works_func_succeeded(self, mock_task_run_id):
        requests_made = responses.add(
            responses.POST,
            MOCK_WEBHOOK_URL,
            status=200,
        )

        mock_task_func()

        assert requests_made.call_count == 2
        assert json.loads(requests_made.calls[0].request.body or "{}") == {
            "event_type": "UPDATE_STATUS",
            "metadata": {},
            "task_run_id": str(mock_task_run_id),
            "timestamp": ANY,
            "message": "test_function started.",
            "status": "RUNNING",
        }
        assert json.loads(requests_made.calls[1].request.body or "{}") == {
            "event_type": "UPDATE_STATUS",
            "metadata": {},
            "task_run_id": str(mock_task_run_id),
            "timestamp": ANY,
            "message": "test_function succeeded.",
            "status": "SUCCEEDED",
        }

    @responses.activate
    def test_works_func_failed(self, mock_task_run_id):
        requests_made = responses.add(
            responses.POST,
            MOCK_WEBHOOK_URL,
            status=200,
        )

        mock_task_func(throw_error=True)

        assert requests_made.call_count == 2
        assert requests_made.calls[0].request.headers["Authorization"] == "Bearer api_key"

        assert json.loads(requests_made.calls[0].request.body or "{}") == {
            "event_type": "UPDATE_STATUS",
            "metadata": {},
            "task_run_id": str(mock_task_run_id),
            "timestamp": ANY,
            "message": "test_function started.",
            "status": "RUNNING",
        }
        assert json.loads(requests_made.calls[1].request.body or "{}") == {
            "event_type": "UPDATE_STATUS",
            "metadata": {},
            "task_run_id": str(mock_task_run_id),
            "timestamp": ANY,
            "message": "test_function failed. Error: ERROR IN YOUR FUNCTION!",
            "status": "FAILED",
        }
