import logging

import pendulum
from pydantic import BaseModel

from .util import punch_datetime

logger = logging.getLogger(__package__)

TZ = pendulum.timezone("Asia/Seoul")


################################################################
# Explorer
################################################################
class ExplorerItem(BaseModel):
    registered_at: str = punch_datetime()


# Query
class Query(ExplorerItem):
    query: str


# Site
class Site(ExplorerItem):
    site: str


# Location
class Location(ExplorerItem):
    location: str


################################################################
# Scraper
################################################################
class ScraperItem(BaseModel):
    name: str
    registered_at: str = punch_datetime()


# ScraperTarget
class ScraperTarget(ScraperItem):
    domain: str
    id: str
    results_type: str
    title: str
    link: str
    product_id: str = None
    product_link: str = None
    source: str = None
    rating: float = 0.0
    reviews: int = 0
    total_hit: int = 0


# ScraperScraper
class ScraperScraper(ScraperItem):
    scraper_name: str
    target_domain: str
    target_patterns: list = None
    api_endpoint: str = None
    api_params: list = None
    default_interval_days: int = 7


################################################################
# Job
################################################################
class Job(BaseModel):
    name: str
    registered_at: str = punch_datetime()
    executed_at: str = None
    succeeded_at: str = None
    last_after: str = None
    last_before: str = None
    last_hit: int = 0
    last_log: str = None
    total_run: int = 0
    total_success: int = 0
    total_hit: int = 0
    interval_days: int
    active: bool = True


# ExplorerJob
class ExplorerJob(Job):
    query: str
    site: str
    location: str
    interval_days: int = 1


# ScraperJob
class ScraperJob(Job):
    title: str
    link: str
    product_id: str = None
    product_link: str = None
    source: str = None
    scraper: str


################################################################
# TaskResult
################################################################
class TaskResult(BaseModel):
    name: str
    after: str = None
    before: str = None
    success: bool = None
    hit: int = 0
    log: str = None
