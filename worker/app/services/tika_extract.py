import httpx

from worker.app.config import settings


async def extract_text(file_bytes: bytes, content_type: str) -> str:
    """Extract plain text from a file via Apache Tika PUT /tika."""
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.put(
            f"{settings.TIKA_URL}/tika",
            content=file_bytes,
            headers={
                "Content-Type": content_type,
                "Accept": "text/plain",
            },
        )
        response.raise_for_status()
        return response.text


async def extract_metadata(file_bytes: bytes, content_type: str) -> dict:
    """Extract metadata from a file via Apache Tika PUT /meta."""
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.put(
            f"{settings.TIKA_URL}/meta",
            content=file_bytes,
            headers={
                "Content-Type": content_type,
                "Accept": "application/json",
            },
        )
        response.raise_for_status()
        return response.json()
