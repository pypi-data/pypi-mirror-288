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

There are also optional configuration values:

- `send_logs`: send the contents of a log file to Orchestra associated with the task (default = False)
- `log_file_path`: the path to the log file to send to Orchestra (default = "orchestra.log")

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

1. The decorator will firstly read and validate the environment variables
1. It will send a `RUNNING` status update to Orchestra
1. Your function will then run
1. If an exception is raised, the decorator will send a `FAILED` status update to Orchestra
1. If the function finishes without an error being raised, regardless of the return value, the decorator will send a `SUCCEEDED` status update to Orchestra
1. If `send_logs` is enabled, the contents of the logs will also be sent.

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

- At least one of `status` or `message` must be provided
- If the function fails or throws an exception, Orchestra might not register that the Task has failed, which could have downstream consequences on your pipeline. Consider wrapping your function in a try/except block and calling `update_task` with `status=TaskRunStatus.FAILED` in the except block.

## Sending logs

To send logs associated to the Task, enable the `send_logs` flag when initialising the `OrchestraSDK` class. The logs will be sent to Orchestra when the Task finishes and the decorator is being used.

An example logging configuration is shown below:

```python
import logging

from orchestra_sdk.orchestra import OrchestraSDK

orchestra = OrchestraSDK(
    api_key="your_api_key",
    send_logs=True,
    log_file="a.log"
)

def test_function():
    # Setup logging configuration
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # File handler
    file_handler = logging.FileHandler("a.log")
    file_handler.setLevel(logging.INFO)

    # Adding handlers to the logger
    logger.addHandler(file_handler)

    logger.info("Hello, World!")
```
