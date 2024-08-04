import logging
from itertools import product
from typing import Any, Dict, List, Optional, Union

from redis import Redis

from ..default import DEFAULT_REDIS_DB
from ..model import (
    ExplorerItem,
    ExplorerJob,
    Job,
    Location,
    Query,
    ScraperItem,
    ScraperJob,
    ScraperScraper,
    ScraperTarget,
    Site,
    TaskResult,
)
from ..util import hash_to_model, model_to_hash, punch_date, punch_datetime
from .util import (
    correct_explorer_items,
    name_explorer_item,
    name_job_for_explorer,
    name_job_for_scraper,
    name_scraper_scraper,
    name_scraper_target,
    split_domain_and_path_from_url,
)

logger = logging.getLogger(__package__)


class RedisMetastore:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = DEFAULT_REDIS_DB,
        password: str = None,
    ):
        logger.debug("Initializing RedisMetastore with host: %s, port: %d, db: %d", host, port, db)
        self.redis = Redis(host=host, port=port, db=db, password=password, decode_responses=True)

    ################################################################
    # Explorer
    ################################################################
    def _add_explorer_items(self, search_type: str, item_type: str, items: List[str]) -> None:
        pipe = self.redis.pipeline()
        for item in correct_explorer_items(*items):
            name = name_explorer_item(search_type=search_type, item_type=item_type, id=item)
            if self.redis.exists(name):
                continue
            model = {"query": Query, "site": Site, "location": Location}[item_type](**{item_type: item})
            mapping = model_to_hash(model)
            pipe.hset(name=name, mapping=mapping)

        # add explorer items
        new_items = [item for item, added in zip(items, pipe.execute()) if added]

        # generate new explorer jobs
        if new_items:
            logger.info("New %s %s %s are added.", search_type, item_type, new_items)
            kwarg = {"query": "queries", "site": "sites", "location": "locations"}[item_type]
            self.generate_explorer_jobs(search_type=search_type, **{kwarg: new_items})

    def _delete_explorer_items(self, search_type: str, item_type: str, items: List[str]) -> None:
        names = [
            name_explorer_item(search_type=search_type, item_type=item_type, id=item)
            for item in correct_explorer_items(*items)
        ]

        # delete explorer jobs
        self.delete_explorer_jobs(
            search_type=search_type,
            **{{"query": "queries", "site": "sites", "location": "locations"}[item_type]: items},
        )

        # delete explorer items
        self.redis.delete(*names)

    def _list_explorer_item_names(self, search_type: str, item_type: str) -> List[str]:
        pattern = name_explorer_item(search_type=search_type, item_type=item_type, id="*")
        return self.redis.keys(pattern=pattern)

    def _get_explorer_item_by_name(self, item_type: str, name: str) -> ExplorerItem:
        return hash_to_model(self.redis.hgetall(name), {"query": Query, "site": Site, "location": Location}[item_type])

    def _get_explorer_items(self, search_type: str, item_type: str) -> List[ExplorerItem]:
        names = self._list_explorer_item_names(search_type=search_type, item_type=item_type)
        return [self._get_explorer_item_by_name(item_type=item_type, name=name) for name in names]

    ################################
    # Explorer Query
    ################################
    def add_explorer_queries(self, search_type: str, *queries: str) -> None:
        return self._add_explorer_items(search_type=search_type, item_type="query", items=queries)

    def delete_explorer_queries(self, search_type: str, *queries: str) -> None:
        return self._delete_explorer_items(search_type, item_type="query", items=queries)

    def list_explorer_query_names(self, search_type: str) -> List[str]:
        return self._list_explorer_item_names(search_type, item_type="query")

    def get_explorer_query_by_name(self, name: str) -> Query:
        return self._get_explorer_item_by_name(item_type="query", name=name)

    def get_explorer_queries(self, search_type: str) -> List[Query]:
        return self._get_explorer_items(search_type=search_type, item_type="query")

    ################################
    # Explorer Site
    ################################
    def add_explorer_sites(self, search_type: str, *sites: str) -> None:
        return self._add_explorer_items(search_type=search_type, item_type="site", items=sites)

    def delete_explorer_sites(self, search_type: str, *sites: str) -> None:
        return self._delete_explorer_items(search_type=search_type, item_type="site", items=sites)

    def list_explorer_site_names(self, search_type: str) -> List[str]:
        return self._list_explorer_item_names(search_type, item_type="site")

    def get_explorer_site_by_name(self, name: str) -> Site:
        return self._get_explorer_item_by_name(item_type="site", name=name)

    def get_explorer_queries(self, search_type: str) -> List[Site]:
        return self._get_explorer_items(search_type=search_type, item_type="site")

    ################################
    # Explorer Location
    ################################
    def add_explorer_locations(self, search_type: str, *locations: str) -> None:
        return self._add_explorer_items(search_type=search_type, item_type="location", items=locations)

    def delete_explorer_locations(self, search_type: str, *locations: str) -> int:
        return self._delete_explorer_items(search_type=search_type, item_type="location", items=locations)

    def list_explorer_location_names(self, search_type: str) -> List[str]:
        return self._list_explorer_item_names(search_type, item_type="location")

    def get_explorer_location_by_name(self, name: str) -> Location:
        return self._get_explorer_item_by_name(item_type="site", name=name)

    def get_explorer_queries(self, search_type: str) -> List[Location]:
        return self._get_explorer_items(search_type=search_type, item_type="location")

    ################################################################
    # Scraper
    ################################################################
    @staticmethod
    def _name_scraper(scraper_type: str, **kwargs):
        return {"target": name_scraper_target, "scraper": name_scraper_scraper}[scraper_type](**kwargs)

    def _list_scraper_item_names(self, scraper_type, **kwargs):
        pattern = self._name_scraper(scraper_type=scraper_type, **kwargs)
        return self.redis.keys(pattern=pattern)

    def _get_scraper_item_by_name(self, scraper_type: str, name: str):
        return hash_to_model(
            self.redis.hgetall(name), {"target": ScraperTarget, "scraper": ScraperScraper}[scraper_type]
        )

    def _get_scraper_items(self, scraper_type: str, **kwargs):
        names = self._list_scraper_item_names(scraper_type=scraper_type, **kwargs)
        return [self._get_scraper_item_by_name(scraper_type=scraper_type, name=name) for name in names]

    def _delete_scraper_item(self, scraper_type: str, **kwargs):
        name = self._name_scraper(scraper_type=scraper_type, **kwargs)
        return self.redis.delete(name)

    ################################
    # Scraper Target
    ################################
    def list_scraper_target_names(self, results_type: str = "*", domain: str = "*", id: str = "*") -> List[str]:
        return self._list_scraper_item_names(scraper_type="target", results_type=results_type, domain=domain, id=id)

    def get_scraper_target_by_name(self, name: str):
        return self._get_scraper_item_by_name(scraper_type="target", name=name)

    def get_scraper_targets(self, results_type: str = "*", domain: str = "*", id: str = "*") -> List[str]:
        return self._get_scraper_items(scraper_type="target", results_type=results_type, domain=domain, id=id)

    def upsert_scraper_targets_from_search_results(self, results_type: str, search_results: List[dict]):
        logger.info("Starting upsert_targets_from_search_results with results_type: %s", results_type)
        new_targets = list()
        n = 0
        n_new = 0
        pipe = self.redis.pipeline()

        for search_result in search_results:
            link = search_result.get("link")
            if not link:
                logger.warning("Ignore target without link: %s", str(search_result))
                continue
            domain, id = split_domain_and_path_from_url(link)
            if results_type in ["shopping_results"]:
                domain, id = "shopping.google.com", search_result.get("product_id")
            name = name_scraper_target(results_type=results_type, domain=domain, id=id)
            n += 1
            if self.redis.exists(name):
                continue
            target = ScraperTarget(
                **{**search_result, "name": name, "domain": domain, "id": id, "results_type": results_type}
            )
            target_dict = model_to_hash(target)
            for key, value in target_dict.items():
                if key in ["total_hit"]:
                    pipe.hincrby(name, key)
                    continue
                pipe.hsetnx(name=name, key=key, value=value)
            new_targets.append(target)
            n_new += 1
        pipe.execute()
        logger.info("Add %d/%d new targets from results_type: %s", n_new, n, results_type)

        if new_targets:
            self.generate_scraper_jobs(*new_targets)

        return new_targets

    ################################
    # Scraper Scraper
    ################################
    def list_scraper_scraper_names(self, scraper_name: str = "*", target_domain: str = "*"):
        return self._list_scraper_item_names(
            scraper_type="scraper", scraper_name=scraper_name, target_domain=target_domain
        )

    def get_scraper_scraper_by_name(self, name: str):
        return self._get_scraper_item_by_name(scraper_type="scraper", name=name)

    def get_scraper_scrapers(self, scraper_name: str = "*", target_domain: str = "*"):
        return self._get_scraper_items(scraper_type="scraper", scraper_name=scraper_name, target_domain=target_domain)

    def delete_scraper_scraper(self, scraper_name: str, target_domain: str):
        return self._delete_scraper(scraper_type="scraper", scraper_name=scraper_name, target_domain=target_domain)

    def upsert_scraper_scraper(
        self,
        scraper_name: str,
        target_domain: str,
        target_patterns: list = None,
        api_endpoint: str = None,
        api_params: list = None,
        default_interval_days: int = 7,
    ):
        scraper_name = scraper_name.lower()
        target_domain = target_domain.lower()
        name = name_scraper_scraper(scraper_name=scraper_name, target_domain=target_domain)

        scraper = ScraperScraper(
            name=name,
            scraper_name=scraper_name,
            target_domain=target_domain,
            target_patterns=target_patterns,
            api_endpoint=api_endpoint,
            api_params=api_params,
            default_interval_days=default_interval_days,
        )

        if self.redis.exists(name):
            status = "updated"
            _scraper = self.get_scraper_scraper_by_name(name)
            _scraper_dict = {k: v for k, v in _scraper.dict().items() if k != "registered_at"}
            scraper_dict = {k: v for k, v in scraper.dict().items() if k != "registered_at"}
            if _scraper_dict == scraper_dict:
                return
            scraper = _scraper
            if target_patterns:
                scraper.target_patterns = target_patterns
            if api_endpoint:
                scraper.api_endpoint = api_endpoint
            if api_params:
                scraper.api_params = api_params
            if default_interval_days:
                scraper.default_interval_days = default_interval_days
        else:
            status = "added"

        results = self.redis.hset(name=name, mapping=model_to_hash(scraper))
        logger.info("Scraper %s is %s.", name, status)
        return results

    ################################################################
    # Job
    ################################################################
    @staticmethod
    def _name_job(job_type: str, **kwargs):
        return {"explorer": name_job_for_explorer, "scraper": name_job_for_scraper}[job_type](**kwargs)

    def _list_job_names(self, job_type: str, **kwargs):
        pattern = self._name_job(job_type=job_type, **kwargs)
        return self.redis.keys(pattern=pattern)

    def _set_job(self, job_type: str, job):
        # job_type is dummy
        return self.redis.hset(name=job.name, mapping=model_to_hash(job))

    def _get_job_by_name(self, job_type: str, name: str):
        try:
            return hash_to_model(self.redis.hgetall(name), {"explorer": ExplorerJob, "scraper": ScraperJob}[job_type])
        except Exception as ex:
            logger.error(f"Failed to get {job_type} job by name {name}: {ex}")
            raise ex

    def _get_jobs(self, job_type: str, **kwargs):
        names = self._list_job_names(job_type=job_type, **kwargs)
        return [self._get_job_by_name(job_type=job_type, name=name) for name in names]

    def _get_jobs_to_execute(self, job_type: str, **kwargs):
        jobs = self._get_jobs(job_type=job_type, **kwargs)
        return [job for job in jobs if job.active and self._is_new_or_expired(job)]

    def _update_job_from_task_result(self, job_type: str, task_result: TaskResult):
        job = self._get_job_by_name(job_type=job_type, name=task_result.name)
        job.executed_at = punch_datetime()
        job.last_log = task_result.log
        job.total_run += 1
        if task_result.success:
            job.succeeded_at = job.executed_at
            job.total_success += 1
            job.last_after = task_result.after
            job.last_before = task_result.before
            job.last_hit = task_result.hit
            job.total_hit += task_result.hit
        self._set_job(job_type=job_type, job=job)
        return job

    @staticmethod
    def _is_new_or_expired(job: Job):
        reference_date = punch_date(offset_days=-job.interval_days)
        if job.last_before is not None and job.last_before >= reference_date:
            return False
        return True

    ################################
    # Explorer Job
    ################################
    def list_explorer_job_names(
        self, search_type: str = "*", query: str = "*", site: str = "*", location: str = "*"
    ) -> List[str]:
        return self._list_job_names(
            job_type="explorer", search_type=search_type, query=query, site=site, location=location
        )

    def set_explorer_job(self, job: ExplorerJob):
        return self._set_job(job_type="explorer", job=job)

    def get_explorer_job_by_name(self, name: str):
        return self._get_job_by_name(job_type="explorer", name=name)

    def get_explorer_jobs(
        self, search_type: str = "*", query: str = "*", site: str = "*", location: str = "*"
    ) -> List[ExplorerJob]:
        return self._get_jobs(job_type="explorer", search_type=search_type, query=query, site=site, location=location)

    def get_explorer_jobs_to_execute(
        self, search_type: str = "*", query: str = "*", site: str = "*", location: str = "*"
    ) -> List[ExplorerJob]:
        return self._get_jobs_to_execute(
            job_type="explorer", search_type=search_type, query=query, site=site, location=location
        )

    def update_explorer_job_from_task_results(self, task_result: TaskResult):
        return self._update_job_from_task_result(job_type="explorer", task_result=task_result)

    def _all_if_none(self, search_type: str, item_type: str, items: list):
        if items:
            return items
        return [getattr(x, item_type) for x in self._get_explorer_items(search_type=search_type, item_type=item_type)]

    def generate_explorer_jobs(
        self, search_type: str, queries: list = None, sites: list = None, locations: list = None
    ) -> List[Any]:
        logger.info("Generating explorer jobs for search_type: %s", search_type)
        queries = self._all_if_none(search_type=search_type, item_type="query", items=queries)
        sites = self._all_if_none(search_type=search_type, item_type="site", items=sites)
        locations = self._all_if_none(search_type=search_type, item_type="locations", items=locations)

        pipe = self.redis.pipeline()
        for query, site, location in product(queries, sites, locations):
            name = name_job_for_explorer(search_type=search_type, site=site, location=location, query=query)
            if self.redis.exists(name):
                continue
            job = ExplorerJob(name=name, query=query, site=site, location=location)
            pipe.hset(name=name, mapping=model_to_hash(job))
        results = pipe.execute()
        if sum(results):
            logger.info("Add explorer jobs for search_type: %s (%s jobs)", search_type, sum(results))

    def delete_explorer_jobs(self, search_type: str, queries: list = None, sites: list = None, locations: list = None):
        queries = self._all_if_none(search_type=search_type, item_type="query", items=queries)
        sites = self._all_if_none(search_type=search_type, item_type="site", items=sites)
        locations = self._all_if_none(search_type=search_type, item_type="locations", items=locations)

        pipe = self.redis.pipeline()
        for query in queries:
            for site in sites:
                for location in locations:
                    name = name_job_for_explorer(search_type=search_type, site=site, location=location, query=query)
                    pipe.delete(name)
        results = pipe.execute()
        if sum(results):
            logger.info("Delete explorer jobs for search_type: %s (%s jobs)", search_type, sum(results))

    ################################
    # Scraper / Job
    ################################
    def list_scraper_job_names(
        self, scraper_type: str = "*", scraper_name: str = "*", target_domain: str = "*", id: str = "*"
    ) -> List[str]:
        return self._list_job_names(
            job_type="scraper",
            scraper_type=scraper_type,
            scraper_name=scraper_name,
            target_domain=target_domain,
            id=id,
        )

    def set_scraper_job(self, job: ScraperJob):
        return self._set_job(job_type="scraper", job=job)

    def get_scraper_job_by_name(self, name: str):
        return self._get_job_by_name(job_type="scraper", name=name)

    def get_scraper_jobs(
        self,
        scraper_name: str = "*",
        target_domain: str = "*",
        id: str = "*",
    ) -> List[ScraperJob]:
        return self._get_jobs(job_type="scraper", scraper_name=scraper_name, target_domain=target_domain, id=id)

    def get_scraper_jobs_to_execute(self, scraper_name: str = "*", target_domain: str = "*", id: str = "*"):
        return self._get_jobs_to_execute(
            job_type="scraper", scraper_name=scraper_name, target_domain=target_domain, id=id
        )

    def update_scraper_job_from_task_results(self, task_result: TaskResult):
        self._update_job_from_task_result(task_result=task_result, job_type="scraper")

    def generate_scraper_jobs_for_all_targets(self):
        targets = self.get_scraper_targets()
        self.generate_scraper_jobs(*targets)

    def generate_scraper_jobs(self, *targets: ScraperTarget):
        logger.info("Generating scraper jobs...")
        scrapers = self.get_scraper_scrapers()
        scrapers_group_by_domain = dict()
        for scraper in scrapers:
            if scraper.target_domain not in scrapers_group_by_domain:
                scrapers_group_by_domain[scraper.target_domain] = list()
            scrapers_group_by_domain[scraper.target_domain].append(scraper)
        new_scraper_jobs = list()
        pipe = self.redis.pipeline()
        for target in targets:
            if target.domain not in scrapers_group_by_domain:
                continue
            for scraper in scrapers_group_by_domain[target.domain]:
                name = name_job_for_scraper(
                    scraper_name=scraper.scraper_name, target_domain=target.domain, id=target.id
                )
                if self.redis.exists(name):
                    continue
                job = ScraperJob(
                    name=name,
                    title=target.title,
                    link=target.link,
                    product_id=target.product_id,
                    product_link=target.product_link,
                    source=target.source,
                    scraper=scraper.name,
                    interval_days=scraper.default_interval_days,
                )
                pipe.hset(name=name, mapping=model_to_hash(job))
                new_scraper_jobs.append(name)
        pipe.execute()
        logger.info("Generate %d scraper jobs: %s", len(new_scraper_jobs), ", ".join(new_scraper_jobs))
