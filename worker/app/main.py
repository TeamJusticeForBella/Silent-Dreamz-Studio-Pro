import asyncio
import json
import logging
import uuid
from datetime import datetime, timezone

import nats
from nats.js.api import StreamConfig, RetentionPolicy

from worker.app.config import settings
from worker.app.consumers.ingest import handle_ingest_finalize
from worker.app.consumers.extract import handle_extract_tika
from worker.app.consumers.ocr import handle_ocr_run
from worker.app.consumers.transcribe import handle_transcribe_whisper
from worker.app.consumers.index_fulltext import handle_index_fulltext
from worker.app.consumers.index_vector import handle_index_vector
from worker.app.consumers.export_packet import handle_export_packet
from worker.app.consumers.draft_generate import handle_draft_generate

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

STREAM_NAME = "BCC_JOBS"
STREAM_SUBJECTS = ["jobs.>"]

# Subject -> handler mapping
SUBJECT_HANDLERS = {
    "jobs.ingest.finalize": handle_ingest_finalize,
    "jobs.extract.tika": handle_extract_tika,
    "jobs.ocr.run": handle_ocr_run,
    "jobs.transcribe.whisper": handle_transcribe_whisper,
    "jobs.index.fulltext": handle_index_fulltext,
    "jobs.index.vector": handle_index_vector,
    "jobs.export.packet": handle_export_packet,
    "jobs.draft.generate": handle_draft_generate,
}


async def publish_job(
    js,
    subject: str,
    kind: str,
    workspace_id: str,
    payload: dict,
    parent_job_id: str | None = None,
    priority: int = 5,
) -> str:
    """Publish a job envelope to the NATS JetStream BCC_JOBS stream."""
    job_id = str(uuid.uuid4())
    envelope = {
        "job_id": job_id,
        "workspace_id": workspace_id,
        "kind": kind,
        "priority": priority,
        "attempt": 1,
        "max_attempts": 3,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "trace": {
            "parent_job_id": parent_job_id,
        },
        "payload": payload,
    }
    await js.publish(subject, json.dumps(envelope).encode())
    logger.info("Published job %s on %s (kind=%s)", job_id, subject, kind)
    return job_id


async def _create_handler(handler, js):
    """Return a closure that passes js context to the handler."""

    async def _wrapper(msg):
        await handler(msg, js)

    return _wrapper


async def run():
    """Main entry point: connect to NATS, set up stream and consumers, and listen."""
    logger.info("Connecting to NATS at %s", settings.NATS_URL)
    nc = await nats.connect(settings.NATS_URL)
    js = nc.jetstream()

    # Ensure BCC_JOBS stream exists
    try:
        await js.find_stream_name_by_subject("jobs.>")
        logger.info("Stream %s already exists", STREAM_NAME)
    except Exception:
        await js.add_stream(
            StreamConfig(
                name=STREAM_NAME,
                subjects=STREAM_SUBJECTS,
                retention=RetentionPolicy.WORK_QUEUE,
                max_age=7 * 24 * 60 * 60 * 10**9,  # 7 days in nanoseconds
            )
        )
        logger.info("Created stream %s", STREAM_NAME)

    # Subscribe to each subject with a durable consumer
    subscriptions = []
    for subject, handler in SUBJECT_HANDLERS.items():
        # Derive durable name from subject: jobs.ingest.finalize -> ingest_finalize
        durable_name = subject.replace("jobs.", "").replace(".", "_")
        wrapper = await _create_handler(handler, js)
        sub = await js.subscribe(
            subject,
            durable=durable_name,
            cb=wrapper,
            manual_ack=True,
        )
        subscriptions.append(sub)
        logger.info("Subscribed to %s (durable=%s)", subject, durable_name)

    logger.info("Worker is running. Listening for jobs on %d subjects.", len(subscriptions))

    # Keep running until interrupted
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass
    finally:
        logger.info("Shutting down worker...")
        for sub in subscriptions:
            await sub.unsubscribe()
        await nc.drain()
        logger.info("Worker shut down cleanly.")


def main():
    """CLI entry point."""
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        logger.info("Received KeyboardInterrupt, exiting.")


if __name__ == "__main__":
    main()
