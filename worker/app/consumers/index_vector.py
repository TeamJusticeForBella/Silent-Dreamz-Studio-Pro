import json
import logging
import uuid

from qdrant_client.models import PointStruct

logger = logging.getLogger(__name__)

CHUNK_SIZE = 512
CHUNK_OVERLAP = 64
EMBEDDING_DIM = 768


def _chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
        if start < 0:
            break
    return chunks


def _placeholder_embedding(dim: int = EMBEDDING_DIM) -> list[float]:
    """Return a zero-vector placeholder embedding."""
    return [0.0] * dim


async def handle_index_vector(msg, js):
    """Chunk text, generate placeholder embeddings, and upsert to Qdrant."""
    from worker.app.services.indexing import upsert_evidence_chunks

    try:
        envelope = json.loads(msg.data.decode())
        payload = envelope["payload"]
        job_id = envelope["job_id"]
        workspace_id = envelope["workspace_id"]

        evidence_id = payload["evidence_id"]
        text = payload["text"]

        logger.info("index.vector job=%s evidence=%s", job_id, evidence_id)

        chunks = _chunk_text(text)
        points = []

        for i, chunk in enumerate(chunks):
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{evidence_id}:chunk:{i}"))
            points.append(
                PointStruct(
                    id=point_id,
                    vector=_placeholder_embedding(),
                    payload={
                        "evidence_id": evidence_id,
                        "workspace_id": workspace_id,
                        "chunk_index": i,
                        "text": chunk,
                    },
                )
            )

        if points:
            await upsert_evidence_chunks(points)
            logger.info("Upserted %d chunks for evidence=%s", len(points), evidence_id)

        await msg.ack()
        logger.info("index.vector completed job=%s", job_id)

    except Exception:
        logger.exception("index.vector failed")
        await msg.nak()
