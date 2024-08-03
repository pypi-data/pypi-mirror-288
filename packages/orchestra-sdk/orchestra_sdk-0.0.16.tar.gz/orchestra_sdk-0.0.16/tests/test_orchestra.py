import json
import logging
import uuid
from unittest.mock import ANY

import pytest
import responses
from orchestra_sdk.enum import TaskRunStatus
from orchestra_sdk.orchestra import OrchestraSDK

logger = logging.getLogger(__name__)

MOCK_API_KEY = "mock_api_key"
MOCK_WEBHOOK_URL = "http://orchestra-webhook-123.com/update"


class TestOrchestraSDK:
    @pytest.fixture
    def mock_task_run_id(self):
        return uuid.uuid4()

    @pytest.fixture
    def test_instance(self, mocker, mock_task_run_id) -> OrchestraSDK:
        mocker.patch.dict(
            "os.environ",
            {
                "ORCHESTRA_WEBHOOK_URL": MOCK_WEBHOOK_URL,
                "ORCHESTRA_TASK_RUN_ID": str(mock_task_run_id),
            },
        )
        return OrchestraSDK(api_key=MOCK_API_KEY)

    @responses.activate
    def test_webhook_non_200(self, caplog, test_instance: OrchestraSDK):
        @test_instance.run()
        def test_function():
            logger.info("A")

        responses.add(
            responses.POST,
            MOCK_WEBHOOK_URL,
            status=404,
            json={"error": "Could not find API"},
        )

        with caplog.at_level(logging.ERROR):
            test_function()

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
    def test_works_func_succeeded(self, mock_task_run_id, test_instance: OrchestraSDK):
        @test_instance.run()
        def test_function():
            logger.info("A")

        requests_made = responses.add(
            responses.POST,
            MOCK_WEBHOOK_URL,
            status=200,
        )

        test_function()

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
    def test_works_func_failed(self, mock_task_run_id, test_instance: OrchestraSDK):
        @test_instance.run()
        def test_function():
            raise Exception("ERROR IN YOUR FUNCTION!")

        requests_made = responses.add(
            responses.POST,
            MOCK_WEBHOOK_URL,
            status=200,
        )

        test_function()

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
            "message": "test_function failed. Error: ERROR IN YOUR FUNCTION!",
            "status": "FAILED",
        }

    def test_orchestra_update_task_no_args_provided(self, caplog, test_instance: OrchestraSDK):
        with caplog.at_level(logging.WARNING):
            assert test_instance.update_task() is False
        assert caplog.record_tuples == [
            (
                "orchestra_sdk.orchestra",
                30,
                "No status or message provided for updating the Task. No update will be sent.",
            )
        ]

    def test_orchestra_update_task_invalid_env(self):
        o = OrchestraSDK(api_key="test")
        assert o.update_task(status=TaskRunStatus.FAILED) is False

    @responses.activate
    def test_update_task_success(self, test_instance: OrchestraSDK):
        mock_request = responses.post(test_instance.webhook_url, status=200)
        assert test_instance.update_task(status=TaskRunStatus.SUCCEEDED)
        assert json.loads(mock_request.calls[0].request.body or "{}") == {
            "event_type": "UPDATE_STATUS",
            "metadata": {},
            "status": "SUCCEEDED",
            "task_run_id": str(test_instance.task_run_id),
            "timestamp": ANY,
        }
