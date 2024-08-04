import asyncio
import logging
from asyncio import Semaphore
from typing import Callable, Dict, List, Union

import orjson
from serpapi_client.google.client import GoogleSearch

from ...fix import REDIS_NULL, SEARCH_TYPE_SEARCH, SEARCH_TYPE_SHOPPING, SEARCH_TYPES
from ...handler.local import MemoryStore
from ...metastore.redis import RedisMetastore
from ...model import TaskResult
from ...parser import serpapi_google_search_parser
from ...util import punch_date
from ..core import Explorer
from ..util import build_query, get_date_range

logger = logging.getLogger(__package__)


################################################################
# GoogleExplorer
################################################################
class GoogleSearchExplorer(Explorer):
    def __init__(
        self,
        serpapi_api_key: str,
        serpapi_rpm: int = 10,
        serpapi_gl: str = "us",
        start_days_ago: int = 360,
        max_search_days: int = 30,
        metastore: RedisMetastore = RedisMetastore(),
        max_concurrent_tasks: int = 10,
        parser: Callable = serpapi_google_search_parser,
        handler: Callable = MemoryStore(),
    ):
        super().__init__(
            search_type="search",
            start_days_ago=start_days_ago,
            max_search_days=max_search_days,
            metastore=metastore,
            max_concurrent_tasks=max_concurrent_tasks,
        )

        self.google = GoogleSearch(api_key=serpapi_api_key, gl=serpapi_gl, rpm=serpapi_rpm)
        self.parser = parser
        self.handler = handler

    async def _handler(self, page):
        records = self.parser(page)
        await self.handler(records)

    ################################################################
    # Search Explorer
    ################################################################
    async def search(
        self,
        name: str,
        query: str,
        location: str,
        site: str = None,
        after: str = None,
        before: str = None,
    ):
        try:
            # search
            q = build_query(query=query, site=site, after=after, before=before)
            logger.info("Executing search for task %s with query: %s", name, q)
            pages = await self.google.search(q=q, location=location)

            # page handler (update target link)
            hit = 0
            log = f"No results for this query. ({q})"
            if pages:
                coros = [self.page_handler(page=page) for page in pages]
                list_targets = await asyncio.gather(*coros)
                for targets in list_targets:
                    hit += len(targets)
                log = orjson.dumps(pages[-1])
                logger.info("Search for task %s returned %d pages with a total of %d hits", name, len(pages), hit)

            return TaskResult(name=name, after=after, before=before, success=True, hit=hit, log=log)
        finally:
            self.semaphore.release()

    async def page_handler(self, page: List[Dict]):
        await self._handler(page)
        targets = list()
        for results_type, results in page.items():
            if results_type in ["organic_results"]:
                targets += self.metastore.upsert_scraper_targets_from_search_results(
                    results_type=results_type, search_results=results
                )
        return targets
