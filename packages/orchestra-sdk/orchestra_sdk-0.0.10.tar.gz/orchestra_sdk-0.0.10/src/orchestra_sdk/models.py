from dataclasses import dataclass
from uuid import UUID


@dataclass
class TaskRunWebhookModel:
    api_key: str
    webhook_url: str
    task_run_id: UUID
    pipeline_run_id: UUID

    def __str__(self):
        return f"(task_run_id={self.task_run_id}, pipeline_run_id={self.pipeline_run_id})"
