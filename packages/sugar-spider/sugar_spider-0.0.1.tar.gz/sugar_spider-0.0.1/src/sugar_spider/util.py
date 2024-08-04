import base64
import logging
from datetime import datetime, timedelta

import orjson
from pydantic import BaseModel

from .common import TZ

logger = logging.getLogger(__package__)


def encoder(key: str) -> str:
    key = key.encode("utf-8")
    return base64.urlsafe_b64encode(key).decode("utf-8").rstrip("=")


def decoder(encoded_key: str) -> str:
    return base64.urlsafe_b64decode((encoded_key + "=")).decode("utf-8")


def punch_datetime(reference_datetime=None, offset_seconds=None, tz=TZ) -> str:
    if not reference_datetime:
        reference_datetime = datetime.now(tz=tz)
    if isinstance(reference_datetime, str):
        reference_datetime = datetime.fromisoformat(reference_datetime)
    _datetime = reference_datetime
    if offset_seconds:
        _datetime += timedelta(seconds=offset_seconds)
    return _datetime.isoformat()


def punch_date(reference_date=None, offset_days=None, tz=TZ) -> str:
    if not reference_date:
        reference_date = datetime.now(tz=tz)
    if isinstance(reference_date, str):
        reference_date = datetime.strptime(reference_date, "%Y-%m-%d")
    date = reference_date
    if offset_days:
        date += timedelta(days=offset_days)
    return date.strftime("%Y-%m-%d")


def to_datetime(datetime_str: str) -> datetime:
    return datetime.fromisoformat(datetime_str)


def to_date(date_str: str) -> datetime.date:
    return datetime.strptime(date_str, "%Y-%m-%d")


def model_to_hash(model: BaseModel):
    return {k: v if isinstance(v, str) else orjson.dumps(v) for k, v in model.dict().items()}


def ensure_type(v: str):
    if v == "null":
        return None
    if v == "true":
        return True
    if v == "false":
        return False
    return v


def hash_to_model(hash: dict, Model: BaseModel, ignore_null: bool = False):
    if not hash:
        return hash
    schema = {k: v["type"] for k, v in Model.schema()["properties"].items()}
    record = {
        k: ensure_type(v) if schema[k] in ["string"] else orjson.loads(v) for k, v in hash.items() if k in schema
    }
    if ignore_null:
        record = {k: v for k, v in record.items() if v is not None}
    return Model(**record)
