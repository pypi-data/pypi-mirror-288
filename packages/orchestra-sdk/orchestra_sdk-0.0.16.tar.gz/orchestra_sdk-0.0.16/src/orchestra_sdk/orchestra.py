import logging
from functools import wraps

from orchestra_sdk.check_environment import validate_environment
from orchestra_sdk.enum import TaskRunStatus, WebhookEventType
from orchestra_sdk.http import HTTPClient

logger = logging.getLogger(__name__)


class OrchestraSDK:
    def __init__(self, api_key: str):
        env_values = validate_environment()
        self.task_run_id, self.webhook_url = env_values if env_values else (None, None)
        self.http_client = (
            HTTPClient(api_key=api_key, task_run_id=self.task_run_id, webhook_url=self.webhook_url)
            if self.task_run_id and self.webhook_url
            else None
        )

    def _update_task(self, status: TaskRunStatus, message: str) -> None:
        if self.http_client:
            logger.info(f"Updating '{self.task_run_id}' to {status.value.lower()}.")
            self.http_client.request(
                event_type=WebhookEventType.UPDATE_STATUS,
                json={"status": status.value, "message": message},
                method="POST",
            )

    def send_running_status(self, function_name: str) -> None:
        self._update_task(status=TaskRunStatus.RUNNING, message=f"{function_name} started.")

    def send_failed_status(self, function_name: str, func_error: Exception) -> None:
        self._update_task(
            status=TaskRunStatus.FAILED,
            message=f"{function_name} failed. Error: {str(func_error)[:250]}",
        )

    def send_success_status(self, function_name: str) -> None:
        self._update_task(status=TaskRunStatus.SUCCEEDED, message=f"{function_name} succeeded.")

    def run(self):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                self.send_running_status(func.__name__)
                try:
                    func(*args, **kwargs)
                    self.send_success_status(func.__name__)
                except Exception as failed_func_err:
                    self.send_failed_status(func.__name__, failed_func_err)

            return wrapper

        return decorator

    def update_task(self, status: TaskRunStatus | None = None, message: str | None = None) -> bool:
        """
        Update the Task with the provided status and message.

        Args:
            status (TaskRunStatus | None): The status to update the Task with.
            message (str | None): The message to update the Task with.

        Returns:
            bool: True if the Task updated request was sent successfully, False otherwise.
        """
        if not status and not message:
            logger.warning(
                "No status or message provided for updating the Task. No update will be sent."
            )
            return False

        if not self.http_client:
            logger.warning("Environment not configured correctly to send update for Task.")
            return False

        logger.info(
            f"Updating '{self.task_run_id}'. Status: {status.value.lower() if status else 'None'}. Message: {str(message)}."
        )

        payload = {}
        if status:
            payload["status"] = status.value
        if message:
            payload["message"] = message

        return self.http_client.request(
            event_type=WebhookEventType.UPDATE_STATUS,
            json=payload,
            method="POST",
        )
