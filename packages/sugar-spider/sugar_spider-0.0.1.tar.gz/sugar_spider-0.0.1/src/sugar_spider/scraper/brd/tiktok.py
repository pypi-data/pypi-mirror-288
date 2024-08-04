import asyncio
import logging
from types import CoroutineType
from typing import Callable

import orjson
from brd_client.scraper_api.social_media.tiktok import TikTok

from ...fix import REDIS_NULL
from ...handler.local import MemoryStore
from ...metastore.redis import RedisMetastore
from ...model import TaskResult
from ...parser import brd_scraper_api_parser
from ...util import punch_date
from ..core import Scraper

logger = logging.getLogger(__package__)

TARGET_DOMAIN = "www.tiktok.com"


class TikTokScraper(Scraper):
    def __init__(
        self,
        brd_api_token: str,
        scraper_name: str = "*",
        target_domain: str = TARGET_DOMAIN,
        metastore: RedisMetastore = RedisMetastore,
        parser: Callable = brd_scraper_api_parser,
        handler: CoroutineType = MemoryStore(),
        max_concurrent_tasks: int = 10,
    ):
        super().__init__(
            target_domain=target_domain,
            scraper_name=scraper_name,
            metastore=metastore,
            max_concurrent_tasks=max_concurrent_tasks,
        )

        self.parser = parser
        self.handler = handler
        self.client = TikTok(api_token=brd_api_token)

        self.tasks = list()

        logger.info("TikTok initialized")

    async def _handler(self, key, results):
        records = self.parser(key, results)
        await self.handler(records)

    async def scrape_posts_and_profiles(self, name: str, link: str):
        # get posts
        results = await self.client.posts(link)
        log = orjson.dumps(results)
        await self._handler(key="tiktok/posts", results=results)

        # get profile
        profile_urls, coros = list(), list()
        for result in results:
            profile_url = result.get("profile_url")
            if profile_url:
                profile_urls.append(profile_url)
                coros.append(self.client.profiles(profile_url))

        list_results = await asyncio.gather(*coros, return_exceptions=True)
        for profile_url, results in zip(profile_urls, list_results):
            if isinstance(results, Exception):
                logger.warning("Fail scraping user profile: %s (%s)", profile_url, results.__repr__())
                continue
            await self._handler(key="tiktok/profiles", results=results)

        return TaskResult(name=name, after=REDIS_NULL, before=punch_date(), success=True, hit=1, log=log)

    async def scrape_comments(self, name: str, link: str):
        results = await self.client.comments(link)
        log = orjson.dumps(results)
        await self._handler(key="tiktok/comments", results=results)
        return TaskResult(name=name, after=REDIS_NULL, before=punch_date(), success=True, hit=1, log=log)
