from pydantic import BaseModel


class Query(BaseModel):
    query: str


class Site(BaseModel):
    site: str


class Location(BaseModel):
    location: str


class ScraperScraper(BaseModel):
    scraper_type: str
    scraper_name: str
    target_domain: str
    target_patterns: list = None
    api_endpoint: str = None
    api_params: list = None
    default_interval_days: int = 7
