# Orchestra Python SDK

![PyPI](https://img.shields.io/pypi/v/orchestra-sdk?label=pypi%20latest%20version)

This is a lightweight SDK that allows [Orchestra](https://www.getorchestra.io/) to interact with self-hosted applications (Tasks).

The basic premise is for your self-hosted Task to send back status updates and logs to Orchestra. This is done via HTTP requests. The Task is started by Orchestra.

## Installation

```bash
pip install orchestra-sdk
```

You initialise the package by creating an instance of the `OrchestraSDK` class. It requires the API key that will connect with Orchestra - this can be found in [your settings page](https://app.getorchestra.io/settings). Orchestra will automatically set the other environment variables when the Task is triggered:

- `ORCHESTRA_WEBHOOK_URL`: The URL to send status updates to
- `ORCHESTRA_TASK_RUN_ID`: The UUID of the Task being executed

```python
from orchestra_sdk.orchestra import OrchestraSDK

orchestra = OrchestraSDK(api_key="your_api_key")
```

Orchestra recommends retrieving the API key from some secret store that you have configured. If that is not possible, you can set the API key as an environment variable and read that value in your code.

## Task decorator

The decorator will handle updating the Task in Orchestra automatically. It will send a `RUNNING` status update when the function is called, and then send a `SUCCEEDED` or `FAILED` status update when the function finishes.

```python
from orchestra_sdk.orchestra import OrchestraSDK

orchestra = OrchestraSDK(api_key="your_api_key")

@orchestra.run()
def my_function(arg1, arg2=1):
    print("Running complex process")
```

### Summary

1. The decorator will firstly read and validate the environment variables
1. It will send a `RUNNING` status update to Orchestra
1. Your function will then run
1. If an exception is raised, the decorator will send a `FAILED` status update to Orchestra
1. If the function finishes without an error being raised, regardless of the return value, the decorator will send a `SUCCEEDED` status update to Orchestra

## Updating Tasks manually

For additional control over when to update the status of the Task, or for sending messages to Orchestra, you can use the `update_task` method of the `OrchestraSDK` class.

```python
from orchestra_sdk.enum import TaskRunStatus
from orchestra_sdk.orchestra import OrchestraSDK

orchestra = OrchestraSDK(api_key="your_api_key")

def my_function(arg1, arg2=1):
    print("Start my complex process")
    orchestra.update_task(status=TaskRunStatus.RUNNING, message="Starting process.")

    print("Running complex process")
    orchestra.update_task(message="Running process.")

    fn_result = complex_process()

    if fn_result == 0:
        orchestra.update_task(status=TaskRunStatus.SUCCEEDED)
    else:
        orchestra.update_task(status=TaskRunStatus.FAILED, message="Process failed")
```

### Notes

- At least one of `status` or `message` must be provided
- If the function fails or throws an exception, Orchestra might not register that the Task has failed, which could have downstream consequences on your pipeline. Consider wrapping your function in a try/except block and calling `update_task` with `status=TaskRunStatus.FAILED` in the except block.
