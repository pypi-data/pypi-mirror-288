import asyncio
import logging

from plantable import BaseClient

from ..metastore.redis import RedisMetastore
from ..metastore.util import correct_explorer_items

logger = logging.getLogger(__package__)


class SeaTableMetadataSyncer:
    def __init__(
        self,
        seatable_url: str,
        seatable_api_token: str,
        metastore: RedisMetastore = RedisMetastore(),
        wait_for_sec: float = 600,
    ):
        self.run_every_sec = wait_for_sec
        self.metastore = metastore
        self.client = BaseClient(seatable_url=seatable_url, api_token=seatable_api_token)

    async def start_syncer(self):
        while True:
            await self.sync_explorer_items()
            await self.sync_scrapers()
            await asyncio.sleep(self.run_every_sec)

    async def sync_explorer_items(self):
        # add queries, sites, locations
        item_types = ["query", "site", "location"]
        # get items
        for item_type in item_types:
            # SeaTable's
            table = await self.client.read_table(item_type)
            grouped_items_in_seatable = dict()
            for r in table:
                if r["search_type"] not in grouped_items_in_seatable:
                    grouped_items_in_seatable[r["search_type"]] = list()
                grouped_items_in_seatable[r["search_type"]].extend(correct_explorer_items(r[item_type]))

            # Metastore's
            for search_type, items_in_seatable in grouped_items_in_seatable.items():
                items_in_metastore = self.metastore._list_explorer_item_names(
                    search_type=search_type, item_type=item_type
                )
                items_to_add = list(set(items_in_seatable) - set(items_in_metastore))
                items_to_delete = list(set(items_in_metastore) - set(items_in_seatable))
                # add items
                if items_to_add:
                    self.metastore._add_explorer_items(
                        search_type=search_type, item_type=item_type, items=items_to_add
                    )
                # delete items
                if items_to_delete:
                    self.metastore._delete_explorer_items(
                        search_type=search_type, item_type=item_type, items=items_to_delete
                    )

    async def sync_scrapers(self):
        # [TODO] DELETE SCRAPERS
        scrapers = await self.client.read_table("scraper")
        for s in scrapers:
            self.metastore.upsert_scraper_scraper(
                scraper_name=s["scraper_name"],
                target_domain=s["target_domain"],
                target_patterns=s["target_patterns"],
                api_endpoint=s["api_endpoint"],
                api_params=s["api_params"],
                default_interval_days=s["default_interval_days"],
            )
