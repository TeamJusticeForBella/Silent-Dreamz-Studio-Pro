import json
import logging

logger = logging.getLogger(__name__)


async def handle_index_fulltext(msg, js):
    """Index extracted text into OpenSearch full-text index."""
    from worker.app.services.indexing import index_evidence_fulltext

    try:
        envelope = json.loads(msg.data.decode())
        payload = envelope["payload"]
        job_id = envelope["job_id"]
        workspace_id = envelope["workspace_id"]

        evidence_id = payload["evidence_id"]
        text = payload["text"]

        logger.info("index.fulltext job=%s evidence=%s", job_id, evidence_id)

        await index_evidence_fulltext(
            evidence_id=evidence_id,
            workspace_id=workspace_id,
            text=text,
            metadata={"source": "tika_extract"},
        )

        await msg.ack()
        logger.info("index.fulltext completed job=%s", job_id)

    except Exception:
        logger.exception("index.fulltext failed")
        await msg.nak()
