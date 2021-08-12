import asyncio
import os

import fire

from temporal.workflow import workflow_method, WorkflowClient


TASK_QUEUE_BASE = "HelloWorld"
TASK_QUEUE = TASK_QUEUE_BASE + str(os.getenv('tqn'))
NAMESPACE = "default"


# Workflow Interface
class GreetingWorkflow:
    @workflow_method(task_queue=TASK_QUEUE)
    async def get_greeting(self, name: str) -> str:
        raise NotImplementedError


async def main():
    client = WorkflowClient.new_client(namespace=NAMESPACE)
    greeting_workflow: GreetingWorkflow = client.new_workflow_stub(GreetingWorkflow)
    result = await greeting_workflow.get_greeting("Bob")
    print("Workflow returned:", result)


def run():
    asyncio.run(main())


if __name__ == '__main__':
    fire.Fire({
        'run': run
    })
