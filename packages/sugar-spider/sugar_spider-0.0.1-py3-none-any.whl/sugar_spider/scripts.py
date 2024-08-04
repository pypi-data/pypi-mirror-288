################################################################
# Example scripts.py
#  - See https://click.palletsprojects.com/en/8.1.x/
################################################################
from __future__ import print_function, unicode_literals

import click
from click_loglevel import LogLevel
from dotenv import load_dotenv

from .default import DEFAULT_REDIS_DB

load_dotenv()


################################################################
# App (Redis CRUD)
################################################################
@click.group()
def sugar_spider():
    pass


@sugar_spider.command()
@click.option("-h", "--host", default="0.0.0.0", envvar="HOST")
@click.option("-p", "--port", default=3000, envvar="PORT")
@click.option("--redis-host", default="localhost", envvar="REDIS_HOST")
@click.option("--redis-port", default=6379, envvar="REDIS_PORT")
@click.option("--redis-db", default=DEFAULT_REDIS_DB, envvar="REDIS_DB")
@click.option("--reload", is_flag=True)
@click.option("--log-level", type=LogLevel(), default="INFO", help="Set Logging Level")
def start_app(
    host: str,
    port: int,
    redis_host: str,
    redis_port: int,
    redis_db: int,
    reload: bool,
    log_level: LogLevel,
):
    import logging
    import os

    import uvicorn

    os.environ["REDIS_HOST"] = redis_host
    os.environ["REDIS_PORT"] = str(redis_port)
    os.environ["REDIS_DB"] = str(redis_db)

    logging.basicConfig(level=log_level)
    logger = logging.getLogger(__package__)
    options = {
        "host": host,
        "port": port,
        "redis_host": redis_host,
        "redis_port": redis_port,
        "redis_db": redis_db,
    }
    logger.info("Start app with options: %s", ", ".join([f"{k}={v}" for k, v in options.items()]))

    if reload:
        app = "sugar_spider.api.app:app"
    else:
        from .api.app import app

    uvicorn.run(app, host=host, port=port, reload=reload, log_level=log_level)


################################################################
# Syncer (SeaTable -> Redis)
################################################################
@sugar_spider.command()
@click.option("--seatable-url", default="https://seatable.cjcj.io", envvar="SEATABLE_URL")
@click.option("--seatable-api-token", envvar="SEATABLE_API_TOKEN")
@click.option("--redis-host", default="localhost", envvar="REDIS_HOST")
@click.option("--redis-port", default=6379, envvar="REDIS_PORT")
@click.option("--redis-db", default=DEFAULT_REDIS_DB, envvar="REDIS_DB")
@click.option("--wait-for-sec", default=600)
@click.option("--log-level", type=LogLevel(), default="INFO", help="Set Logging Level")
def start_syncer_seatable(
    seatable_url: str,
    seatable_api_token: str,
    redis_host: str,
    redis_port: int,
    redis_db: int,
    wait_for_sec: float,
    log_level: LogLevel,
):
    import asyncio
    import logging

    from .manager.seatable import SeaTableMetadataSyncer
    from .metastore.redis import RedisMetastore

    logging.basicConfig(level=log_level)
    logger = logging.getLogger(__package__)
    options = {
        "seatable_url": seatable_url,
        "seatable_api_token": 24 * "*" + seatable_api_token[24:],
        "redis_host": redis_host,
        "redis_port": redis_port,
        "redis_db": redis_db,
        "wait_for_sec": wait_for_sec,
    }
    logger.info("Start seatable syncer with options: %s", ", ".join([f"{k}={v}" for k, v in options.items()]))

    metastore = RedisMetastore(host=redis_host, port=redis_port, db=redis_db)

    syncer = SeaTableMetadataSyncer(
        seatable_url=seatable_url,
        seatable_api_token=seatable_api_token,
        metastore=metastore,
        wait_for_sec=wait_for_sec,
    )

    async def run_explorer():
        try:
            await syncer.start_syncer()
        finally:
            pass

    asyncio.run(run_explorer())


