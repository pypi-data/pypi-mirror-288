import logging
import os
import uuid

from orchestra_sdk.errors import (
    MissingEnvironmentKeysError,
    NoEnvironmentVariablesFoundError,
)
from orchestra_sdk.models import TaskRunWebhookModel
from orchestra_sdk.task_updates import (
    send_failed_status,
    send_running_status,
    send_success_status,
)

logger = logging.getLogger(__name__)


def _check_env_vars(env_keys: list[str], env_vars: os._Environ[str] | None) -> None:
    if env_vars is None or len(env_vars) == 0:
        raise NoEnvironmentVariablesFoundError

    missing_keys = set()

    for key in env_keys:
        if key not in env_vars:
            missing_keys.add(key)

    if missing_keys:
        raise MissingEnvironmentKeysError(missing_keys)


def orchestra_run(func):
    def wrapper(*args, **kwargs):
        env_keys = [
            "orchestra_api_key",
            "orchestra_pipeline_run_id",
            "orchestra_task_run_id",
            "orchestra_webhook_url",
        ]
        env_vars = None
        task_run_webhook = None

        try:
            # Read webhook_url, task_run_id, pipeline_run_id from the environment
            env_vars = os.environ
            # Validate the environment variables
            _check_env_vars(env_keys, env_vars)
            # Create the model
            task_run_webhook = TaskRunWebhookModel(
                api_key=env_vars["orchestra_api_key"],
                webhook_url=env_vars["orchestra_webhook_url"],
                task_run_id=uuid.UUID(env_vars["orchestra_task_run_id"]),
                pipeline_run_id=uuid.UUID(env_vars["orchestra_pipeline_run_id"]),
            )
        except MissingEnvironmentKeysError as e:
            logger.error(f"Missing environment variables: {', '.join(e.missing_keys)}")
        except NoEnvironmentVariablesFoundError:
            logger.error("No environment variables loaded")
        except Exception as e:
            logger.error(f"Error processing environment variables: {e}")

        send_running_status(task_run_webhook, func.__name__)

        try:
            func(*args, **kwargs)
            send_success_status(task_run_webhook, func.__name__)
        except Exception as failed_func_err:
            send_failed_status(task_run_webhook, func.__name__, failed_func_err)

    return wrapper
