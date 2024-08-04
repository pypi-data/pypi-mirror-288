import asyncio
import logging
from types import CoroutineType
from typing import Callable

import orjson
from serpapi_client.google.client import GoogleSearch

from ...fix import REDIS_NULL
from ...handler.local import MemoryStore
from ...metastore.redis import RedisMetastore
from ...model import TaskResult
from ...parser import serpapi_google_search_parser
from ...util import punch_date
from ..core import Scraper

logger = logging.getLogger(__package__)

TARGET_DOMAIN = "shopping.google.com"


class GoogleProductScraper(Scraper):
    def __init__(
        self,
        serpapi_api_key: str,
        serpapi_rpm: int = 10,
        gl: str = "us",
        scraper_name: str = "*",
        target_domain: str = TARGET_DOMAIN,
        metastore: RedisMetastore = RedisMetastore(),
        parser: Callable = serpapi_google_search_parser,
        handler: CoroutineType = MemoryStore(),
        max_concurrent_tasks: int = 10,
    ):
        super().__init__(
            scraper_name=scraper_name,
            target_domain=target_domain,
            metastore=metastore,
            max_concurrent_tasks=max_concurrent_tasks,
        )

        self.gl = gl
        self.rpm = serpapi_rpm
        self.parser = parser
        self.handler = handler
        self.google = GoogleSearch(api_key=serpapi_api_key, gl=self.gl, rpm=self.rpm)

        self.tasks = list()

        logger.info("GoogleProductScraper initialized")

    async def _handler(self, page):
        records = self.parser(page)
        await self.handler(records)

    async def _scrape(self, name: str, product_id: str, fetch_func: Callable, results_type: str, hit_func: Callable):
        pages = await fetch_func(product_id=product_id)
        if not pages:
            return self._no_results(name=name, product_id=product_id)

        hit = 0
        log = REDIS_NULL
        for page in pages:
            await self._handler(page)
            results = page.get(results_type)
            if results:
                hit += hit_func(results)
                log = orjson.dumps(results)

        return TaskResult(name=name, after=REDIS_NULL, before=punch_date(), success=True, hit=hit, log=log)

    async def scrape_product_page(self, name: str, product_id: str):
        return await self._scrape(
            name=name,
            product_id=product_id,
            fetch_func=self.google.product_page,
            results_type="product_results",
            hit_func=lambda results: 1,
        )

    async def scrape_product_offers(self, name: str, product_id: str):
        return await self._scrape(
            name=name,
            product_id=product_id,
            fetch_func=self.google.product_offers,
            results_type="sellers_results",
            hit_func=lambda results: len(results.get("online_sellers", [])),
        )

    async def scrape_product_specs(self, name: str, product_id: str):
        return await self._scrape(
            name=name,
            product_id=product_id,
            fetch_func=self.google.product_specs,
            results_type="specs_results",
            hit_func=lambda results: 1,
        )

    async def scrape_product_reviews(self, name: str, product_id: str):
        return await self._scrape(
            name=name,
            product_id=product_id,
            fetch_func=self.google.product_reviews,
            results_type="reviews_results",
            hit_func=lambda results: len(results.get("reviews", [])),
        )

    @staticmethod
    def _no_results(name: str, product_id: str):
        return TaskResult(
            name=name,
            after=REDIS_NULL,
            before=punch_date(),
            success=False,
            hit=0,
            log=f"No results for product_id '{product_id}'!",
        )