################################################################
# Explorer / Google Search
################################################################
@sugar_spider.command()
@click.option("--serpapi-api-key", envvar="SERPAPI_API_KEY")
@click.option("--serpapi-rpm", default=30, envvar="SERPAPI_RPM", help="SerpAPI max requests per minute")
@click.option("--redis-host", default="localhost", envvar="REDIS_HOST")
@click.option("--redis-port", default=6379, envvar="REDIS_PORT")
@click.option("--redis-db", default=DEFAULT_REDIS_DB, envvar="REDIS_DB")
@click.option("--kafka-client-id", default="spider-explorer-serpapi", envvar="KAFKA_CLIENT_ID")
@click.option("--kafka-topic", default="prod.spider.explorer.google", envvar="KAFKA_TOPIC")
@click.option(
    "--kafka-bootstrap-servers",
    default="pkc-e82om.ap-northeast-2.aws.confluent.cloud:9092",
    envvar="KAFKA_BOOTSTRAP_SERVERS",
)
@click.option("--kafka-sasl-plain-username", envvar="KAFKA_SASL_PLAIN_USERNAME")
@click.option("--kafka-sasl-plain-password", envvar="KAFKA_SASL_PLAIN_PASSWORD")
@click.option("--max-concurrent-tasks", default=30, envvar="MAX_CONCURRENT_TASKS")
@click.option("--start-days-ago", default=360, envvar="START_DAYS_AGO")
@click.option("--max-search-days", default=90, envvar="MAX_SEARCH_DAYS")
@click.option("--log-level", type=LogLevel(), default="INFO", help="Set Logging Level")
def start_explorer_google_search(
    serpapi_api_key: str,
    serpapi_rpm: int,
    redis_host: str,
    redis_port: int,
    redis_db: int,
    kafka_client_id: str,
    kafka_topic: str,
    kafka_bootstrap_servers: str,
    kafka_sasl_plain_username: str,
    kafka_sasl_plain_password: str,
    max_concurrent_tasks: int,
    start_days_ago: int,
    max_search_days: int,
    log_level: LogLevel,
):
    import asyncio
    import logging

    from .explorer.serpapi.google_search import GoogleSearchExplorer
    from .handler.kafka import KafkaProducer
    from .metastore.redis import RedisMetastore
    from .parser import serpapi_google_search_parser

    logging.basicConfig(level=log_level)
    logging.getLogger("aiokafka").setLevel(logging.WARNING)

    metastore = RedisMetastore(host=redis_host, port=redis_port, db=redis_db)

    kafka_producer = KafkaProducer(
        client_id=kafka_client_id,
        topic=kafka_topic,
        bootstrap_servers=kafka_bootstrap_servers,
        sasl_plain_username=kafka_sasl_plain_username,
        sasl_plain_password=kafka_sasl_plain_password,
    )

    explorer = GoogleSearchExplorer(
        serpapi_api_key=serpapi_api_key,
        serpapi_rpm=serpapi_rpm,
        serpapi_gl="us",
        start_days_ago=start_days_ago,
        max_search_days=max_search_days,
        metastore=metastore,
        max_concurrent_tasks=max_concurrent_tasks,
        parser=serpapi_google_search_parser,
        handler=kafka_producer,
    )

    def main():
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(explorer.start_explorer())
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

    asyncio.run(main())


################################################################
# Explorer / Google Shopping
################################################################
@sugar_spider.command()
@click.option("--serpapi-api-key", envvar="SERPAPI_API_KEY")
@click.option("--serpapi-rpm", default=30, envvar="SERPAPI_RPM", help="SerpAPI max requests per minute")
@click.option("--redis-host", default="localhost", envvar="REDIS_HOST")
@click.option("--redis-port", default=6379, envvar="REDIS_PORT")
@click.option("--redis-db", default=DEFAULT_REDIS_DB, envvar="REDIS_DB")
@click.option("--kafka-client-id", default="spider-explorer-serpapi", envvar="KAFKA_CLIENT_ID")
@click.option("--kafka-topic", default="prod.spider.explorer.google", envvar="KAFKA_TOPIC")
@click.option(
    "--kafka-bootstrap-servers",
    default="pkc-e82om.ap-northeast-2.aws.confluent.cloud:9092",
    envvar="KAFKA_BOOTSTRAP_SERVERS",
)
@click.option("--kafka-sasl-plain-username", envvar="KAFKA_SASL_PLAIN_USERNAME")
@click.option("--kafka-sasl-plain-password", envvar="KAFKA_SASL_PLAIN_PASSWORD")
@click.option("--max-concurrent-tasks", default=30, envvar="MAX_CONCURRENT_TASKS")
@click.option("--log-level", type=LogLevel(), default="INFO", help="Set Logging Level")
def start_explorer_google_shopping(
    serpapi_api_key: str,
    serpapi_rpm: int,
    redis_host: str,
    redis_port: int,
    redis_db: int,
    kafka_client_id: str,
    kafka_topic: str,
    kafka_bootstrap_servers: str,
    kafka_sasl_plain_username: str,
    kafka_sasl_plain_password: str,
    max_concurrent_tasks: int,
    log_level: LogLevel,
):
    import asyncio
    import logging

    from .explorer.serpapi.google_shopping import GoogleShoppingExplorer
    from .handler.kafka import KafkaProducer
    from .metastore.redis import RedisMetastore
    from .parser import serpapi_google_search_parser

    logging.basicConfig(level=log_level)
    logging.getLogger("aiokafka").setLevel(logging.WARNING)

    metastore = RedisMetastore(host=redis_host, port=redis_port, db=redis_db)

    kafka_producer = KafkaProducer(
        client_id=kafka_client_id,
        topic=kafka_topic,
        bootstrap_servers=kafka_bootstrap_servers,
        sasl_plain_username=kafka_sasl_plain_username,
        sasl_plain_password=kafka_sasl_plain_password,
    )

    explorer = GoogleShoppingExplorer(
        serpapi_api_key=serpapi_api_key,
        serpapi_rpm=serpapi_rpm,
        serpapi_gl="us",
        metastore=metastore,
        max_concurrent_tasks=max_concurrent_tasks,
        parser=serpapi_google_search_parser,
        handler=kafka_producer,
    )

    def main():
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(explorer.start_explorer())
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

    asyncio.run(main())


