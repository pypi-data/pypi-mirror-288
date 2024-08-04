import logging
from typing import List

from serpapi_client.fix import GOOGLE_PAGINATION_ATTRS, SERPAPI_METADATA_ATTRS

logger = logging.getLogger(__package__)


class SugarSpiderParsingError(Exception):
    pass


def serpapi_google_search_parser(page: dict):
    metadata = {k: page.get(k) for k in SERPAPI_METADATA_ATTRS}

    records = list()
    for results_type, contents in page.items():
        try:
            if results_type in [*SERPAPI_METADATA_ATTRS, *GOOGLE_PAGINATION_ATTRS]:
                continue
            records.append({"key": results_type, "value": {**metadata, results_type: contents}})
        except Exception as ex:
            logger.warning()
            SugarSpiderParsingError(ex)

    return records


def brd_scraper_api_parser(key: str, records=List[dict]):
    return [{"key": key, "value": r} for r in records]
