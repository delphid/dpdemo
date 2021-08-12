import asyncio
import logging
from datetime import timedelta
import os
import time

import fire
from temporal.activity_method import activity_method, ActivityOptions
from temporal.workerfactory import WorkerFactory
from temporal.workflow import workflow_method, Workflow, WorkflowClient

from invoke import invoke


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
        await asyncio.sleep(0.2)
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
            tasks = []
            for task_queue in task_queues:
                time0 = time.time()
                activity_options = ActivityOptions(task_queue=task_queue)
                activities = Workflow.new_activity_stub(
                    GreetingActivities, activity_options=activity_options)
                print(f'activities newed and start wait in {task_queue}')
                result = await activities.compose_greeting("Hello!", f'{name} from task_queue: {task_queue}')
                results.append(result)
                time.sleep(0.2)
                print(f'stop wait in {task_queue}, last {time.time() - time0} s')
            return results
    return GreetingWorkflowImpl


async def worker_main(task_queue=None):
    client = WorkflowClient.new_client(namespace=NAMESPACE)
    factory = WorkerFactory(client, NAMESPACE)
    worker = factory.new_worker(task_queue)
    worker.register_activities_implementation(GreetingActivitiesImpl(), "GreetingActivities")
    impl_queues = {
        'all': ['q1_all', 'q2_all'],
        'q1': ['q1'],
        'q2': ['q2'],
        'q1_all': ['q1_all', 'q2_all'],
        'q2_all': ['q1_all', 'q2_all']}
    GreetingWorkflowImpl = create_wf_impl_class(impl_queues[task_queue])
    worker.register_workflow_implementation_type(GreetingWorkflowImpl)
    factory.start()
    print("Worker started")


def worker(task_queue=None):
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(worker_main(task_queue=task_queue))
    loop.run_forever()


def run(task_queue, name):
    result = asyncio.run(
        invoke(
            GreetingWorkflow,
            task_queue,
            'get_greeting',
            name))
    return result


if __name__ == '__main__':
    fire.Fire({
        'worker': worker,
        'run': run
    })
