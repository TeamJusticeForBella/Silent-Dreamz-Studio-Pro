from opensearchpy import AsyncOpenSearch
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import PointStruct

from worker.app.config import settings

EVIDENCE_CHUNKS_COLLECTION = "bcc_evidence_chunks_v1"


def _get_opensearch_client() -> AsyncOpenSearch:
    """Return an AsyncOpenSearch client."""
    return AsyncOpenSearch(
        hosts=[settings.OPENSEARCH_URL],
        use_ssl=False,
        verify_certs=False,
    )


def _get_qdrant_client() -> AsyncQdrantClient:
    """Return an AsyncQdrantClient."""
    return AsyncQdrantClient(url=settings.QDRANT_URL)


async def index_evidence_fulltext(
    evidence_id: str, workspace_id: str, text: str, metadata: dict | None = None
) -> None:
    """Index evidence full-text into OpenSearch."""
    client = _get_opensearch_client()
    try:
        doc = {
            "evidence_id": evidence_id,
            "workspace_id": workspace_id,
            "text": text,
            **(metadata or {}),
        }
        await client.index(
            index="bcc_evidence_fulltext",
            id=evidence_id,
            body=doc,
            refresh="wait_for",
        )
    finally:
        await client.close()


async def index_incident_fulltext(
    incident_id: str, workspace_id: str, text: str, metadata: dict | None = None
) -> None:
    """Index incident full-text into OpenSearch."""
    client = _get_opensearch_client()
    try:
        doc = {
            "incident_id": incident_id,
            "workspace_id": workspace_id,
            "text": text,
            **(metadata or {}),
        }
        await client.index(
            index="bcc_incident_fulltext",
            id=incident_id,
            body=doc,
            refresh="wait_for",
        )
    finally:
        await client.close()


async def index_draft_fulltext(
    draft_id: str, workspace_id: str, text: str, metadata: dict | None = None
) -> None:
    """Index draft full-text into OpenSearch."""
    client = _get_opensearch_client()
    try:
        doc = {
            "draft_id": draft_id,
            "workspace_id": workspace_id,
            "text": text,
            **(metadata or {}),
        }
        await client.index(
            index="bcc_draft_fulltext",
            id=draft_id,
            body=doc,
            refresh="wait_for",
        )
    finally:
        await client.close()


async def index_packet_fulltext(
    packet_id: str, workspace_id: str, text: str, metadata: dict | None = None
) -> None:
    """Index packet full-text into OpenSearch."""
    client = _get_opensearch_client()
    try:
        doc = {
            "packet_id": packet_id,
            "workspace_id": workspace_id,
            "text": text,
            **(metadata or {}),
        }
        await client.index(
            index="bcc_packet_fulltext",
            id=packet_id,
            body=doc,
            refresh="wait_for",
        )
    finally:
        await client.close()


async def upsert_evidence_chunks(points: list[PointStruct]) -> None:
    """Upsert a list of PointStruct into the Qdrant evidence chunks collection."""
    client = _get_qdrant_client()
    try:
        await client.upsert(
            collection_name=EVIDENCE_CHUNKS_COLLECTION,
            points=points,
        )
    finally:
        await client.close()
