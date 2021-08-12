import asyncio
import os

import fire

from temporal.workflow import workflow_method, WorkflowClient


NAMESPACE = "default"


def create_wf_class(task_queue):
    class GreetingWorkflow:
        @workflow_method(task_queue=task_queue)
        async def get_greeting(self, name: str) -> str:
            raise NotImplementedError
    return GreetingWorkflow


async def main(task_queue, name):
    GreetingWorkflow = create_wf_class(task_queue)
    client = WorkflowClient.new_client(namespace=NAMESPACE)
    greeting_workflow: GreetingWorkflow = client.new_workflow_stub(GreetingWorkflow)
    result = await greeting_workflow.get_greeting(name)
    print("Workflow returned:", result)


def run(task_queue, name):
    asyncio.run(main(task_queue, name))


if __name__ == '__main__':
    fire.Fire({
        'run': run
    })
