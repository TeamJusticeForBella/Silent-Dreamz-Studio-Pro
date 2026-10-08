import json
import logging

logger = logging.getLogger(__name__)


async def handle_transcribe_whisper(msg, js):
    """Placeholder Whisper transcription handler. Stores transcript.txt in MinIO."""
    from worker.app.services.storage import download_object, upload_object

    try:
        envelope = json.loads(msg.data.decode())
        payload = envelope["payload"]
        job_id = envelope["job_id"]
        workspace_id = envelope["workspace_id"]

        bucket = payload["bucket"]
        key = payload["key"]
        evidence_id = payload["evidence_id"]

        logger.info("transcribe.whisper job=%s evidence=%s", job_id, evidence_id)

        # Download the file (placeholder: actual transcription would process it)
        _ = download_object(bucket, key)

        # Placeholder: produce empty transcript
        transcript_text = f"[Transcript placeholder for evidence {evidence_id}]"
        transcript_key = f"{evidence_id}/transcript.txt"
        upload_object(bucket, transcript_key, transcript_text.encode("utf-8"), "text/plain")

        logger.info("Stored transcript at %s/%s", bucket, transcript_key)

        await msg.ack()
        logger.info("transcribe.whisper completed job=%s", job_id)

    except Exception:
        logger.exception("transcribe.whisper failed")
        await msg.nak()