################################################################
# Scraper / SerpAPI Google Product
################################################################
@sugar_spider.command()
@click.option("--serpapi-api-key", envvar="SERPAPI_API_KEY")
@click.option("--serpapi-rpm", default=30, envvar="SERPAPI_RPM", help="SerpAPI max requests per minute")
@click.option("--redis-host", default="localhost", envvar="REDIS_HOST")
@click.option("--redis-port", default=6379, envvar="REDIS_PORT")
@click.option("--redis-db", default=DEFAULT_REDIS_DB, envvar="REDIS_DB")
@click.option("--kafka-client-id", default="spider-explorer-serpapi", envvar="KAFKA_CLIENT_ID")
@click.option("--kafka-topic", default="prod.spider.explorer.google", envvar="KAFKA_TOPIC")
@click.option(
    "--kafka-bootstrap-servers",
    default="pkc-e82om.ap-northeast-2.aws.confluent.cloud:9092",
    envvar="KAFKA_BOOTSTRAP_SERVERS",
)
@click.option("--kafka-sasl-plain-username", envvar="KAFKA_SASL_PLAIN_USERNAME")
@click.option("--kafka-sasl-plain-password", envvar="KAFKA_SASL_PLAIN_PASSWORD")
@click.option("--max-concurrent-tasks", default=30, envvar="MAX_CONCURRENT_TASKS")
@click.option("--log-level", type=LogLevel(), default="INFO", help="Set Logging Level")
def start_scraper_google_product(
    serpapi_api_key: str,
    serpapi_rpm: int,
    redis_host: str,
    redis_port: int,
    redis_db: int,
    kafka_client_id: str,
    kafka_topic: str,
    kafka_bootstrap_servers: str,
    kafka_sasl_plain_username: str,
    kafka_sasl_plain_password: str,
    max_concurrent_tasks: int,
    log_level: LogLevel,
):
    import asyncio
    import logging

    from .handler.kafka import KafkaProducer
    from .metastore.redis import RedisMetastore
    from .parser import serpapi_google_search_parser
    from .scraper.serpapi.google_product import GoogleProductScraper

    logging.basicConfig(level=log_level)
    logging.getLogger("aiokafka").setLevel(logging.WARNING)

    metastore = RedisMetastore(host=redis_host, port=redis_port, db=redis_db)

    kafka_producer = KafkaProducer(
        client_id=kafka_client_id,
        topic=kafka_topic,
        bootstrap_servers=kafka_bootstrap_servers,
        sasl_plain_username=kafka_sasl_plain_username,
        sasl_plain_password=kafka_sasl_plain_password,
    )

    scraper = GoogleProductScraper(
        serpapi_api_key=serpapi_api_key,
        gl="us",
        serpapi_rpm=serpapi_rpm,
        metastore=metastore,
        parser=serpapi_google_search_parser,
        handler=kafka_producer,
        max_concurrent_tasks=max_concurrent_tasks,
    )

    def main():
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(scraper.start_scraper())
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

    asyncio.run(main())


################################################################
# Bright Data Scraper API Scrapers
################################################################


