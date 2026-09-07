import hashlib
import io
from urllib.parse import urlparse

import boto3

from worker.app.config import settings


def _get_s3_client():
    """Return a boto3 S3 client configured for MinIO."""
    parsed = urlparse(settings.MINIO_ENDPOINT)
    return boto3.client(
        "s3",
        endpoint_url=settings.MINIO_ENDPOINT,
        aws_access_key_id=settings.MINIO_ACCESS_KEY,
        aws_secret_access_key=settings.MINIO_SECRET_KEY,
        region_name="us-east-1",
        use_ssl=parsed.scheme == "https",
    )


def download_object(bucket: str, key: str) -> bytes:
    """Download an object from MinIO/S3 and return its bytes."""
    client = _get_s3_client()
    response = client.get_object(Bucket=bucket, Key=key)
    return response["Body"].read()


def upload_object(bucket: str, key: str, data: bytes, content_type: str) -> None:
    """Upload bytes to MinIO/S3."""
    client = _get_s3_client()
    client.put_object(
        Bucket=bucket,
        Key=key,
        Body=io.BytesIO(data),
        ContentLength=len(data),
        ContentType=content_type,
    )


def get_object_sha256(bucket: str, key: str) -> str:
    """Download an object and return its SHA-256 hex digest."""
    data = download_object(bucket, key)
    return hashlib.sha256(data).hexdigest()
