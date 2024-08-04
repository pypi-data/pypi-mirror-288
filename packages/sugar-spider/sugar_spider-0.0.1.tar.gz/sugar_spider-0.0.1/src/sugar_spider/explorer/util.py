import logging
from typing import Callable, Dict, List, Union

from ..fix import REDIS_NULL
from ..util import punch_date

logger = logging.getLogger(__package__)


################################################################
# Helper
################################################################
def get_date_range(last_before: str, start_days_ago: int, max_search_days: int) -> Dict[str, Union[str, None]]:
    if not start_days_ago:
        return {"after": None, "before": None}

    # start_days_ago 이전까지는 일괄 검색
    if not last_before:
        return {"after": None, "before": punch_date(offset_days=-start_days_ago)}

    # start_days_ago 이후부터는 max_search_days만큼 전진하며 검색
    after = last_before
    before = punch_date(reference_date=last_before, offset_days=max_search_days - 1)
    today = punch_date()
    if before > today:
        before = today
    return {"after": after, "before": before}


def build_query(query: str, site: str = None, after: str = None, before: str = None) -> str:
    if site and site != REDIS_NULL:
        query += f" site:{site}"
    if after:
        query += f" after:{after}"
    if before:
        query += f" before:{before}"
    return query
