from typing import Callable, List, Union

import orjson
from aiokafka import AIOKafkaProducer
from aiokafka.helpers import create_ssl_context

from ..parser import serpapi_google_search_parser
from .exception import KafkaProducerInitError, KafkaProducerProduceError


class KafkaProducer:
    def __init__(
        self,
        client_id: str,
        topic: str,
        *,
        bootstrap_servers: Union[str, List[str]],
        sasl_plain_username: str,
        sasl_plain_password: str,
        parser: Callable = serpapi_google_search_parser,
    ):
        self.topic = topic
        self.client_id = client_id
        self.kafka_conf = {
            "bootstrap_servers": bootstrap_servers,
            "security_protocol": "SASL_SSL",
            "ssl_context": create_ssl_context(),
            "sasl_mechanism": "PLAIN",
            "sasl_plain_username": sasl_plain_username,
            "sasl_plain_password": sasl_plain_password,
        }
        self.parser = parser

    async def __call__(self, records: List[dict]):
        # publish records
        try:
            producer = AIOKafkaProducer(client_id=self.client_id, **self.kafka_conf)
        except Exception as ex:
            raise KafkaProducerInitError(str(ex))

        await producer.start()
        try:
            # batch = producer.create_batch()
            for record in records:
                key = orjson.dumps(record["key"])
                value = orjson.dumps(record["value"])
                await producer.send_and_wait(topic=self.topic, value=value, key=key)
        except Exception as ex:
            raise KafkaProducerProduceError(str(ex))
        finally:
            await producer.stop()
