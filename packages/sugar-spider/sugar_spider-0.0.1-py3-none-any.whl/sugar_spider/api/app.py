import os
from typing import List

from fastapi import APIRouter, FastAPI

from ..metastore.redis import RedisMetastore
from .input_model import Location, Query, ScraperScraper, Site

################################################################
# Explorer
################################################################
explorer_router = APIRouter()


################################
# Query
################################
@explorer_router.post("/{search_type}/query")
async def add_query(search_type: str, queries: List[Query]):
    result = await metastore.add_explorer_queries(search_type, *[q.query for q in queries])
    return {"status": "success", "result": result}


@explorer_router.delete("/{search_type}/query")
async def delete_query(search_type: str, query: str):
    result = await metastore.delete_explorer_queries(search_type, query)
    return {"status": "success", "deleted_count": result}


@explorer_router.get("/{search_type}/queries")
async def list_queries(search_type: str):
    result = await metastore.list_explorer_query_names(search_type)
    return {"status": "success", "result": result}


################################
# Site
################################
@explorer_router.post("/{search_type}/site")
async def add_site(search_type: str, sites: List[Site]):
    result = await metastore.add_explorer_sites(search_type, *[site.site for site in sites])
    return {"status": "success", "result": result}


@explorer_router.delete("/{search_type}/site")
async def delete_site(search_type: str, site: str):
    result = await metastore.delete_explorer_sites(search_type, site)
    return {"status": "success", "deleted_count": result}


@explorer_router.get("/{search_type}/sites")
async def list_sites(search_type: str):
    result = await metastore.list_explorer_site_names(search_type)
    return {"status": "success", "result": result}


################################
# Location
################################
@explorer_router.post("/{search_type}/location")
async def add_location(search_type: str, locations: List[Location]):
    result = await metastore.add_explorer_locations(search_type, *[location.location for location in locations])
    return {"status": "success", "result": result}


@explorer_router.delete("/{search_type}/location")
async def delete_location(search_type: str, location: str):
    result = await metastore.delete_explorer_locations(search_type, location)
    return {"status": "success", "deleted_count": result}


@explorer_router.get("/{search_type}/locations")
async def list_locations(search_type: str):
    result = await metastore.list_explorer_location_names(search_type)
    return {"status": "success", "result": result}


################################
# Job
################################
@explorer_router.get("/{search_type}/jobs")
async def list_jobs(search_type: str, site: str = "*", location: str = "*", interval_days: str = None):
    result = await metastore.get_explorer_jobs(
        search_type=search_type, site=site, location=location, interval_days=interval_days
    )
    return {"status": "success", "result": result}


################################################################
# Scraper
################################################################
scraper_router = APIRouter()


################################
# Scraper
################################
@scraper_router.post("/scraper")
async def upsert_scraper(scrapers: List[ScraperScraper]):
    for scraper in scrapers:
        result = await metastore.upsert_scraper_scraper(**scraper.dict())
    return {"status": "success", "result": result}


@scraper_router.delete("/scraper")
async def delete_scraper(scraper_name: str, target_domain: str):
    result = await metastore.delete_scraper_scraper(scraper_name=scraper_name, target_domain=target_domain)
    return {"status": "success", "deleted_count": result}


@scraper_router.get("/scrapers")
async def list_scraper(scraper_type: str = "*", scraper_name="*", target_domain="*"):
    result = await metastore.get_scraper_scrapers(
        scraper_type=scraper_type, scraper_name=scraper_name, target_domain=target_domain
    )
    return {"status": "success", "result": result}


################################################################
# App
################################################################
app = FastAPI()

print("redis_host", os.getenv("REDIS_HOST"))
metastore = RedisMetastore()

app.include_router(explorer_router, prefix="/explorer", tags=["explorer"])
app.include_router(scraper_router, prefix="/scraper", tags=["scraper"])
