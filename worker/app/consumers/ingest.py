import hashlib
import json
import logging

logger = logging.getLogger(__name__)

IMAGE_CONTENT_TYPES = {"image/png", "image/jpeg", "image/tiff", "image/bmp", "image/gif", "image/webp"}
PDF_CONTENT_TYPES = {"application/pdf"}
AUDIO_CONTENT_TYPES = {"audio/mpeg", "audio/wav", "audio/ogg", "audio/flac", "audio/mp4"}
VIDEO_CONTENT_TYPES = {"video/mp4", "video/mpeg", "video/webm", "video/quicktime"}


async def handle_ingest_finalize(msg, js):
    """Download object, verify SHA-256, and fan out to extraction jobs."""
    from worker.app.services.storage import download_object

    try:
        envelope = json.loads(msg.data.decode())
        payload = envelope["payload"]
        job_id = envelope["job_id"]
        workspace_id = envelope["workspace_id"]
        trace = envelope.get("trace", {})

        bucket = payload["bucket"]
        key = payload["key"]
        expected_sha256 = payload["sha256"]
        content_type = payload.get("content_type", "application/octet-stream")
        evidence_id = payload["evidence_id"]

        logger.info("ingest.finalize job=%s evidence=%s", job_id, evidence_id)

        # Download and verify SHA-256
        file_bytes = download_object(bucket, key)
        actual_sha256 = hashlib.sha256(file_bytes).hexdigest()

        if actual_sha256 != expected_sha256:
            raise ValueError(
                f"SHA-256 mismatch: expected {expected_sha256}, got {actual_sha256}"
            )

        logger.info("SHA-256 verified for evidence=%s", evidence_id)

        # Fan out: always enqueue extract.tika
        from worker.app.main import publish_job

        base_payload = {
            "bucket": bucket,
            "key": key,
            "content_type": content_type,
            "evidence_id": evidence_id,
        }

        await publish_job(
            js,
            subject="jobs.extract.tika",
            kind="extract.tika",
            workspace_id=workspace_id,
            payload=base_payload,
            parent_job_id=job_id,
            priority=envelope.get("priority", 5),
        )

        # Fan out: OCR for images and PDFs
        if content_type in IMAGE_CONTENT_TYPES or content_type in PDF_CONTENT_TYPES:
            await publish_job(
                js,
                subject="jobs.ocr.run",
                kind="ocr.run",
                workspace_id=workspace_id,
                payload=base_payload,
                parent_job_id=job_id,
                priority=envelope.get("priority", 5),
            )

        # Fan out: transcription for audio/video
        if content_type in AUDIO_CONTENT_TYPES or content_type in VIDEO_CONTENT_TYPES:
            await publish_job(
                js,
                subject="jobs.transcribe.whisper",
                kind="transcribe.whisper",
                workspace_id=workspace_id,
                payload=base_payload,
                parent_job_id=job_id,
                priority=envelope.get("priority", 5),
            )

        await msg.ack()
        logger.info("ingest.finalize completed job=%s", job_id)

    except Exception:
        logger.exception("ingest.finalize failed")
        await msg.nak()
