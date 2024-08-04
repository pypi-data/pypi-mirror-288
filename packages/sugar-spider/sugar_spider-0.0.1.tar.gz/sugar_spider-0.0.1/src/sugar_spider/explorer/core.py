import asyncio
import logging
from asyncio import Semaphore
from typing import Callable, Dict, List, Union

from ..metastore.redis import RedisMetastore
from ..model import TaskResult
from .util import get_date_range

logger = logging.getLogger(__package__)


################################################################
# Explorer
################################################################
class Explorer:
    def __init__(
        self,
        search_type: str,
        start_days_ago: int,
        max_search_days: int,
        metastore: RedisMetastore = RedisMetastore(),
        max_concurrent_tasks: int = 10,
    ):
        self.search_type = search_type
        self.start_days_ago = start_days_ago
        self.max_search_days = max_search_days

        self.metastore = metastore
        self.semaphore = Semaphore(max_concurrent_tasks)
        self.loop = asyncio.get_event_loop()

        self.tasks = list()

    async def start_explorer(self):
        try:
            while True:
                jobs = self.metastore.get_explorer_jobs_to_execute(search_type=self.search_type)
                logger.info("Retrieved %d jobs to execute for search_type: %s", len(jobs), self.search_type)

                # submit jobs
                for job in jobs:
                    date_range = get_date_range(
                        last_before=job.last_before,
                        start_days_ago=self.start_days_ago,
                        max_search_days=self.max_search_days,
                    )

                    # submit job
                    logger.info("Submit '%s'", job.name)
                    await self.semaphore.acquire()
                    task = self.loop.create_task(
                        self.search(
                            name=job.name, query=job.query, site=job.site, **date_range, location=job.location
                        ),
                        name=job.name,
                    )
                    self.tasks.append(task)

                # manage tasks & sleep
                await self.cleanup_tasks()
                await asyncio.sleep(10.0)

        except KeyboardInterrupt:
            logger.warning("Keyboard interrupted!")

        except Exception as ex:
            logger.error("An error occurred: %s", str(ex))

        finally:
            logger.warning("Waiting all tasks are done...")
            await asyncio.gather(*self.tasks)
            await self.cleanup_tasks()
            logger.warning("All tasks are done. Exit.")

    async def cleanup_tasks(self):
        tasks = list()
        for task in self.tasks:
            if not task.done():
                tasks.append(task)
                continue
            if task.exception():
                task_result = TaskResult(name=task.get_name(), success=False, hit=0, log=task.exception().__repr__())
                self.metastore.update_explorer_job_from_task_results(task_result)
                logger.error("Task %s failed with exception: %s", task.get_name(), task.exception().__repr__())
                continue
            task_result = task.result()
            self.metastore.update_explorer_job_from_task_results(task_result)
            logger.info("Task %s completed successfully with %d hits", task_result.name, task_result.hit)
        self.tasks = tasks