################################
# Instagram
################################
@sugar_spider.command()
@click.option("--brd-api-token", envvar="BRD_API_TOKEN")
@click.option("--redis-host", default="localhost", envvar="REDIS_HOST")
@click.option("--redis-port", default=6379, envvar="REDIS_PORT")
@click.option("--redis-db", default=DEFAULT_REDIS_DB, envvar="REDIS_DB")
@click.option("--kafka-client-id", default="spider-explorer-serpapi", envvar="KAFKA_CLIENT_ID")
@click.option("--kafka-topic", default="prod.spider.explorer.google", envvar="KAFKA_TOPIC")
@click.option(
    "--kafka-bootstrap-servers",
    default="pkc-e82om.ap-northeast-2.aws.confluent.cloud:9092",
    envvar="KAFKA_BOOTSTRAP_SERVERS",
)
@click.option("--kafka-sasl-plain-username", envvar="KAFKA_SASL_PLAIN_USERNAME")
@click.option("--kafka-sasl-plain-password", envvar="KAFKA_SASL_PLAIN_PASSWORD")
@click.option("--max-concurrent-tasks", default=30, envvar="MAX_CONCURRENT_TASKS")
@click.option("--log-level", type=LogLevel(), default="INFO", help="Set Logging Level")
def start_scraper_brd_instagram(
    brd_api_token: str,
    redis_host: str,
    redis_port: int,
    redis_db: int,
    kafka_client_id: str,
    kafka_topic: str,
    kafka_bootstrap_servers: str,
    kafka_sasl_plain_username: str,
    kafka_sasl_plain_password: str,
    max_concurrent_tasks: int,
    log_level: LogLevel,
):
    import asyncio
    import logging

    from .handler.kafka import KafkaProducer
    from .metastore.redis import RedisMetastore
    from .parser import brd_scraper_api_parser
    from .scraper.brd.instagram import InstagramScraper

    logging.basicConfig(level=log_level)
    logging.getLogger("aiokafka").setLevel(logging.WARNING)

    metastore = RedisMetastore(host=redis_host, port=redis_port, db=redis_db)

    kafka_producer = KafkaProducer(
        client_id=kafka_client_id,
        topic=kafka_topic,
        bootstrap_servers=kafka_bootstrap_servers,
        sasl_plain_username=kafka_sasl_plain_username,
        sasl_plain_password=kafka_sasl_plain_password,
    )

    scraper = InstagramScraper(
        brd_api_token=brd_api_token,
        metastore=metastore,
        parser=brd_scraper_api_parser,
        handler=kafka_producer,
        max_concurrent_tasks=max_concurrent_tasks,
    )

    def main():
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(scraper.start_scraper())
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

    asyncio.run(main())


################################
# TikTok
################################
@sugar_spider.command()
@click.option("--brd-api-token", envvar="BRD_API_TOKEN")
@click.option("--redis-host", default="localhost", envvar="REDIS_HOST")
@click.option("--redis-port", default=6379, envvar="REDIS_PORT")
@click.option("--redis-db", default=DEFAULT_REDIS_DB, envvar="REDIS_DB")
@click.option("--kafka-client-id", default="spider-explorer-serpapi", envvar="KAFKA_CLIENT_ID")
@click.option("--kafka-topic", default="prod.spider.explorer.google", envvar="KAFKA_TOPIC")
@click.option(
    "--kafka-bootstrap-servers",
    default="pkc-e82om.ap-northeast-2.aws.confluent.cloud:9092",
    envvar="KAFKA_BOOTSTRAP_SERVERS",
)
@click.option("--kafka-sasl-plain-username", envvar="KAFKA_SASL_PLAIN_USERNAME")
@click.option("--kafka-sasl-plain-password", envvar="KAFKA_SASL_PLAIN_PASSWORD")
@click.option("--max-concurrent-tasks", default=30, envvar="MAX_CONCURRENT_TASKS")
@click.option("--log-level", type=LogLevel(), default="INFO", help="Set Logging Level")
def start_scraper_brd_tiktok(
    brd_api_token: str,
    redis_host: str,
    redis_port: int,
    redis_db: int,
    kafka_client_id: str,
    kafka_topic: str,
    kafka_bootstrap_servers: str,
    kafka_sasl_plain_username: str,
    kafka_sasl_plain_password: str,
    max_concurrent_tasks: int,
    log_level: LogLevel,
):
    import asyncio
    import logging

    from .handler.kafka import KafkaProducer
    from .metastore.redis import RedisMetastore
    from .parser import brd_scraper_api_parser
    from .scraper.brd.tiktok import TikTokScraper

    logging.basicConfig(level=log_level)
    logging.getLogger("aiokafka").setLevel(logging.WARNING)

    metastore = RedisMetastore(host=redis_host, port=redis_port, db=redis_db)

    kafka_producer = KafkaProducer(
        client_id=kafka_client_id,
        topic=kafka_topic,
        bootstrap_servers=kafka_bootstrap_servers,
        sasl_plain_username=kafka_sasl_plain_username,
        sasl_plain_password=kafka_sasl_plain_password,
    )

    scraper = TikTokScraper(
        brd_api_token=brd_api_token,
        metastore=metastore,
        parser=brd_scraper_api_parser,
        handler=kafka_producer,
        max_concurrent_tasks=max_concurrent_tasks,
    )

    def main():
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(scraper.start_scraper())
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

    asyncio.run(main())
