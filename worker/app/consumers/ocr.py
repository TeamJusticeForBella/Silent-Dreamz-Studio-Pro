import json
import logging

logger = logging.getLogger(__name__)


async def handle_ocr_run(msg, js):
    """Placeholder OCR handler. Stores ocr.txt in MinIO."""
    from worker.app.services.storage import download_object, upload_object

    try:
        envelope = json.loads(msg.data.decode())
        payload = envelope["payload"]
        job_id = envelope["job_id"]
        workspace_id = envelope["workspace_id"]

        bucket = payload["bucket"]
        key = payload["key"]
        evidence_id = payload["evidence_id"]

        logger.info("ocr.run job=%s evidence=%s", job_id, evidence_id)

        # Download the file (placeholder: actual OCR would process it)
        _ = download_object(bucket, key)

        # Placeholder: produce empty OCR text
        ocr_text = f"[OCR placeholder for evidence {evidence_id}]"
        ocr_key = f"{evidence_id}/ocr.txt"
        upload_object(bucket, ocr_key, ocr_text.encode("utf-8"), "text/plain")

        logger.info("Stored OCR result at %s/%s", bucket, ocr_key)

        await msg.ack()
        logger.info("ocr.run completed job=%s", job_id)

    except Exception:
        logger.exception("ocr.run failed")
        await msg.nak()
