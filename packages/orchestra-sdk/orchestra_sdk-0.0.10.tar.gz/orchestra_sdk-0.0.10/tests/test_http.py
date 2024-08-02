import json
import uuid
from unittest.mock import ANY

import responses

from src.orchestra_sdk.enum import WebhookEventType
from src.orchestra_sdk.http import orchestra_http_request


@responses.activate
def test_retry_mechanism_works():
    mock_url = "http://mock.url"
    mock_task_run_id = uuid.uuid4()

    responses.post(mock_url, status=503)
    responses.post(mock_url, status=500)
    r3 = responses.post(mock_url, status=200, json={"result": "all good"})

    orchestra_http_request(
        url=mock_url,
        api_key="mock_api_key",
        event_type=WebhookEventType.UPDATE_STATUS,
        task_run_id=mock_task_run_id,
    )

    assert len(responses.calls) == 3
    assert json.loads(r3.calls[0].request.body or "{}") == {
        "event_type": "UPDATE_STATUS",
        "metadata": {},
        "task_run_id": str(mock_task_run_id),
        "timestamp": ANY,
    }
