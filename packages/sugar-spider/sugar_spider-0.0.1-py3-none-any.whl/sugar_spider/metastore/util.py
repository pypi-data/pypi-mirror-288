import logging
import urllib.parse

import parse

from .exception import InvalidPatternName

logger = logging.getLogger(__package__)

DELIM = ":"

EXPLORER_ITEM_NAME_RULE = DELIM.join(["explorer", "{search_type}", "{item_type}", "{id}"])

SCRAPER_TARGET_NAME_RULE = DELIM.join(["scraper", "target", "{results_type}", "{domain}", "{id}"])
SCRAPER_SCRAPER_NAME_RULE = DELIM.join(["scraper", "scraper", "{scraper_name}", "{target_domain}"])

JOB_FOR_EXPLORER_NAME_RULE = DELIM.join(["job", "explorer", "{search_type}", "{query}", "{site}", "{location}"])
JOB_FOR_SCRAPER_NAME_RULE = DELIM.join(["job", "scraper", "{scraper_name}", "{target_domain}", "{id}"])


################################################################
# Helper
################################################################
def split_domain_and_path_from_url(url: str):
    parsed = urllib.parse.urlparse(urllib.parse.unquote_plus(url))
    path = parsed.path if parsed.path else "__no path__"
    return parsed.netloc, path


def _parse_name(name: str, name_rule: str):
    p = parse.compile(name_rule)
    parsed = p.parse(name)
    if not parsed:
        raise InvalidPatternName(f"Target link name pattern is '{name_rule}', but '{name}'")
    return parsed.named


def correct_explorer_items(*items: str) -> list:
    # [NOTE] Google 검색 시 대소문자 차이 없음, 중복 쿼리 제거 위해 소문자로 변환
    corrected = list()
    for item in items:
        item = item.replace("  ", " ").lower()
        item = item.replace("https://", "").replace("http://", "")
        corrected.append(item)
    return corrected


################################################################
# Explorer
################################################################
def name_explorer_item(search_type: str, item_type: str, id=id):
    return EXPLORER_ITEM_NAME_RULE.format(search_type=search_type, item_type=item_type, id=id)


def parse_explorer_item_list(name: str):
    return _parse_name(name=name, name_rule=EXPLORER_ITEM_NAME_RULE)


################################################################
# Scraper
################################################################
# scraper target
def name_scraper_target(results_type: str, domain: str, id: str):
    return SCRAPER_TARGET_NAME_RULE.format(results_type=results_type, domain=domain, id=id)


def parse_scraper_target_name(name: str):
    return _parse_name(name=name, name_rule=SCRAPER_TARGET_NAME_RULE)


# scraper scraper
def name_scraper_scraper(scraper_name: str, target_domain: str):
    return SCRAPER_SCRAPER_NAME_RULE.format(scraper_name=scraper_name, target_domain=target_domain)


def parse_scraper_scraper_name(name: str):
    return _parse_name(name=name, name_rule=SCRAPER_SCRAPER_NAME_RULE)


################################################################
# Job
################################################################
# job for explorer
def name_job_for_explorer(search_type: str, site: str, query: str, location: str) -> str:
    return JOB_FOR_EXPLORER_NAME_RULE.format(search_type=search_type, query=query, site=site, location=location)


def parse_explorer_job_name(name: str):
    return _parse_name(name=name, name_rule=JOB_FOR_EXPLORER_NAME_RULE)


# job for scraper
def name_job_for_scraper(scraper_name: str, target_domain: str, id: str):
    return JOB_FOR_SCRAPER_NAME_RULE.format(scraper_name=scraper_name, target_domain=target_domain, id=id)


def parse_scraper_job_name(name: str):
    return _parse_name(name=name, name_rule=JOB_FOR_SCRAPER_NAME_RULE)
