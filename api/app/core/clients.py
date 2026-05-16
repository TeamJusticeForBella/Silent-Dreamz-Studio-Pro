import boto3
import nats
import redis.asyncio as redis
from opensearchpy import AsyncOpenSearch
from qdrant_client import AsyncQdrantClient

from .config import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
opensearch_client = AsyncOpenSearch(hosts=[settings.OPENSEARCH_URL], use_ssl=False, verify_certs=False)
qdrant_client = AsyncQdrantClient(url=settings.QDRANT_URL)
s3_client = boto3.client(
    "s3",
    endpoint_url=f"http://{settings.MINIO_ENDPOINT}",
    aws_access_key_id=settings.MINIO_ACCESS_KEY,
    aws_secret_access_key=settings.MINIO_SECRET_KEY,
    region_name="us-east-1",
)

_nats_conn = None
_jetstream = None


async def connect_nats():
    global _nats_conn, _jetstream
    _nats_conn = await nats.connect(settings.NATS_URL)
    _jetstream = _nats_conn.jetstream()
    return _jetstream


async def get_jetstream():
    if _jetstream is None:
        return await connect_nats()
    return _jetstream


async def close_nats():
    global _nats_conn, _jetstream
    if _nats_conn:
        await _nats_conn.close()
        _nats_conn = None
        _jetstream = None
