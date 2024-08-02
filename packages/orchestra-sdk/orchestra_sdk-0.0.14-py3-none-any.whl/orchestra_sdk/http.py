import logging
from datetime import datetime
from typing import Any, Literal
from uuid import UUID

import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from orchestra_sdk.enum import WebhookEventType

logger = logging.getLogger(__name__)


def _get_response_json(r: requests.Response) -> dict | None:
    try:
        return r.json()
    except Exception:
        return None


@retry(
    reraise=True,
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=3, min=2, max=15),
)
def _make_request(
    json: dict[str, Any], headers: dict[str, str], method: Literal["POST"], url: str
) -> None:
    logger.info(f"Sending request to {url}...")
    r = requests.request(json=json, method=method, url=url, headers=headers)
    logger.info(f"Status: {r.status_code}. Response: {_get_response_json(r)}")
    r.raise_for_status()


def orchestra_http_request(
    url: str,
    api_key: str,
    event_type: WebhookEventType,
    task_run_id: UUID,
    metadata: dict[str, Any] = {},
    json: dict[str, Any] = {},
    method: Literal["POST"] = "POST",
):
    try:
        _make_request(
            json={
                "event_type": event_type.value,
                "metadata": metadata,
                "task_run_id": str(task_run_id),
                "timestamp": datetime.now().isoformat(),
                **json,
            },
            headers={"Authorization": f"Bearer {api_key}"},
            method=method,
            url=url,
        )
    except requests.exceptions.HTTPError as e:
        logger.error(f"Failed request ({e.response.status_code}): {_get_response_json(e.response)}")
    except Exception as e:
        logger.error(f"Could not send {method} request to {url} with JSON: {json} - {e}")
