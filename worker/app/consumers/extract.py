import json
import logging

logger = logging.getLogger(__name__)


async def handle_extract_tika(msg, js):
    """Download file, extract text via Tika, store result, and enqueue indexing."""
    from worker.app.services.storage import download_object, upload_object
    from worker.app.services.tika_extract import extract_text

    try:
        envelope = json.loads(msg.data.decode())
        payload = envelope["payload"]
        job_id = envelope["job_id"]
        workspace_id = envelope["workspace_id"]
        trace = envelope.get("trace", {})

        bucket = payload["bucket"]
        key = payload["key"]
        content_type = payload["content_type"]
        evidence_id = payload["evidence_id"]

        logger.info("extract.tika job=%s evidence=%s", job_id, evidence_id)

        # Download and extract text
        file_bytes = download_object(bucket, key)
        text = await extract_text(file_bytes, content_type)

        # Store extracted text in MinIO
        extracted_key = f"{evidence_id}/extracted.txt"
        upload_object(bucket, extracted_key, text.encode("utf-8"), "text/plain")
        logger.info("Stored extracted text at %s/%s", bucket, extracted_key)

        # Enqueue full-text indexing
        from worker.app.main import publish_job

        index_payload = {
            "evidence_id": evidence_id,
            "bucket": bucket,
            "text_key": extracted_key,
            "text": text,
        }

        await publish_job(
            js,
            subject="jobs.index.fulltext",
            kind="index.fulltext",
            workspace_id=workspace_id,
            payload=index_payload,
            parent_job_id=job_id,
            priority=envelope.get("priority", 5),
        )

        # Enqueue vector indexing
        await publish_job(
            js,
            subject="jobs.index.vector",
            kind="index.vector",
            workspace_id=workspace_id,
            payload=index_payload,
            parent_job_id=job_id,
            priority=envelope.get("priority", 5),
        )

        await msg.ack()
        logger.info("extract.tika completed job=%s", job_id)

    except Exception:
        logger.exception("extract.tika failed")
        await msg.nak()
