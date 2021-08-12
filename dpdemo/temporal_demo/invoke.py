import asyncio
import os

import fire
from temporal.api.taskqueue.v1 import TaskQueue
from temporal.workflow import workflow_method, WorkflowClient, WorkflowOptions


NAMESPACE = "default"


async def invoke(wf_cls, task_queue, func_name, *args, **kwargs):
    client = WorkflowClient.new_client(namespace=NAMESPACE)
    workflow_options = WorkflowOptions(
        task_queue=TaskQueue(name=task_queue))
    wf = client.new_workflow_stub(
        wf_cls,
        workflow_options=workflow_options)
    print(getattr(wf, func_name))
    result = await getattr(wf, func_name)(*args, **kwargs)
    print("Workflow returned:", result)
    return result
