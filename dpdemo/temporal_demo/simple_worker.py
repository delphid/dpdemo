import asyncio
import logging
from datetime import timedelta
import os

import fire
from temporal.activity_method import activity_method, ActivityOptions
from temporal.workerfactory import WorkerFactory
from temporal.workflow import workflow_method, Workflow, WorkflowClient

logging.basicConfig(level=logging.INFO)

NAMESPACE = "default"


# Activities Interface
class GreetingActivities:
    @activity_method(task_queue='random queue name', schedule_to_close_timeout=timedelta(seconds=60))
    async def compose_greeting(self, greeting: str, name: str) -> str:
        raise NotImplementedError


# Activities Implementation
class GreetingActivitiesImpl:
    async def compose_greeting(self, greeting: str, name: str) -> str:
        return greeting + " " + name


# Workflow Interface
class GreetingWorkflow:
    @workflow_method()
    async def get_greeting(self, name: str) -> str:
        raise NotImplementedError


def create_wf_impl_class(task_queues):
    class GreetingWorkflowImpl(GreetingWorkflow):

        async def get_greeting(self, name):
            results = []
            for task_queue in task_queues:
                activity_options = ActivityOptions(task_queue=task_queue)
                activities = Workflow.new_activity_stub(
                    GreetingActivities, activity_options=activity_options)
                result = await activities.compose_greeting("Hello!", f'{name} from task_queue: {task_queue}')
                results.append(result)
            return results
    return GreetingWorkflowImpl


async def worker_main(task_queue):
    client = WorkflowClient.new_client(namespace=NAMESPACE)
    factory = WorkerFactory(client, NAMESPACE)
    worker = factory.new_worker(task_queue)
    worker.register_activities_implementation(GreetingActivitiesImpl(), "GreetingActivities")
    GreetingWorkflowImpl = create_wf_impl_class(['q1', 'q2'])
    worker.register_workflow_implementation_type(GreetingWorkflowImpl)
    factory.start()
    print("Worker started")


def run(task_queue):
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(worker_main(task_queue))
    loop.run_forever()


if __name__ == '__main__':
    fire.Fire({
        'run': run
    })
