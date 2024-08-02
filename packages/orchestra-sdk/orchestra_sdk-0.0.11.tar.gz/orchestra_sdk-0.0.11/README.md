# Orchestra Python SDK

![PyPI](https://img.shields.io/pypi/v/orchestra-sdk?label=pypi%20latest%20version)

This is a lightweight SDK that allows [Orchestra](https://www.getorchestra.io/) to interact with self-hosted applications (Tasks).

The basic premise is for your self-hosted Task to send back status updates and logs to Orchestra. This is done via HTTP requests. The Task is started by Orchestra.

## Guide

Firstly, install the package:

```bash
pip install orchestra-sdk
```

The package requires the following environment variable to be set manually:

- `ORCHESTRA_API_KEY`: The API key to connect to Orchestra. This can be found in [your settings page](https://app.getorchestra.io/settings).

Orchestra will automatically set the following environment variables when the Task is triggered:

- `ORCHESTRA_WEBHOOK_URL`: The URL to send status updates to
- `ORCHESTRA_TASK_RUN_ID`: The UUID of the Task being executed
- `ORCHESTRA_PIPELINE_RUN_ID`: The UUID of the Pipeline Run that the Task is part of

To use the package in your code:

```python
from orchestra_sdk.decorators import orchestra_run

@orchestra_run()
def my_function(arg1, arg2=1):
    print("Running complex process")
```

### Summary

1. The decorator will firstly read and validate the environment variables
1. It will send a `RUNNING` status update to Orchestra
1. Your function will then run
1. If an exception is raised, the decorator will send a `FAILED` status update to Orchestra
1. If the function finishes without an error being raised, regardless of the return value, the decorator will send a `SUCCEEDED` status update to Orchestra
