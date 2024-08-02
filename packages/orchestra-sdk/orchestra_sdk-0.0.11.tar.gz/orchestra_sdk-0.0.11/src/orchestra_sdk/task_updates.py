import logging

from orchestra_sdk.enum import TaskRunStatus, WebhookEventType
from orchestra_sdk.http import orchestra_http_request
from orchestra_sdk.models import TaskRunWebhookModel

logger = logging.getLogger(__name__)


def _update_task(
    task_run_webhook: TaskRunWebhookModel,
    status: TaskRunStatus,
    message: str,
) -> None:
    logger.info(f"Updating {task_run_webhook} to {status.value.lower()}.")
    orchestra_http_request(
        event_type=WebhookEventType.UPDATE_STATUS,
        task_run_id=task_run_webhook.task_run_id,
        json={"status": status.value, "message": message},
        method="POST",
        url=task_run_webhook.webhook_url,
        api_key=task_run_webhook.api_key,
    )


def send_running_status(task_run_webhook: TaskRunWebhookModel | None, function_name: str) -> None:
    if task_run_webhook:
        _update_task(
            task_run_webhook=task_run_webhook,
            status=TaskRunStatus.RUNNING,
            message=f"{function_name} started.",
        )


def send_failed_status(
    task_run_webhook: TaskRunWebhookModel | None,
    function_name: str,
    func_error: Exception,
) -> None:
    if task_run_webhook:
        _update_task(
            task_run_webhook=task_run_webhook,
            status=TaskRunStatus.FAILED,
            message=f"{function_name} failed. Error: {str(func_error)[:250]}",
        )


def send_success_status(task_run_webhook: TaskRunWebhookModel | None, function_name: str) -> None:
    if task_run_webhook:
        _update_task(
            task_run_webhook=task_run_webhook,
            status=TaskRunStatus.SUCCEEDED,
            message=f"{function_name} succeeded.",
        )
