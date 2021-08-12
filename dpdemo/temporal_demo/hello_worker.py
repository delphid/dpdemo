import asyncio
import logging
from datetime import timedelta
import os

import fire
from temporal.activity_method import activity_method, ActivityOptions
from temporal.workerfactory import WorkerFactory
from temporal.workflow import workflow_method, Workflow, WorkflowClient

logging.basicConfig(level=logging.INFO)

TASK_QUEUE_BASE = "HelloWorld"
TASK_QUEUE = TASK_QUEUE_BASE + str(os.getenv('tqn'))
NAMESPACE = "default"


# Activities Interface
class GreetingActivities:
    @activity_method(task_queue=TASK_QUEUE, schedule_to_close_timeout=timedelta(seconds=60))
    async def compose_greeting(self, greeting: str, name: str) -> str:
        raise NotImplementedError


# Activities Implementation
class GreetingActivitiesImpl:
    async def compose_greeting(self, greeting: str, name: str) -> str:
        return greeting + " " + name


# Workflow Interface
class GreetingWorkflow:
    @workflow_method(task_queue=TASK_QUEUE)
    async def get_greeting(self, name: str) -> str:
        raise NotImplementedError


# Workflow Implementation
class GreetingWorkflowImpl(GreetingWorkflow):

    def __init__(self):
        activity_options = ActivityOptions(task_queue=TASK_QUEUE)
        self.greeting_activities: GreetingActivities = Workflow.new_activity_stub(
            GreetingActivities, activity_options=activity_options)

    async def get_greeting(self, name):
        results = []
        for task_queue_no in range(3):
            task_queue_no = str(task_queue_no)
            activity_options = ActivityOptions(task_queue=TASK_QUEUE_BASE + task_queue_no)
            activities = Workflow.new_activity_stub(
                GreetingActivities, activity_options=activity_options)
            result = await activities.compose_greeting("Hello!", name + task_queue_no)
            results.append(result)
        return results


async def worker_main():
    client = WorkflowClient.new_client(namespace=NAMESPACE)
    factory = WorkerFactory(client, NAMESPACE)
    worker = factory.new_worker(TASK_QUEUE)
    worker.register_activities_implementation(GreetingActivitiesImpl(), "GreetingActivities")
    worker.register_workflow_implementation_type(GreetingWorkflowImpl)
    factory.start()
    print("Worker started")


def run():
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(worker_main())
    loop.run_forever()


if __name__ == '__main__':
    fire.Fire({
        'run': run
    })
