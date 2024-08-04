import asyncio
import logging
from types import CoroutineType
from typing import Callable

import orjson
from brd_client.scraper_api.social_media.instagram import Instagram

from ...fix import REDIS_NULL
from ...handler.local import MemoryStore
from ...metastore.redis import RedisMetastore
from ...model import TaskResult
from ...parser import brd_scraper_api_parser
from ...util import punch_date
from ..core import Scraper

logger = logging.getLogger(__package__)

TARGET_DOMAIN = "www.reddit.com"


class RedditScraper(Scraper):
    def __init__(
        self,
        scraper_name: str,
        brd_api_token: str,
        target_domain: str = TARGET_DOMAIN,
        metastore: RedisMetastore = RedisMetastore(),
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
        self.client = Instagram(api_token=brd_api_token)

        self.tasks = list()

        logger.info("InstagramScraper initialized")

    async def _handler(self, key, results):
        records = self.parser(key, results)
        await self.handler(records)

    async def scrape_posts(self, name: str, link: str):
        # get posts
        results = await self.client.posts(link)
        log = orjson.dumps(results)
        await self._handler(key="reddit/posts", results=results)

        # get profile
        users, coros = list(), list()
        for result in results:
            user = result.get("user_posted")
            if user:
                users.append(user)
                coros.append(self.client.profiles(f"https://www.instagram.com/{user}/"))

        list_results = await asyncio.gather(*coros, return_exceptions=True)
        for user, results in zip(users, list_results):
            if isinstance(results, Exception):
                logger.warning("Fail scraping user profile: %s", user)
                continue
            await self._handler(key="reddit/profiles", results=results)

        return TaskResult(name=name, after=REDIS_NULL, before=punch_date(), success=True, hit=1, log=log)

    async def scrape_comments(self, name: str, link: str):
        results = await self.client.comments(link)
        log = orjson.dumps(results)
        await self._handler(key="reddit/comments", results=results)
        return TaskResult(name=name, after=REDIS_NULL, before=punch_date(), success=True, hit=1, log=log)
