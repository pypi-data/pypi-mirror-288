import asyncio
import logging
from asyncio import Semaphore

import parse

from ..metastore.redis import RedisMetastore
from ..model import TaskResult

logger = logging.getLogger(__package__)


################################################################
# Scraper
################################################################
class Scraper:
    def __init__(
        self,
        scraper_name: str,
        target_domain: str,
        metastore: RedisMetastore = RedisMetastore(),
        max_concurrent_tasks: int = 10,
    ):
        self.scraper_name = scraper_name
        self.target_domain = target_domain
        self.metastore = metastore

        self.semaphore = Semaphore(max_concurrent_tasks)
        self.loop = asyncio.get_event_loop()

        self.tasks = list()

    async def start_scraper(self):
        try:
            while True:
                jobs = self.metastore.get_scraper_jobs_to_execute(
                    scraper_name=self.scraper_name, target_domain=self.target_domain
                )
                logger.info("Retrieved %d jobs to execute", len(jobs))

                # submit jobs
                for job in jobs:
                    # get scraper for job
                    scraper = self.metastore.get_scraper_scraper_by_name(job.scraper)

                    # check link pattern
                    if not self._is_target_pattern(patterns=scraper.target_patterns, link=job.link):
                        continue

                    # get scrape function
                    scrape_func = getattr(self, scraper.api_endpoint or "nothing", None)
                    if not scrape_func:
                        logger.warning("No method name '{scraper.api_endpoint}'!")
                        continue

                    # get parameter for scrape function
                    params = dict()
                    for parameter in scraper.api_params:
                        value = getattr(job, parameter)
                        if not value:
                            logger.warning("No endpoint '{scraper.api_endpoint}'!")
                            continue
                        params.update({parameter: value})

                    # submit job
                    logger.info("Submit '%s'", job.name)
                    await self.semaphore.acquire()
                    task = self.loop.create_task(self.run_task(scrape_func, job.name, **params), name=job.name)
                    self.tasks.append(task)

                    # manage tasks & sleep
                    await self.cleanup_tasks()
                    await asyncio.sleep(1.0)

        except KeyboardInterrupt:
            logger.warning("Keyboard interrupted!")

        except Exception as ex:
            logger.error("An unexpected error occurred: %s", ex, exc_info=True)

        finally:
            logger.warning("Waiting all tasks are done before exit...")
            await asyncio.gather(*self.tasks, return_exceptions=True)
            await self.cleanup_tasks()
            logger.warning("All tasks are done. Exit!")

    async def run_task(self, scrape_func, name, **params):
        try:
            return await scrape_func(name=name, **params)
        finally:
            self.semaphore.release()

    async def cleanup_tasks(self):
        tasks = []
        for task in self.tasks:
            if task.done():
                if task.exception():
                    name = task.get_name()
                    log = task.exception().__repr__()
                    task_result = TaskResult(name=name, success=False, hit=0, log=log)
                    self.metastore.update_scraper_job_from_task_results(task_result)
                    logger.info("FAILED '%s' (%s)", name, log)
                else:
                    result = task.result()
                    self.metastore.update_scraper_job_from_task_results(result)
                    logger.info("Finish '%s'", result.name)
            else:
                tasks.append(task)
        self.tasks = tasks

    @staticmethod
    def _is_target_pattern(patterns: list, link: str):
        if not patterns:
            return True
        for pattern in patterns:
            parsed = parse.compile(pattern).parse(link)
            if parsed:
                return True
        return False
